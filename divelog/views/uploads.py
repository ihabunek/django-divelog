from divelog.forms import DiveUploadForm
from divelog.models import DiveUpload, Location, Sample, Event
from divelog.parsers import subsurface
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from django.template.context import RequestContext
from django.utils import timezone
from django.utils.log import getLogger
from django.views.decorators.cache import never_cache
from xml.etree.ElementTree import ParseError
import os

@login_required
@never_cache
def upload_add(request):
    if request.method == 'POST':
        form = DiveUploadForm(request.POST, request.FILES)
        form.instance.user = request.user
        form.instance.uploaded = timezone.now()
        
        if form.is_valid():
            upload = form.save()
            messages.success(request, 'File upload successful.')
            return redirect('divelog_upload_view', upload_id = upload.id)
    else:
        form = DiveUploadForm()
    
    t = loader.get_template('divelog/uploads/add.html')
    c = RequestContext(request, {
        'form': form
    });
    return HttpResponse(t.render(c))
 
@login_required
def upload_list(request):
    uploads = DiveUpload.objects.filter(user = request.user)
    t = loader.get_template('divelog/uploads/list.html')
    c = RequestContext(request, {
        'uploads': uploads
    });
    return HttpResponse(t.render(c))

@login_required
def upload_view(request, upload_id):
    """
    Displays a single upload.
    """
    try:
        upload = DiveUpload.objects.get(pk = upload_id)
    except DiveUpload.DoesNotExist:
        raise Http404
    
    if os.path.exists(upload.data.path):
        file_size = os.path.getsize(upload.data.path)
    
#        # Fetch fingerprints of existing user's dives for marking already uploaded dives
#        fingerprints = {}
#        dives = Dive.objects.filter(user = request.user).values_list('id', 'fingerprint')
#        for dive_id, fingerprint in dives:
#            fingerprints[fingerprint] = dive_id
    
        # Parse the XML file
        try:
            with open(upload.data.path) as input:
                overview = subsurface.parse_short(upload.data.path)
        except Exception:
            messages.error(request, "Uploaded data cannot be parsed.")
            overview = []
    
#        # Add dive_id for existing dives
#        for item in overview:
#            if item['fingerprint'] in fingerprints:
#                item['dive_id'] = fingerprints[item['fingerprint']]

    else:
        overview = None
        file_size = None
        messages.error(request, "The uploaded file has been deleted from the system.")
    
    t = loader.get_template('divelog/uploads/view.html')
    c = RequestContext(request, {
        'upload': upload,
        'overview': overview,
        'file_size': file_size,
    });
    return HttpResponse(t.render(c))

@login_required
@never_cache
def upload_import(request):
    logger = getLogger('app')

    if request.method == 'POST':
        # Provided numbers identify dives which should be imported
        numbers = request.POST.getlist('numbers')
        upload_id = request.POST.get('upload_id')
        
        try:
            upload = DiveUpload.objects.get(pk = upload_id)
            logger.debug("Parsing dives from upload #%d" % int(upload_id))

            # TODO: Parse only requested dives to improve performance
            dives = subsurface.parse_full(upload.data.path)
            logger.debug("Parsed %d dives" % len(dives))

            # Save parsed dives
            count = 0
            for dive, samples, events, sLocation in dives:
                if unicode(dive.number) in numbers:
                    _save_dive(request.user, dive, samples, events, sLocation)
                    count += 1
            
            logger.info("Saved %d dives" % count)
            messages.success(request, "Successfully imported %d dives." % count)
            return redirect('divelog_dive_list')
            
        except ParseError as ex:
            logger.error(ex)
            messages.error(request, "Failed parsing XML file.<br />Underlying error: %s" % ex.message)
            return redirect('divelog_upload_view', upload_id = upload_id)
        
    t = loader.get_template('divelog/index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

@transaction.commit_on_success
def _save_dive(user, dive, samples, events, sLocation):
    logger = getLogger('app')
    logger.info("Saving dive %s" % dive.fingerprint)
    
    if sLocation:
        locations = Location.objects.filter(name=sLocation)
        if locations:
            location = locations[0]
        else:
            location = Location()
            location.name = sLocation
            location.user = user
            location.save()
        dive.location = location
    
    dive.user = user
    dive.size = len(samples)
    dive.save()
    
    for sample in samples:
        sample.dive = dive
    
    for event in events:
        event.dive = dive
        
    Sample.objects.bulk_create(samples)
    Event.objects.bulk_create(events)
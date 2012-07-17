from divelog.forms import DiveForm, DiveUploadForm, UserProfileForm, \
    ValidatingPasswordChangeForm, LocationForm
from divelog.models import Dive, DiveUpload, Sample, Event, Location
from divelog.parsers import libdc, subsurface
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.utils import timezone, simplejson
from django.views.decorators.cache import never_cache
from xml.etree.cElementTree import ParseError
import logging
import os

def index(request):
    t = loader.get_template('divelog/index.html')
    c = RequestContext(request);
    return HttpResponse(t.render(c))

def gallery(request):
    t = loader.get_template('divelog/gallery.html')
    c = RequestContext(request);
    return HttpResponse(t.render(c))

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
            return redirect('divelog.views.upload_view', upload_id = upload.id)
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
    if request.method == 'POST':
        # Provided numbers identify dives which should be imported
        numbers = request.POST.getlist('numbers')
        upload_id = request.POST.get('upload_id')
        
        try:
            upload = DiveUpload.objects.get(pk = upload_id)
            logging.debug("Parsing dives from upload #%d" % int(upload_id))

            # TODO: Parse only requested dives to improve performance
            dives = subsurface.parse_full(upload.data.path)
            logging.debug("Parsed %d dives" % len(dives))            

            # Save parsed dives
            count = 0
            for dive, samples, events, sLocation in dives:
                if unicode(dive.number) in numbers:
                    _save_dive(request.user, dive, samples, events, sLocation)
                    count += 1
            
            logging.info("Saved %d dives" % count)
            messages.success(request, "Successfully imported %d dives." % count)
            return redirect('divelog.views.dive_list')
            
        except ParseError as ex:
            logging.error(ex)
            messages.error(request, "Failed parsing XML file.<br />Underlying error: %s" % ex.message)
            return redirect('divelog.views.upload_view', upload_id = upload_id)
        
    t = loader.get_template('divelog/index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

@transaction.commit_on_success
def _save_dive(user, dive, samples, events, sLocation):
    logging.info("Saving dive %s" % dive.fingerprint)
    
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

@login_required
def dive_view(request, dive_id):
    """
    Displays a single dive.
    """
    try:
        dive = Dive.objects.get(pk = dive_id)
    except Dive.DoesNotExist:
        raise Http404
    
    if dive.user != request.user:
        raise Http404
    
    # Find next and previous dives (if any exist)
    next = Dive.objects.filter(user = request.user, date_time__gt = dive.date_time).order_by('date_time')[0:1]
    prev = Dive.objects.filter(user = request.user, date_time__lt = dive.date_time).order_by('-date_time')[0:1]
    
    t = loader.get_template('divelog/dives/view.html')
    c = RequestContext(request, {
        'dive': dive,
        'next': next[0].id if next else None,
        'prev': prev[0].id if prev else None
    });
    return HttpResponse(t.render(c))

@login_required
def dive_list(request):
    """
    Displays a list of user's dives.
    """
    dives = Dive.objects.filter(user = request.user, status = 'A')

    t = loader.get_template('divelog/dives/list.html')
    c = RequestContext(request, {
        'dives': dives
    });
    return HttpResponse(t.render(c))

@login_required
@never_cache
def dive_edit(request, dive_id):
    """
    View for editing dive data.
    """
    
    # Fetch locations for auto-completion
#    locations = Dive.objects.filter(user=request.user).exclude(location=None).values_list('location', flat=True).distinct()
    
    if request.method == 'POST':
        dive = Dive.objects.get(pk = dive_id)
        form = DiveForm(request.POST, instance = dive)
        if form.is_valid():
            form.save()
            return redirect('divelog.views.dive_view', dive_id = dive_id)
    else:
        dive = Dive.objects.get(pk = dive_id)
        form = DiveForm(instance = dive)
    
    t = loader.get_template('divelog/dives/edit.html')
    c = RequestContext(request, {
        'form': form,
        'dive_id': dive_id,
#        'locations': locations,
    });
    return HttpResponse(t.render(c))

@login_required
@never_cache
def dive_trash(request, dive_id):
    """
    Moves a dive to trash (changes dive status to D).
    """
    try:
        dive = Dive.objects.get(pk = dive_id)
    except Dive.DoesNotExist:
        raise Http404
    
    # Prevent deleting other people's dives
    if dive.user != request.user:
        raise Http404
    
    # Change status to Defunct
    dive.status = 'D'
    dive.save()
    
    undo_url = reverse('divelog.views.dive_restore', args=[dive_id])
    messages.success(request, 'Dive #%d moved to trash. <a href="%s">Undo</a>' % (int(dive_id), undo_url))
    return redirect('divelog.views.dive_list')

@login_required
@never_cache
def dive_restore(request, dive_id):
    try:
        dive = Dive.objects.get(pk = dive_id)
    except Dive.DoesNotExist:
        raise Http404
    
    # Prevent deleting other people's dives
    if dive.user != request.user:
        raise Http404
    
    # Change status to Active
    dive.status = 'A'
    dive.save()
    
    messages.success(request, 'Dive #%d restored' % int(dive_id))
    return redirect('divelog.views.dive_list')

@login_required
@never_cache
def dive_add(request):
    """
    View for adding a new dive.
    """
    if request.method == 'POST':
        form = DiveForm(request.POST)
        form.instance.user = request.user
        form.instance.number = 1
        form.instance.size = 0
 
        if form.is_valid():
            new_dive = form.save()
            messages.success(request, "New dive added.")
            return redirect('divelog.views.dive_view', dive_id = new_dive.id)
        else:
            messages.error(request, "Failed saving dive.")
    else:
        form = DiveForm()
    
    t = loader.get_template('divelog/dives/add.html')
    c = RequestContext(request, {
        'form': form,
    });
    return HttpResponse(t.render(c))

@login_required
def dive_samples_json(request, dive_id):
    """
    Returns dive samples in JSON format.
    """
    try:
        dive = Dive.objects.get(pk = dive_id)
    except Dive.DoesNotExist:
        raise Http404
    
    if dive.user != request.user:
        raise Http404
    
    samples = simplejson.dumps([[
        sample.time,
        sample.depth, 
        sample.temperature
    ] for sample in dive.sample_set.all()] )
    
    return HttpResponse(samples, mimetype="application/json")

@login_required
def dive_events_json(request, dive_id):
    """
    Returns dive events in JSON format.
    """
    try:
        dive = Dive.objects.get(pk = dive_id)
    except Dive.DoesNotExist:
        raise Http404
    
    if dive.user != request.user:
        raise Http404
    
    samples = simplejson.dumps([[
        event.time,
        event.text, 
    ] for event in dive.event_set.all()] )
    
    return HttpResponse(samples, mimetype="application/json")

def location_list(request):
    locations = Location.objects.filter(user=request.user)

    t = loader.get_template('divelog/locations/list.html')
    c = RequestContext(request, {
        'locations': locations
    });
    return HttpResponse(t.render(c))

def location_view(request, location_id):
    try:
        location = Location.objects.get(pk = location_id)
    except Location.DoesNotExist:
        raise Http404
    
    if location.user != request.user:
        raise Http404

    t = loader.get_template('divelog/locations/view.html')
    c = RequestContext(request, {
        'location': location
    });
    return HttpResponse(t.render(c))

def location_edit(request, location_id):
    try:
        location = Location.objects.get(pk = location_id)
    except Location.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        form = LocationForm(request.POST, instance = location)
        if form.is_valid():
            form.save()
            return redirect('divelog.views.location_view', location_id = location_id)
    else:
        form = LocationForm(instance = location)
    
    t = loader.get_template('divelog/locations/edit.html')
    c = RequestContext(request, {
        'form': form,
    });
    return HttpResponse(t.render(c))

def settings(request):
    return redirect('divelog.views.settings_account')

@login_required
def settings_account(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your settings have been saved.")
    else:
        form = UserProfileForm(instance=request.user)
    
    t = loader.get_template('divelog/settings/account.html')
    c = RequestContext(request, {
        'form': form,
    });
    return HttpResponse(t.render(c))

@login_required
def settings_password(request):
    if request.method == 'POST':
        form = ValidatingPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed.")
    else:
        form = ValidatingPasswordChangeForm(request.user)
    
    t = loader.get_template('divelog/settings/password.html')
    c = RequestContext(request, {
        'form': form,
    });
    return HttpResponse(t.render(c))


#
# Interesting extened example: http://djangosnippets.org/snippets/1454/
#
class ImportWizard(SessionWizardView):
    
    file_storage = default_storage
    
    def get_template_names(self):
        # use self.steps.current to get current step
        logging.info(self.steps.current)
        logging.info(self.steps.next)
        return 'divelog/wizard/form.html'
    
    def done(self, form_list, **kwargs):
        return render_to_response('divelog/wizard/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

from datetime import timedelta
from divelog.forms import DiveForm, DiveUploadForm
from divelog.models import Dive, DiveUpload, Sample, Event
from divelog.parsers.libdc import parse_short, parse_full
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from django.template.context import RequestContext
from django.utils import timezone
from django.views.decorators.cache import never_cache
from time import mktime
import logging
import os
from django.core.urlresolvers import reverse

def index(request):
    """
    Title page view.
    """
    t = loader.get_template('divelog/index.html')
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
    upload = DiveUpload.objects.get(pk = upload_id)
    file_size = os.path.getsize(upload.data.path)
    
    # Fetch fingerprints of existing user's dives for marking already uploaded dives
    fingerprints = {}
    dives = Dive.objects.filter(user = request.user).values_list('id', 'fingerprint')
    for dive_id, fingerprint in dives:
        fingerprints[fingerprint] = dive_id

    # Parse the XML file
    try:
        overview = parse_short(upload.data.path)
    except Exception:
        messages.error(request, "Uploaded data cannot be parsed.")
        overview = []
    
    # Add dive_id for existing dives
    for item in overview:
        if item['fingerprint'] in fingerprints:
            item['dive_id'] = fingerprints[item['fingerprint']]
    
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
        
        # Provided fingerprints identify dives which should be imported
        fingerprints = request.POST.getlist('fingerprints')
        upload_id = request.POST.get('upload_id')
        
        try:
            upload = DiveUpload.objects.get(pk = upload_id)
            logging.debug("Parsing dives from upload #%d" % int(upload_id))

            # TODO: Parse only requested files 
            dives = parse_full(upload.data.path)
            logging.debug("Parsed %d dives" % len(dives))            

            count = 0
            for dive, samples, events in dives:
                if dive.fingerprint in fingerprints:
                    _save_dive(request.user, dive, samples, events)
                    count += 1
            
            logging.info("Saved %d dives" % count)
            messages.success(request, "Successfully imported %d dives." % count)
            return redirect('divelog.views.dive_list')
            
        except Exception as ex:
            logging.error(ex)
            messages.error(request, "Import failed")
        
    else:
        messages.error(request, 'Import failed')
        
    t = loader.get_template('divelog/uploads/import.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

@transaction.commit_on_success
def _save_dive(user, dive, samples, events):
    logging.info("Saving dive %s" % dive.fingerprint)
    
    dive.user = user
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
    
    # Find next and previous dives
    next = Dive.objects.filter(date_time__gt = dive.date_time).order_by('date_time')[0:1]
    prev = Dive.objects.filter(date_time__lt = dive.date_time).order_by('-date_time')[0:1]
    
    next_id = next[0].id if next else None
    prev_id = prev[0].id if prev else None

    logging.debug(next)
    logging.debug(prev) 
    
    # Prepare chart data
    chart = {
        'depth': [],
        'temperature': [],
        'events': []
    }
    
    last_temp = None
    
    for sample in dive.sample_set.all():
        delta = timedelta(seconds = sample.time)
        sample_time = dive.date_time + delta
        sample_ts = int(1000 * mktime(sample_time.timetuple()))
        
        if sample.temperature:
            last_temp = sample.temperature
        
        chart['depth'].append([sample_ts, sample.depth])
        chart['temperature'].append([sample_ts, last_temp])
        
    for event in dive.event_set.all():
        delta = timedelta(seconds = event.time)
        event_time = dive.date_time + delta
        chart['events'].append({
            'x': int(1000 * mktime(event_time.timetuple())),
            'title': event.text
        })
    
    t = loader.get_template('divelog/dives/view.html')
    c = RequestContext(request, {
        'dive': dive,
        'chart': chart,
        'next': next_id,
        'prev': prev_id
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
    dive_url = '/dive/%d' % int(dive_id)
    
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
        'dive_url': dive_url,
    });
    return HttpResponse(t.render(c))

@login_required
@never_cache
def dive_defunct(request, dive_id):
    """
    Defuncts a dive (changes dive status to D).
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
    
    undo_url = reverse('divelog.views.dive_activate', args=[dive_id])
    messages.success(request, 'Dive #%d moved to trash. <a href="%s">Undo</a>' % (int(dive_id), undo_url))
    return redirect('divelog.views.dive_list')

@login_required
@never_cache
def dive_activate(request, dive_id):
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
def profile(request):
    """
    Displays user's profile.
    """
    t = loader.get_template('accounts/profile.html')
    c = RequestContext(request);
    return HttpResponse(t.render(c))

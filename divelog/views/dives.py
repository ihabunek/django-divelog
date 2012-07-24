from divelog.forms import DiveForm
from divelog.models import Dive
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.template import loader
from django.template.context import RequestContext
from django.utils import simplejson
from django.views.decorators.cache import never_cache

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
            return redirect('divelog_dive_view', dive_id = dive_id)
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
    
    dive.trash()
    
    undo_url = reverse('divelog_dive_restore', args=[dive_id])
    messages.success(request, 'Dive #%d moved to trash. <a href="%s">Undo</a>' % (int(dive_id), undo_url))
    return redirect('divelog_dive_list')

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
    
    dive.restore()
    
    messages.success(request, 'Dive #%d restored' % int(dive_id))
    return redirect('divelog_dive_list')

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
            return redirect('divelog_dive_view', dive_id = new_dive.id)
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

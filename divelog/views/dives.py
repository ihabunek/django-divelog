from divelog.forms import DiveForm
from divelog.models import Dive, dive_stats
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template import loader
from django.template.context import RequestContext
from django.views.decorators.cache import never_cache
import json
from django.utils.log import getLogger
from logging import getLoggerClass

@login_required
def dive_view(request, dive_id):
    """
    Displays a single dive.
    """
    dive = get_object_or_404(Dive, pk=dive_id, user=request.user)

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
    dive = get_object_or_404(Dive, pk=dive_id, user=request.user)

    # Fetch existing buddies & divemasters for auto-completion
    buddies = Dive.objects.filter(user=request.user).exclude(buddy='').values_list('buddy', flat=True).order_by('buddy').distinct()
    divemasters = Dive.objects.filter(user=request.user).exclude(divemaster='').values_list('divemaster', flat=True).order_by('divemaster').distinct()

    if request.method == 'POST':
        form = DiveForm(request.POST, instance=dive)
        if form.is_valid():
            form.save()
            return redirect('divelog_dive_view', dive_id = dive_id)
    else:
        form = DiveForm(instance=dive)

    t = loader.get_template('divelog/dives/edit.html')
    c = RequestContext(request, {
        'form': form,
        'buddies': list(buddies),
        'divemasters': list(divemasters),
    });
    return HttpResponse(t.render(c))

@login_required
@never_cache
def dive_trash(request, dive_id):
    """
    Moves a dive to trash (changes dive status to D).
    """
    dive = get_object_or_404(Dive, pk=dive_id, user=request.user)
    dive.trash()

    undo_url = reverse('divelog_dive_restore', args=[dive_id])
    messages.success(request, 'Dive #%d moved to trash. <a href="%s">Undo</a>' % (int(dive_id), undo_url))
    return redirect('divelog_dive_list')

@login_required
@never_cache
def dive_restore(request, dive_id):
    dive = get_object_or_404(Dive, pk=dive_id, user=request.user)
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
    dive = get_object_or_404(Dive, pk=dive_id, user=request.user)

    samples = json.dumps([[
        sample.time,
        sample.depth,
        sample.temperature,
        sample.pressure
    ] for sample in dive.sample_set.all()] )

    return HttpResponse(samples, mimetype="application/json")

@login_required
def dive_events_json(request, dive_id):
    """
    Returns dive events in JSON format.
    """
    dive = get_object_or_404(Dive, pk=dive_id, user=request.user)

    samples = json.dumps([[
        event.time,
        event.text,
    ] for event in dive.event_set.all()] )

    return HttpResponse(samples, mimetype="application/json")

@login_required
def dive_stats_json(request, dive_id):
    stats = json.dumps(dive_stats(dive_id))
    return HttpResponse(stats, mimetype="application/json")

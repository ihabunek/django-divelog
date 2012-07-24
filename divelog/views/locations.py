from divelog.forms import LocationForm
from divelog.models import Location
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from django.template.context import RequestContext
from django.views.decorators.cache import never_cache

@login_required
def location_list(request):
    locations = Location.objects.filter(user=request.user)

    t = loader.get_template('divelog/locations/list.html')
    c = RequestContext(request, {
        'locations': locations
    });
    return HttpResponse(t.render(c))

@login_required
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

@login_required
@never_cache
def location_edit(request, location_id):
    try:
        location = Location.objects.get(pk = location_id)
    except Location.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        form = LocationForm(request.POST, instance = location)
        if form.is_valid():
            form.save()
            return redirect('divelog_location_view', location_id = location_id)
    else:
        form = LocationForm(instance = location)
    
    t = loader.get_template('divelog/locations/edit.html')
    c = RequestContext(request, {
        'form': form,
    });
    return HttpResponse(t.render(c))
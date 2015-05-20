from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from event.forms import EventForm
from event.services import *

@login_required
def create(request):

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('event:list'))
        else:
            return render(request, 'event/create.html', {'form' : form,})
    else:
        form = EventForm()
        return render(request, 'event/create.html', {'form' : form,})

@login_required
def delete(request, event_id):

    if request.method == 'POST':
        result = delete_event(event_id)
        if result:
            return HttpResponseRedirect(reverse('event:list'))
        else:
            return render(request, 'event/delete_error.html')
    return render(request, 'event/delete.html', {'event_id' : event_id})

@login_required
def edit(request, event_id):

    event = None
    if event_id:
        event = get_event_by_id(event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('event:list'))
        else:
            return render(request, 'event/edit.html', {'form' : form,})
    else:
        form = EventForm(instance=event)
        return render(request, 'event/edit.html', {'form' : form,})

@login_required
def list(request):
    event_list = get_events_ordered_by_name()
    return render(request, 'event/list.html', {'event_list' : event_list})

@login_required
def list_sign_up(request, volunteer_id):
    event_list = get_events_ordered_by_name()
    return render(request, 'event/list_sign_up.html', {'event_list' : event_list, 'volunteer_id' : volunteer_id})

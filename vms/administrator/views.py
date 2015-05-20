from administrator.forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from shift.services import *

@login_required
def report(request):

    user = request.user
    admin = None
    try:
        admin = user.administrator
    except ObjectDoesNotExist:
        pass
    if not admin:
        return HttpResponse(status=403)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            organization = form.cleaned_data['organization']
            event_name = form.cleaned_data['event_name']
            job_name = form.cleaned_data['job_name']
            date = form.cleaned_data['date']
            report_list = get_administrator_report(first_name, last_name, organization, event_name, job_name, date)
            total_hours = calculate_total_report_hours(report_list)
            return render(request, 'administrator/report.html', {'form' : form, 'report_list' : report_list, 'total_hours' : total_hours, 'notification' : True})
        else:
            return render(request, 'administrator/report.html', {'form' : form, 'notification' : False})
    else:
        form = ReportForm()
        return render(request, 'administrator/report.html', {'form' : form, 'notification' : False})

@login_required
def settings(request):

    user = request.user
    admin = None
    try:
        admin = user.administrator
    except ObjectDoesNotExist:
        pass
    if not admin:
        return HttpResponse(status=403)

    return HttpResponseRedirect(reverse('event:list'))

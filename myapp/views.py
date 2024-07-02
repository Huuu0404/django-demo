from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Event
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myapp.models import Event, ShowInfo, Location
from django.views.decorators.csrf import csrf_exempt


def home(request):
    events_list = Event.objects.all()
    paginator = Paginator(events_list, 10)  # Show 10 events per page

    page_number = request.GET.get('page')
    try:
        events = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)

    context = {
        'events': events,
        'user': request.user,  # Assuming you want to pass the user to the template
    }
    return render(request, 'home.html', context)

@csrf_exempt 
def operation_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        event_id = request.POST.get('id')
        event = get_object_or_404(Event, id=event_id)

        if request.user.is_authenticated:
            if action == 'detail':
                return redirect('event_detail', id=event_id)

            elif action == 'edit':
                event.title = request.POST.get('title')
                event.category = request.POST.get('category')
                event.startDate = request.POST.get('startDate')
                event.endDate = request.POST.get('endDate')
                event.description = request.POST.get('description')
                event.save()
                return redirect('home')

            elif action == 'delete':
                event.delete()
                return redirect('home')
        
        return redirect('login')

    elif request.method == 'GET':
        search_query = request.GET.get('search')
        if search_query and search_query.strip():
            events = Event.objects.filter(title__icontains=search_query)
        else:
            events = Event.objects.all()

        context = {
            'events': events
        }
        return render(request, 'home.html', context)

    return HttpResponse(status=405)

@login_required
def edit(request, id):
    event = get_object_or_404(Event, id=id)
    context = {
        'event': event
    }
    return render(request, 'edit.html', context)

@login_required
def detail(request, id):
    event = get_object_or_404(Event, id=id)
    show_infos = ShowInfo.objects.filter(event=event)
    context = {
        'event': event,
        'show_infos': show_infos
    }
    return render(request, 'detail.html', context)
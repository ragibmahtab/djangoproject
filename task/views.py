from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from task.forms import eventform,catagoryform
from task.models import event,catagory
from datetime import date
from django.db.models import Q,Count,Min,Max
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Create your views here.

def Homepage(request):
    events=event.objects.select_related("catagory").all()
    context={
        "events":events
    }

    return render(request,"homepage.html",context)


def detail_View(request,id):
    events=event.objects.select_related("catagory").get(id=id)
    countt=events.participents.count()

    context={
        "events":events,
        "countt":countt
    }

    return render(request,"detail_view.html",context)








def Dashboard(request):
    type=request.GET.get("type")

    events=event.objects.select_related("catagory").all()
    
    count_event=events.aggregate(
        total=Count('id'),
        upcoming=Count('id',filter=Q(date__gt=date.today())),
        past=Count('id',filter=Q(date__lt=date.today())),
        todays=Count('id',filter=Q(date=date.today())),
    )
    # countt=participant.objects.aggregate(total=Count('id'))


    if type=='UPcoming Events':
        events=events.filter(date__gt=date.today())
    elif type=='Past Events':
        events=events.filter(date__lt=date.today())
    elif type=='Todays Events':
        events=events.filter(date=date.today())
    elif type=='Total Events':
        events=events.all()
    
    context={
        "events":events,
        "counts":count_event,
        # "countt":countt,
        
    }
    return render(request,"dashboard.html",context)



@login_required
@role_required("Organizer")
def create_event(request):
    form=eventform()

    if request.method =="POST":
        form=eventform(request.POST)
        if form.is_valid():
            form.save()

            return render(request, 'event_form.html', {"form": form, "message": "...EVENT ADDED SUCCESSFULLY..."})
    


    context={"form":form}

    return render(request,"event_form.html",context)

@login_required
@role_required("Organizer")
def update_event(request,id):
    ev=event.objects.select_related("catagory").get(id=id)
    form=eventform(instance=ev)

    if request.method =="POST":
        form=eventform(request.POST,instance=ev)
        if form.is_valid():
            form.save()

            messages.success(request, "EVENT UPDATED SUCCESSFULLY")
            return redirect('update_event', id=id)

    context={"form":form}

    return render(request,"event_form.html",context)

@login_required
@role_required("Organizer")
def delete_event(request,id):
    if request.method=='POST':
        ev=event.objects.select_related("catagory").get(id=id)
        ev.delete()
        messages.success(request, "EVENT DELETED SUCCESSFULLY")
        return redirect('homepage')
    else:
        messages.error(request, "SOMETHING WENT WRONG")
        return redirect('homepage')



# def create_participant(request):
#     form=participantform()

#     if request.method =="POST":
#         form=participantform(request.POST)
#         if form.is_valid():
#             form.save()

#             return render(request, 'event_form.html', {"form": form, "message": "...PARTICIPANT ADDED SUCCESSFULLY..."})
    


#     context={"form":form}

#     return render(request,"event_form.html",context)


    # context={"form":form}

    # return render(request,"event_form.html",context)


@login_required
@role_required("Organizer")
def create_catagory(request):
    form=catagoryform()

    if request.method =="POST":
        form=catagoryform(request.POST)
        if form.is_valid():
            form.save()

            return render(request, 'event_form.html', {"form": form, "message": "...CATAGORY ADDED SUCCESSFULLY..."})
    


    context={"form":form}

    return render(request,"event_form.html",context)

@login_required
@role_required("Organizer")
def update_catagory(request,id):
    ev=event.objects.select_related("catagory").prefetch_related("participents").get(id=id)

    form=catagoryform(instance=ev)

    if request.method =="POST":
        form=catagoryform(request.POST,instance=ev)
        if form.is_valid():
            form.save()
            messages.success(request, "CATAGORY UPDATED SUCCESSFULLY")
            return redirect('update_catagory', id=id)

            
    


    context={"form":form}

    return render(request,"event_form.html",context)


def search(request):
    query=request.GET.get('q')
    eventss=[]
    if query:
        eventss=event.objects.filter(Q(name__icontains=query)| Q(location__icontains=query))

    return render(request,"search.html",{"eventss":eventss,"query": query})

@login_required
def event_detail(request, id):
    event_obj = get_object_or_404(event, id=id)

    context = {
        "event": event_obj
    }

    return render(request, "event_detail.html", context)






@login_required
@role_required("Admin")
def admin_dashboard(request):
    return render(request,"admin_dashboard.html",{
        "events":event.objects.all(),
        "users":User.objects.all(),
        "categories":catagory.objects.all()
    })

@login_required
@role_required("Organizer")
def organizer_dashboard(request):
    return render(request,"organizer_dashboard.html",{
        "events":event.objects.all(),
        "categories":catagory.objects.all()
    })

@login_required
@role_required("Participant")
def participant_dashboard(request):
    return render(request,"participant_dashboard.html",{
        "events":request.user.rsvp_events.all()
    })


@login_required
@role_required("Participant")
def rsvp_event(request,id):
    ev=event.objects.get(id=id)

    if request.user not in ev.rsvp_users.all():
        ev.rsvp_users.add(request.user)

        send_mail(
            "RSVP Confirmation",
            f"You successfully RSVP’d for {ev.name}",
            "admin@example.com",
            [request.user.email],
        )

    return redirect("participant_dashboard")

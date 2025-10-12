from django.shortcuts import render,redirect
from django.http import HttpResponse
from task.forms import eventform,participantform,catagoryform
from task.models import participant,event,catagory
from datetime import date
from django.db.models import Q,Count,Min,Max
from django.contrib import messages
# Create your views here.

def Homepage(request):
    events=event.objects.select_related("catagory").prefetch_related("participents").all()
    context={
        "events":events
    }

    return render(request,"homepage.html",context)


def detail_View(request,id):
    events=event.objects.select_related("catagory").prefetch_related("participents").get(id=id)
    countt=events.participents.count()

    context={
        "events":events,
        "countt":countt
    }

    return render(request,"detail_view.html",context)








def Dashboard(request):
    type=request.GET.get("type")

    events=event.objects.select_related("catagory").prefetch_related("participents")
    
    count_event=events.aggregate(
        total=Count('id'),
        upcoming=Count('id',filter=Q(date__gte=date.today())),
        past=Count('id',filter=Q(date__lt=date.today())),
        todays=Count('id',filter=Q(date=date.today())),
    )
    countt=participant.objects.aggregate(total=Count('id'))


    if type=='UPcoming Events':
        events=events.filter(date__gte=date.today())
    elif type=='Past Events':
        events=events.filter(date__lt=date.today())
    elif type=='Todays Events':
        events=events.filter(date=date.today())
    elif type=='Total Events':
        events=events.all()
    
    context={
        "events":events,
        "counts":count_event,
        "countt":countt,
        
    }
    return render(request,"dashboard.html",context)




def create_event(request):
    form=eventform()

    if request.method =="POST":
        form=eventform(request.POST)
        if form.is_valid():
            form.save()

            return render(request, 'event_form.html', {"form": form, "message": "...EVENT ADDED SUCCESSFULLY..."})
    


    context={"form":form}

    return render(request,"event_form.html",context)


def update_event(request,id):
    ev=event.objects.select_related("catagory").prefetch_related("participents").get(id=id)
    form=eventform(instance=ev)

    if request.method =="POST":
        form=eventform(request.POST,instance=ev)
        if form.is_valid():
            form.save()

            messages.success(request, "EVENT UPDATED SUCCESSFULLY")
            return redirect('update_event', id=id)

    context={"form":form}

    return render(request,"event_form.html",context)


def delete_event(request,id):
    if request.method=='POST':
        ev=event.objects.select_related("catagory").prefetch_related("participents").get(id=id)
        ev.delete()
        messages.success(request, "EVENT DELETED SUCCESSFULLY")
        return redirect('homepage')
    else:
        messages.error(request, "SOMETHING WENT WRONG")
        return redirect('homepage')



def create_participant(request):
    form=participantform()

    if request.method =="POST":
        form=participantform(request.POST)
        if form.is_valid():
            form.save()

            return render(request, 'event_form.html', {"form": form, "message": "...PARTICIPANT ADDED SUCCESSFULLY..."})
    


    context={"form":form}

    return render(request,"event_form.html",context)





    


    context={"form":form}

    return render(request,"event_form.html",context)



def create_catagory(request):
    form=catagoryform()

    if request.method =="POST":
        form=catagoryform(request.POST)
        if form.is_valid():
            form.save()

            return render(request, 'event_form.html', {"form": form, "message": "...CATAGORY ADDED SUCCESSFULLY..."})
    


    context={"form":form}

    return render(request,"event_form.html",context)


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




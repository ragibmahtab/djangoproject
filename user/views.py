from django.shortcuts import render
from user.form import customregistrationform

# Create your views here.
def sign_up(request):
    form = customregistrationform()
    if request.method == 'POST':
        form = customregistrationform(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid")
    return render(request, 'registration.html', {"form": form})
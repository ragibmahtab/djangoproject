from django import forms
from task.models import event,participant,catagory

class eventform(forms.ModelForm):
    class Meta:
        model=event
        fields="__all__"
        widgets={
            'name':forms.TextInput(attrs={
                'class':"border-2 border-solid  border-slate-700 inset-shadow-lg inset-shadow-amber-600 rounded-2xl "
                "w-full h-full px-4",
                'placeholder':"Enter Event Name"
            }),

             'description':forms.Textarea(attrs={
                'class':"border-2 border-solid  border-slate-700 inset-shadow-lg inset-shadow-amber-600 rounded-2xl "
                "w-full h-full  px-4 ",
                'placeholder':"Enter Event Description "
            }),

            "date":forms.SelectDateWidget(attrs={
                'class':"border-2 border-solid  border-slate-700 inset-shadow-lg inset-shadow-amber-600 rounded-2xl "
            }),

            "time":forms.TimeInput(attrs={
                
                'class':"border-2 border-solid  border-slate-700 inset-shadow-lg "
                "inset-shadow-amber-600 rounded-2xl my-4 h-full  px-4",
                'placeholder':"HOUR:MINUTE"
            }),


            'location':forms.TimeInput(attrs={
                'class':"border-2 border-solid  border-slate-700 inset-shadow-lg inset-shadow-amber-600 rounded-2xl "
                "h-full  px-4 ",
                'placeholder':"Enter Event Location "
            }),


            'catagory':forms.Select(attrs={
               'class':"border-2 border-solid  border-slate-700 my-4",
           })     

                  

        }

class participantform(forms.ModelForm):
    class Meta:
        model=participant
        fields="__all__"
        widgets={
            'name':forms.TextInput(attrs={
                'class':"border-2 border-solid  border-slate-700 inset-shadow-lg inset-shadow-amber-600 rounded-2xl "
                "w-full h-full px-4 ",
                'placeholder':"Enter Participant Name"
            }),
            'email':forms.TextInput(attrs={
                'class':"border-2 border-solid  border-slate-700 inset-shadow-lg inset-shadow-amber-600 rounded-2xl "
                "w-full h-full px-4 mb-4",
                'placeholder':"Enter Email",
            }),
            'participated_event':forms.CheckboxSelectMultiple(attrs={
               'class':"border-2 border-solid  border-slate-700 px-2 w-4 h-4 inline-block mr-2",
        
           })     

        }













class catagoryform(forms.ModelForm):
    class Meta:
        model=catagory
        fields="__all__"
        widgets={
            'name':forms.TextInput(attrs={
                'class':"border-2 border-solid  border-slate-700 inset-shadow-lg inset-shadow-amber-600 rounded-2xl "
                "w-full h-full px-4 ",
                'placeholder':"Enter Catagory Name"
            }),
            'description':forms.Textarea(attrs={
                'class':"border-2 border-solid  border-slate-700 inset-shadow-lg inset-shadow-amber-600 rounded-2xl "
                "w-full h-full  px-4 ",
                'placeholder':"Enter Catagory Description "
            }),

        }

       

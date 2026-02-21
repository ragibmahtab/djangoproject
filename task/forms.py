from django import forms
from task.models import event,catagory



class StyledFormMixin:
    """ Mixing to apply style to form field"""

    def __init__(self,*arg,**kwarg):
        super().__init__(*arg,**kwarg)
        self.apply_styled_widgets()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })



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

# class participantform(forms.ModelForm):
#     class Meta:
#         model=participant
#         fields="__all__"
#         widgets={
#             'name':forms.TextInput(attrs={
#                 'class':"border-2 border-solid  border-slate-700 inset-shadow-lg inset-shadow-amber-600 rounded-2xl "
#                 "w-full h-full px-4 ",
#                 'placeholder':"Enter Participant Name"
#             }),
#             'email':forms.TextInput(attrs={
#                 'class':"border-2 border-solid  border-slate-700 inset-shadow-lg inset-shadow-amber-600 rounded-2xl "
#                 "w-full h-full px-4 mb-4",
#                 'placeholder':"Enter Email",
#             }),
#             'participated_event':forms.CheckboxSelectMultiple(attrs={
#                'class':"border-2 border-solid  border-slate-700 px-2 w-4 h-4 inline-block mr-2",
        
#            })     

#         }













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

       

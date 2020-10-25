from django import forms 
from .models import Panel , Szkolenie
class DateInput(forms.DateInput):
    input_type = 'date'
    format_key = 'DATE_INPUT_FORMATS'

class userslist (forms.ModelForm):
    #DateTraining = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))#
    class Meta:
        required_css_class = 'required'
        model = Panel
        
        fields = "__all__"

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice'].widget.attrs.update({'onchange' : "onCheckboxChanged(this.checked);"})
        self.fields['statement'].widget.attrs.update({'onchange' : "showcost(this.checked);"})
        self.fields['NewTraining'].widget.attrs.update({'onchange' : "getSelectValue();"})

        make_list = [i.NewTraining for i in Szkolenie.objects.all() if i.max_participants > Panel.objects.filter(NewTraining = i.id).count()]

        self.fields['NewTraining'].queryset = Szkolenie.objects.filter(NewTraining__in = make_list)

    def clean(self):

        cleaned_data = super().clean()
        name_user = cleaned_data.get("name_user")
        subname = cleaned_data.get("subname")
        email = cleaned_data.get("email_user")
        phoneNumber = cleaned_data.get("phoneNumber")
        invoice = cleaned_data.get("invoice")
        name_company = cleaned_data.get("name_company")
        full_name_company = cleaned_data.get("full_name_company")
        NIP = cleaned_data.get("NIP")
        street = cleaned_data.get("street")
        zip = cleaned_data.get("zip")
        if invoice:
            if full_name_company == None or name_company == None or NIP == None or street == None or zip == None :
                msg = "podaj dane firmy"
                self.add_error('invoice', msg)

class Szkolenielist (forms.ModelForm):
    class Meta:
        required_css_class = 'required'
        model = Szkolenie
        fields = "__all__"

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['NewTraining'].widget.attrs.update({'placeholder':'Szkolenie'})
        self.fields['DateTraining'].widget.attrs.update({'placeholder':'Data Szkolenia'})
        self.fields['Provider'].widget.attrs.update({'placeholder':'Prowadzący Szkolenie'})
        self.fields['max_participants'].widget.attrs.update({'placeholder':'Max.ilość uczestników'})


              
            
            
    

        
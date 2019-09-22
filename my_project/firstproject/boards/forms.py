from django import forms
from .models import Topic,Post
from django.core import validators



class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'row': 5,
        'placeholder':'what is your message '}),
        max_length= 5000,
        help_text=" Max length is 5000")
    class Meta:
        model = Topic
        fields = ['subject','message']
    #def clean_message(self):
     #   msg = self.cleaned_data.get('message')
     #   if not "ss" in msg:
     #       raise forms.ValidationError("no No ")
     #   return msg

class Postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']

    #def clean_dd(self):
     #   subject = self.cleaned_data.get('message')
     #   if not "faisal" in subject:
     #       raise forms.ValidationError("sorry where is faisal ")
     #   return subject
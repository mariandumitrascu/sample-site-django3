

from django import forms


# reference:
# https://docs.djangoproject.com/en/dev/topics/forms/

class NameForm(forms.Form):
    your_name = forms.CharField(
        label='Your name',
        max_length=100,
        )



class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)

    message = forms.CharField(
        widget=forms.Textarea
        )

    sender = forms.EmailField()

    cc_myself = forms.BooleanField(required=False)

######################################################################################################################
# reference:
# https://docs.djangoproject.com/en/dev/topics/forms/formsets/

from django.forms import formset_factory

class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()


ArticleFormSet = formset_factory(ArticleForm, extra=2)
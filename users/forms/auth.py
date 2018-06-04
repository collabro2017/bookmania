from django import forms
from users.models import User
from publisher.models import Publisher

from django.contrib.auth.forms import UserCreationForm


'''
class PublisherCreationForm(UserCreationForm):
    publisher_name = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
'''

class PublisherCreationForm(forms.ModelForm):
    publisher = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", )

    def clean_publisher(self):
        publisher = self.cleaned_data.get('publisher')
        if Publisher.objects.filter(name=publisher).exists():
            raise forms.ValidationError(
                'Publisher already exists',
                code='publisher_already_exists',
            )
        return publisher

    def save(self, commit=True):
        publisher = Publisher.objects.create(name=self.cleaned_data["publisher"])

        user = super(PublisherCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.publisher = publisher
        user.set_password(self.cleaned_data["password"])
        user.save()

        return user

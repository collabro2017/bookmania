from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from users.models import User
from django.views import View
from users.forms.auth import PublisherCreationForm


@login_required
def login_complete(request):
    if request.user.user_type == User.PUBLISHER or request.user.user_type == User.STAFF:
        return redirect('publisher_dashboard')
    else:
        return redirect('/')


class Register(View):

    def get(self, request):
        form = PublisherCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = PublisherCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            error = form.errors.values()[0]
            return render(request, 'registration/register.html', {'form': form, 'error': error})

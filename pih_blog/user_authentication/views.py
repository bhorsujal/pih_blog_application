from django.shortcuts import render, redirect
from django.contrib import messages
from .form_updation import UserRegistrationForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!, Logged in!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'user_authentication/registration.html', {'form': form})


@login_required
def user_profile(request):
    return render(request, 'user_authentication/user_profile.html')
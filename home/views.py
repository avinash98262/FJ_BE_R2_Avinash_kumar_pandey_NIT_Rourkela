from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import *


@login_required
def home(request):
    profile = Profile.objects.filter(user=request.user).first()
    expenses = Expense.objects.filter(user=request.user)

    if request.method == 'POST':
        text = request.POST.get('text')
        amount = request.POST.get('amount')
        expense_type = request.POST.get('expense_type')

        expense = Expense(name=text, amount=amount, expense_type=expense_type, user=request.user)
        expense.save()

        if expense_type == 'Positive':
            profile.balance += float(amount)
        else:
            profile.expenses += float(amount)
            profile.balance -= float(amount)

        profile.save()
        return redirect('home')

    # Prepare data for the chart
    expense_types = ['Positive', 'Negative']
    expense_amounts = [profile.balance, profile.expenses]

    context = {
        'profile': profile,
        'expenses': expenses,
        'expense_types': expense_types,
        'expense_amounts': expense_amounts,
    }
    return render(request, 'home.html', context)


def register_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('register_page')

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create a Profile object for the new user
        profile = Profile(user=user, balance=0, expenses=0)  # You can set initial balance and expenses as needed
        profile.save()

        # Log in the user after registration
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')  # Replace 'home' with the URL name of your home page

    return render(request, 'register.html')







def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')  # Replace 'home' with the URL name of your home page
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')

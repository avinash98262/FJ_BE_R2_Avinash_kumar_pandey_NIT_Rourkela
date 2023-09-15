from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile, Expense

from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Profile
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_user(request):
    logout(request)
    return redirect('login_page')  # Redirect to your login page name (adjust as needed)


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Get the original amount and type of the expense
        original_amount = expense.amount
        original_type = expense.expense_type

        # Update the expense fields
        expense.name = request.POST['text']
        new_amount = float(request.POST['amount'])
        new_type = request.POST['expense_type']
        expense.amount = new_amount
        expense.expense_type = new_type
        expense.save()

        # Calculate the change in balance and expenses
        if original_type == 'Positive':
            # The original expense increased the balance
            profile.balance -= original_amount
        else:
            # The original expense increased the expenses
            profile.expenses -= original_amount

        if new_type == 'Positive':
            # The updated expense increases the balance
            profile.balance += new_amount
        else:
            # The updated expense increases the expenses
            profile.expenses += new_amount

        # Save the profile
        profile.save()

        # Redirect back to the home page or wherever you want
        return redirect('home')

    # Render the edit expense form
    context = {'expense': expense}
    return render(request, 'edit_expense.html', context)



@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        # Handle the form submission for deleting the expense
        expense.delete()

        # Redirect back to the home page or wherever you want
        return redirect('home')

    # Render the delete expense confirmation page
    context = {'expense': expense}
    return render(request, 'delete_expense.html', context)

@login_required
def home(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # If the profile does not exist for the user, create one with default values
        profile = Profile(user=request.user, balance=0, expenses=0, income=0)
        profile.save()

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

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('register_page')

        user = User.objects.create_user(username=username, email=email, password=password)

        if user is not None:
            # Check if a Profile object already exists for the user
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                # If no profile exists, create one
                profile = Profile(user=user, balance=0, expenses=0, income=0)
                profile.save()

            # Log in the user after registration
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful. You are now logged in.')
                return redirect('home')

    return render(request, 'register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')

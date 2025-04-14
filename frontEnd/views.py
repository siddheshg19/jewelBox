from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from frontEnd.forms import SignupForm
from jewelBoxDbServices.models import Jewelry,Order, CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.db import transaction

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]


        user = authenticate(request, username=email, password=password)

        if user:
            auth_login(request, user)  
            request.session["user_id"] = user.id  
            request.session["user_name"] = user.first_name
            
            messages.success(request, "Login successful!")
            return redirect("jewelry_list")
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, "Signup successful! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

def logout(request):
    auth_logout(request)  # Logs out the user
    request.session.flush()  # Clear session data
    messages.success(request, "You have been logged out.")
    return redirect("home")


@login_required
def jewelry_list(request):
    category = request.GET.get("category")  # Get category from request parameters

    if category:
        jewelry_items = Jewelry.objects.filter(category=category)  # Filter by category
    else:
        jewelry_items = Jewelry.objects.all().order_by("category")  # Default order

    return render(request, "jewelry_list.html", {"jewelry_items": jewelry_items})

@login_required
def order_jewelry(request, jewelry_id):
    jewelry = get_object_or_404(Jewelry, id=jewelry_id)

    if request.method == "POST":
        customer_instance = get_object_or_404(CustomUser, id=request.session.get("user_id"))
        
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0 or quantity > jewelry.stock:
            messages.error(request, "Invalid quantity selected.")
            return redirect("order_jewelry", jewelry_id=jewelry.id)

        total_price = jewelry.price * quantity

        order = Order.objects.create(
            user=customer_instance,
            jewelry=jewelry,
            quantity=quantity,
            total_price=total_price
        )
        order.save()

        # Reduce stock after ordering
        jewelry.stock -= quantity
        jewelry.save()

        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'order_jewelry.html', {'jewelry': jewelry})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})


@login_required
def my_orders(request):
    """Displays the logged-in user's order history."""

    user = request.user  

    orders = Order.objects.filter(user=user).order_by('-order_date') 

    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    """Handles the cancellation of an order (by DELETING it) and adds back the stock."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'Pending':
        with transaction.atomic():  
            jewelry = order.jewelry
            jewelry.stock += order.quantity  
            jewelry.save() 

            order.delete()  
        messages.success(request, f"Order #{order.id} has been deleted, and stock has been updated.")

    else:
        messages.error(request, "You can only delete orders that are in 'Pending' status.")

    return redirect('my_orders')





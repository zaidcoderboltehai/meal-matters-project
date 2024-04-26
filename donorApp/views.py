from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import *
from foodsorterlib.foodsorter import sort_foods_by_date

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'please enter valid email and password')
            return render(request,"login.html")
    else:
        return render(request,"login.html")
    

def singup(request):
    if request.method=="POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        return redirect("/")
    else:
        return render(request,"singup.html")
    
def home(request):
    if request.user.is_staff:
        return redirect("/food-list")
    else:
        return redirect("/user-food-list")
    
def foodList(request):
    foods=Food.objects.filter(donor=request.user)
    return render(request,"foodlist.html",{"foods":foods})

def userLogout(request):
    logout(request)
    return redirect("/")

def addFood(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        expiry_date = request.POST.get('expiry_date')
        pickup_address = request.POST.get('pickup_address')
        image = request.FILES.get('image')  
        food = Food(name=name, description=description, expiry_date=expiry_date, pickup_address=pickup_address, image=image, donor=request.user)
        food.save()
        return redirect('/food-list')
    else:
        return render(request,"foodform.html")
    
def deleteFood(request,pk):
    food= Food.objects.get(id=pk)
    food.delete()
    return redirect("/food-list")

def editFood(request,pk):
    food = Food.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        expiry_date = request.POST.get('expiry_date')
        pickup_address = request.POST.get('pickup_address')
        image = request.FILES.get('image') 
        food.name = name
        food.description = description
        food.expiry_date = expiry_date
        food.pickup_address = pickup_address
        if image:
            food.image = image    
        food.save()
        return redirect("/food-list")
    else:
        return render(request, 'editfood.html', {'food': food})
    
def userFoodList(request):
    if(not request.user.is_staff):
        foods=Food.objects.all()
        sorting_options = ['All foods', 'Sort by date']
        return render(request,"userfoodlist.html",{"foods":foods,'sorting_options': sorting_options})
    return redirect("/")

def send_request(request,pk):
    user=request.user
    food=Food.objects.get(id=pk)
    reqobj=Request()
    reqobj.user=user
    reqobj.food=food
    reqobj.save()
    return redirect("/myfoodcart")

def myfoodcart(request):
    current_user_requests = Request.objects.filter(user=request.user)
    requested_food_details = []
    for food_request in current_user_requests:  # Rename 'request' variable
        food_item = food_request.food
        status = food_request.status
        requested_food_details.append({'food_item': food_item, 'status': status})
    return render(request, 'userfoodcart.html', {'requested_food_details': requested_food_details})

def donorfoodcart(request):
    donor_foods = Food.objects.filter(donor=request.user)
    pending_requests = Request.objects.filter(food__in=donor_foods, status='pending')
    food_details = [{'food': req.food, 'user_email': req.user.email,"req_id":req.id} for req in pending_requests]
    return render(request, 'donorfoodcart.html', {'food_details': food_details})


def accept_request(request, request_id):
    req = Request.objects.get(id=request_id)
    req.status = 'accepted'
    req.save()
    return redirect('/donorcart')

def reject_request(request, request_id):
    req = Request.objects.get(id=request_id)
    req.status = 'rejected'
    req.save()
    return redirect('/donorcart')

def view_food(request,pk):
    food=Food.objects.get(id=pk)
    return render(request,"viewfood.html",{"food":food})

def sortByDate(request):
    foods = Food.objects.all()
    # Sort the list of food objects by date
    sorted_foods = sort_foods_by_date(foods)
    sorting_options = [ 'Sort by date','All foods']
    return render(request, "userfoodlist.html", {"foods": sorted_foods,'sorting_options': sorting_options})

    
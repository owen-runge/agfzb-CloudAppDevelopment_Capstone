from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, get_request, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html')


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        # Get username and password
        username = request.POST['username']
        password = request.POST['psw']

        # Try authentication
        user = authenticate(username=username, password=password)
        if user is not None:
            # credentials are valid
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # credentials are not valid
            return render(request, 'djangoapp:index.html', context)
    else:
        return render(request, 'djangoapp:index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html')
    elif request.method == "POST":
        # Get user info
        username = request.POST['username']
        password = request.POST['psw']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        exists = False

        try:
            # Check if user already exists
            User.objects.get(username=username)
            exists = True
        except:
            print(f"{username} is a new user")
        
        # If new user
        if not exists:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password)
            # Login the user and redirect to homepage
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/cbe0fb6e-9956-4ee6-94de-4294bb219704/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
#     if request.method == "GET":
#         context = {}
#         url = "https://us-south.functions.appdomain.cloud/api/v1/web/cbe0fb6e-9956-4ee6-94de-4294bb219704/dealership-package/get-review"
#         url2 = "https://us-south.functions.appdomain.cloud/api/v1/web/cbe0fb6e-9956-4ee6-94de-4294bb219704/dealership-package/get-dealership"
#         reviews = get_dealer_reviews_from_cf(url, id=dealer_id)
#         context['reviews'] = reviews
#         dealer = get_dealer_by_id_from_cf(url2, dealer_id)
#         context['dealer'] = dealer
#         return render(request, 'djangoapp/dealer_details.html', context)

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/cbe0fb6e-9956-4ee6-94de-4294bb219704/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=dealer_id)
        context["dealer"] = dealer

        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/cbe0fb6e-9956-4ee6-94de-4294bb219704/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, id=dealer_id)
        print(reviews)
        context["reviews"] = reviews

        # return HttpResponse(reviews)
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/cbe0fb6e-9956-4ee6-94de-4294bb219704/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=dealer_id)
    context['dealer'] = dealer
    if request.method == "GET":
        cars = CarModel.objects.all()
        print(cars)
        context['cars'] = cars

        # return HttpResponse(cars)
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            print("request.POST1: ", request.POST)
            car_id = request.POST["car"]
            print("request.POST2: ", request.POST)
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = dealer_id
            payload["id"] = dealer_id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/cbe0fb6e-9956-4ee6-94de-4294bb219704/dealership-package/post-review"
            post_request(review_post_url, new_payload, id=dealer_id)
        
        # return HttpResponse(new_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


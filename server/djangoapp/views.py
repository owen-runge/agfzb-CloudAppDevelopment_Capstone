from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf
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
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/cbe0fb6e-9956-4ee6-94de-4294bb219704/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/cbe0fb6e-9956-4ee6-94de-4294bb219704/dealership-package/get-review"
        url2 = "https://us-south.functions.appdomain.cloud/api/v1/web/cbe0fb6e-9956-4ee6-94de-4294bb219704/dealership-package/get-dealership"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['reviews'] = reviews
        dealer = get_dealer_by_id_from_cf(url2, dealer_id)
        context['dealer'] = dealer
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...


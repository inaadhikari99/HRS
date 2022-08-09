# Create your views here.
import pandas as pd

from django.db import transaction
import math
from django.http import JsonResponse
from django.views import View
import requests
from .forms import UploadForm, ReviewForm
from .ml import get_recommendation_for_hotel
from .models import Hotel, WishList, Review
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .serializers import HotelSerializer

import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def index(request):
    hotel = Hotel.objects.all()
    return render(request, 'index.html', {'hotels': hotel})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def home(request, page_number):
    page_size = 12
    if page_number < 1:
        page_number = 1
    hotel_count = Hotel.objects.count()

    last_page = math.ceil(hotel_count / page_size)
    pagination = {
        'previous_page': page_number - 1,
        'current_page': page_number,
        'next_page': page_number + 1,
        'last_page': last_page
    }

    # hotel = Hotel.objects.all().order_by('-updated')
    hotel = Hotel.objects.all().order_by('-updated')[(page_number - 1) * page_size:page_number * page_size]

    return render(request, 'index.html', {'hotels': hotel, 'pagination': pagination})


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/page/1')

        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                # cleaned_data returns a validated form inputs fields and their values
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was successfully created for ' + "  " + user)
                # if user is registered redirect to login page
                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def upload_dataset(request):
    file_form = UploadForm()
    error_messages = {}
    if request.method == "POST":
        file_form = UploadForm(request.POST, request.FILES)
        try:
            if file_form.is_valid():
                dataset = pd.read_csv(request.FILES['file'])
                new_hotels_list = []

                with transaction.atomic():
                    for index, row in dataset.iterrows():
                        hotel = Hotel(
                            name=row['name'],
                            price=row['price'],
                            location=row['location'],
                            image=row['image'],
                            cuisine=row['cuisine']

                        )

                        new_hotels_list.append(hotel)

                Hotel.objects.bulk_create(new_hotels_list)
                return redirect('movies/index')

        except Exception as e:
            error_messages['error'] = e

    return render(request, 'upload_dataset.html',
                  {'form': file_form, 'error_messages': error_messages}
                  )


def add_to_favorite(request, id):
    hotel = Hotel.objects.get(id=id)
    hotel.favorite.add(request.user)

    return redirect('/hotels/{0}'.format(id))


def remove_from_favorites(request, id):
    restaurant = Hotel.objects.get(id=id)
    restaurant.favorite.remove(request.user)

    return redirect('/hotels/{0}'.format(id))


def get_user_favorites(request):
    hotels = request.user.favorite.all()
    return render(request, 'user_favourite.html', {'hotel': hotels})


def get_hotel_info(request, id):
    if not request.user.is_authenticated:
        return redirect('/register')
    try:
        review_form = ReviewForm()
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.hotel_id = id
                review.user_id = request.user.id
                review.save()

        hotel = Hotel.objects.get(id=id)
        reviews = Review.objects.filter(hotel=hotel).order_by('created_at')[0:4]
        context = {
            'is_favorite': False
        }
        hotel_ids = get_recommendation_for_hotel(id)

        recommended_hotels = Hotel.objects.filter(id__in=hotel_ids)
        if hotel.favorite.filter(pk=request.user.pk).exists():
            context['is_favorite'] = True
        return render(request, 'hotel_detail.html', {
            'hotel': hotel,
            'context': context,
            'reviews': reviews,
            'review_form': review_form,
            # //LEFT SIDE KO CHAI HTML MA RAKHNE
            'recommended_hotels': recommended_hotels
        })

    except Hotel.DoesNotExist:
        return render(request, '404.html')


# class KhaltiRequestView(View):
#     def get(self, request, *args, **kwargs):
#         # hotel = Hotel.objects.get(price)
#         # context = {
#         #          "hotel": hotel
#         # }
#         return render(request, "khaltirequest.html",{'hotels': hotel})

def KhaltiReq(request, id):
    hotel = Hotel.objects.get(id=id)

    return render(request, "khaltirequest.html", {'hotel': hotel})

def KhaltiVerify(request):
    token = request.GET.get("token")
    amount = request.GET.get("amount")
    book_id = request.GET.get("book_id")

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
        "token": token,
        "amount": amount,
        "book_id":book_id
    }
    headers = {
        "Authorization": "Key test_secret_key_93fad8c9fa8647f7a41b162c32f48f95"
    }

    response = requests.post(url, payload, headers=headers)
    resp_dict = response.json()

    if resp_dict.get('idx'):
        success = True

    else:
        success = False

    data = {
        "success": success
    }
    return JsonResponse(data)
# Create your views here.
import pandas as pd

from django.db import transaction
import math
from django.http import JsonResponse

from .forms import UploadForm
from .ml import get_recommendation_for_hotel
from .models import Hotel, WishList
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
            return redirect('home')

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


def Addwishlist(request):
    hid = request.GET['hotel']
    hotel = Hotel.objects.get(pk=hid)
    data = {}
    checkwishlist = WishList.objects.filter(hotel=hotel,
                                            user=request.user).count()
    if checkwishlist > 0:
        data = {
            'bool': False
        }
    else:

        wishlist = WishList.objects.create(
            hotel=hotel,
            user=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)


def my_wishlist(request):
    wlist = WishList.objects.filter(user=request.user).order_by('-id')
    return render(request, 'wishlist.html', {'wlist': wlist})


def remove_from_favourite(request, id):
    hotel = Hotel.objects.get(id=id)
    hotel.favourite.remove(request.user)
    return redirect('/hotel/{0}'.format(id))


class RetrieveHotelList(APIView):
    def get(self, request):
        hotels = Hotel.objects.all()[0:10]
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetHotelRecommendation(APIView):
    def get(self, request, id):
        hotel_ids = get_recommendation_for_hotel(id)
        recommended_hotels = Hotel.objects.filter(id__in=hotel_ids)
        serializer = HotelSerializer(recommended_hotels,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CreateHotel(APIView):
    def post(self,request):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def get_hotel_info(request,id):
    try:

        hotel = Hotel.objects.get(id=id)

        hotel_ids = get_recommendation_for_hotel(id)
        recommended_hotels = Hotel.objects.filter(id__in=hotel_ids)

        return render(request, 'hotel_detail.html', {
            'hotel': hotel,
            # //LEFT SIDE KO CHAI HTML MA RAKHNE
            'recommended_hotels': recommended_hotels

        })

    except Hotel.DoesNotExist:
        return render(request, '404.html')

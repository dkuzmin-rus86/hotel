from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
# from django.http import JsonResponse
from django.core import serializers
from hotelapp.models import Hotel, Filial, Region, Room, Booking
from .forms import HotelForm, BookingForm
import datetime
from calendar import monthrange
# Create your views here.


def to_json(self, objects):
    return serializers.serialize('json', objects)


@login_required
def index(request):
    """ Формирование главной страницы """
    regions = Region.objects.filter(deleted=False).order_by('name')
    # hotels = Hotel.objects.filter(deleted=False, filial__region__in=regions).order_by('name')
    hotels = Hotel.objects.filter(deleted=False).order_by('filial', 'name')
    filials = Filial.objects.filter(deleted=False, ).order_by('region', 'name')

    return render(request, 'hotel/index.html', {'regions': regions, 'hotels': hotels, 'filials': filials})


def my_login(request):
    username = ""
    password = ""
    message = ""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            try:
                username = request.POST["username"]
                password = request.POST["pwd"]
                user = auth.authenticate(username=username, password=password)
                if user is None:
                    message = 'Неверный логин/пароль'
                    return render(request, 'hotel/login.html', {'message': message})

                if not user.is_active:
                    message = 'Неудача авторизации.'
                    return render(request, 'hotel/login.html', {'message': message})

                auth.login(request, user)
                return redirect(reverse_lazy('index'))
            except Exception:
                pass
        else:
            return redirect(reverse_lazy('index'))

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse_lazy('index'))

    return render(request, 'hotel/login.html', {'message': message})


def my_logout(request):
    if request.user.is_active and request.user.is_authenticated:
        auth.logout(request)
    return redirect(reverse_lazy('index'))


# Форма создания новой гостиницы
def create_hotel(request):
    form = HotelForm(request.POST or None)
    print('111')
    if request.method == "POST" and form.is_valid():
        try:
            print('222')
            form.save()
        except:
            print('Ошибка при сохранении данных')
        return redirect(reverse_lazy('index'))

    return render(request, 'hotel/create_hotel.html', locals())


def update_hotel(request):
    pass


def get_hotels(request):
    return render(request, 'hotel/hotels.html', locals())


def ajax_get_hotels(request):
    # message = Message()
    if request.is_ajax() and request.method == 'GET':
        hotels = Hotel.objects.filter(deleted=False).order_by('name')
        # if request.GET.get('name'):
        #     hotels = hotels.filter(name__icontains=request.GET.get('name').upper())

        # if request.GET.get('slug'):
        #     hotels = hotels.filter(slug=request.GET.get('slug'))

        # data = {'result': list(hotels)}
        data = serializers.serialize('json', hotels)
        # hotels_list = list(hotels)
        # return JsonResponse(data)
        return HttpResponse(data, content_type='application/json; charset=utf-8', status=200)
    else:
        return render(request, 'hotel/hotels.html', {'message': 'message.get_text()', 'status': 'message.status'})


# def get_bookings_room(room, date):
#     result = Booking.objects.filter(deleted=False, room=room, chekin___lte=date, chekout__gte=date).count()
#     return result


@login_required
def hotel_details(request, slug):
    year = 2018
    month = 5

    hotel = Hotel.objects.get(deleted=False, slug=slug)
    rooms = Room.objects.filter(deleted=False, hotel=hotel).order_by('category_room')

    # rm = Room.objects.get(id=1).get_count_booking(date=dt)
    # dt = datetime.now()

    first_day = datetime.date(year, month, 1)

    # last_day = datetime.date(year, month, monthrange(year, month)[1])
    # base = datetime.datetime.today()


# {   'room_number': 'A101', 
#     'category_room': 'standart',
#     'status': [{'d':'01.05.2018', 's': '1'},
#                {'d':'02.05.2018', 's': '0'}
#               ]

# }

    date_list = [first_day + datetime.timedelta(days=x) for x in range(0, monthrange(year, month)[1])]
    allroom = []
    rn = {}
    for room in rooms:
        # rn = {'room_number': room.room_number, 'category_room': room.category_room}
        # rn['room_number'] = room.room_number
        # rn['category_room'] = room.category_room

        # month_s = datetime.datetime.today().strftime("%A, %d. %B %Y %I:%M%p")
        status = []
        for dt in date_list:
            s = {'d': dt.strftime("%d.%m.%Y"), 's': room.get_count_booking(date=dt)}
            status.append(s)

        rn = {'room_number': room.room_number, 'category_room': room.category_room, 'status': status}
        # rn['status'] = status

        allroom.append(rn)

    return render(request, 'hotel/hotel_details.html', {'hotel': hotel, 'rooms': rooms, 'allroom': allroom, 'year': year, 'month': month, 'date_list': date_list})


@login_required
def booking(request, slug):
    hotel = Hotel.objects.get(deleted=False, slug=slug)
    form = BookingForm(hotel, request.POST or None)
    message = ""
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
        except:
            message = "Ошибка при сохранении данных"
        return redirect(reverse_lazy('index'))

    return render(request, 'hotel/booking.html', {'hotel': hotel, 'form': form, 'message': message})

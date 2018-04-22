from django.forms import ModelForm, Textarea, HiddenInput, CharField, TextInput, ModelChoiceField, Select, DateInput, ChoiceField, BooleanField
from hotelapp.models import Hotel, Booking, Room


class HotelForm(ModelForm):
    # pkey = CharField(required=False, widget=HiddenInput())
    # name = CharField(label='Наименование', widget=TextInput())
    # address = CharField(label='Адрес', widget=TextInput())
    # phone = CharField(label='Адрес', widget=TextInput())
    # manager = CharField(label='Адрес', widget=TextInput())
    # description = CharField(label='Адрес', widget=TextInput())

    class Meta:
        model = Hotel
        fields = ['id', 'filial', 'name', 'address', 'phone', 'manager', 'description', 'deleted']

        labels = {
                    'name': 'Наименование',
                    'address': 'Адрес',
                    'phone': 'Телефон',
                    'manager': 'Администратор',
                    'description': 'Описание',
                    'deleted': 'Удалить'
                }

        widgets = {'name': TextInput(attrs={'class': 'form-control'}),
                   'address': TextInput(attrs={'class': 'form-control'}),
                   'phone': TextInput(attrs={'class': 'form-control'}),
                   'manager': TextInput(attrs={'class': 'form-control'}),
                   'description': Textarea(attrs={'class': 'form-control'})
                   }


    # code = models.CharField(max_length=14, blank=True)
    # room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, null=False)
    # guest_name = models.CharField(max_length=512, blank=True, null=True)
    # gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    # birth_year = models.CharField(max_length=4, blank=True)
    # position = models.CharField(max_length=128, blank=True)
    # chekin = models.DateTimeField(blank=True, null=True)
    # chekout = models.DateTimeField(blank=True, null=True)
    # event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True)
    # type_placement = models.CharField(max_length=10, choices=TYPE_PLACEMENT_CHOICES, blank=True)
    # status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True)
    # payment = models.CharField(max_length=50, choices=PAYMENT_CHOICES, blank=True)
    # description = models.TextField(max_length=512, blank=True)
    # created = models.DateTimeField(auto_now_add=True, auto_now=False)
    # updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # deleted = models.BooleanField(default=False)


class BookingForm(ModelForm):

    room = ModelChoiceField(queryset=Room.objects.filter(deleted=False).order_by('room_number'), label='Комната')

    class Meta:
        model = Booking
        # fields = ['id', 'code', 'room', 'guest_name', 'gender', 'birth_year', 'position', 'chekin', 'chekout', 'event', 'type_placement', 'status', 'payment', 'description']
        fields = ['room', 'guest_name', 'gender', 'birth_year', 'position', 'chekin', 'chekout', 'event', 'type_placement', 'status', 'payment', 'description']

        labels = {
                    'room': 'Комната',
                    'guest_name': 'ФИО гостя',
                    'gender': 'Пол',
                    'birth_year': 'Год рождения',
                    'position': 'Должность',
                    'chekin': 'Дата заезда',
                    'chekout': 'Дата выезда'
                }

        widgets = {
                    # 'room': TextInput(attrs={'class': 'form-control'}),
                    'guest_name': TextInput(attrs={'class': 'form-control'}),
                    # 'gender': TextInput(attrs={'class': 'form-control'}),
                    'birth_year': TextInput(attrs={'class': 'form-control'}),
                    'position': TextInput(attrs={'class': 'form-control'}),
                    'chekin': DateInput(attrs={'placeholder': 'дд.мм.гггг', 'maxlength': '10'}),
                    'chekout': DateInput(attrs={'placeholder': 'дд.мм.гггг', 'maxlength': '10'})
                   }

    def __init__(self, hotel, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(deleted=False, hotel=hotel).order_by('room_number')

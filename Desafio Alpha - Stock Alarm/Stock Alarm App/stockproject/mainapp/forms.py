from django.forms import ModelForm
from .models import Room, Alerta

##-------------------------------ROOM CREATE MESSAGE:
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

##--------------------------------FORMULARIO ALERTA:
class AlertForm(ModelForm):
    class Meta:
        model = Alerta
        fields = '__all__'
        exclude = ['host']
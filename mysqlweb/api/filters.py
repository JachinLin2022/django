import django_filters
from .models import Food,RCom,RShop,Riden,Guest,Outorder
class OutorderFilter(django_filters.FilterSet):
    class Meta:
        model = Outorder
        fields = ('__all__')
class GuestFilter(django_filters.FilterSet):
    class Meta:
        model = Guest
        fields = ('__all__')
class FoodFilter(django_filters.FilterSet):
    class Meta:
        model = Food
        fields = ('__all__')

class RComFilter(django_filters.FilterSet):
    class Meta:
        model = RCom
        fields = ('__all__')

class RShopFilter(django_filters.FilterSet):
    class Meta:
        model = RShop
        fields = ('__all__')

class RidenFilter(django_filters.FilterSet):
    class Meta:
        model = Riden
        fields = ('__all__')
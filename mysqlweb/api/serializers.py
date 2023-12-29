from rest_framework import serializers
from .models import RShop,Food,RCom,Guest,Outorder,Riden
###################################################################
class RShopSerializers(serializers.ModelSerializer):
    class Meta:
        model = RShop     #指定的模型类
        fields = ('__all__')   #需要序列化的属性 

class RidenSerializers(serializers.ModelSerializer):
    class Meta:
        model = Riden     #指定的模型类
        fields = ('__all__')   #需要序列化的属性 

class FoodSerializers(serializers.ModelSerializer):
    class Meta:
        model = Food     #指定的模型类
        fields = ('__all__')   #需要序列化的属性 

class RComSerializers(serializers.ModelSerializer):
    class Meta:
        model = RCom     #指定的模型类
        fields = ('__all__')   #需要序列化的属性 


class GuestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Guest     #指定的模型类
        fields = ('__all__')   #需要序列化的属性 


class OutorderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Outorder     #指定的模型类
        fields = ('__all__')   #需要序列化的属性  
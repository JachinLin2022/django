from django.conf.urls import include,url
from rest_framework import routers
from api import views

# 定义路由地址
route_food = routers.DefaultRouter()
# 注册新的路由地址
route_food.register(r'rshop' , views.RShopViewSet)
route_food.register(r'rpass' , views.RidenViewSet)
route_food.register(r'food' , views.FoodViewSet)
route_food.register(r'rcom' , views.RComViewSet)

route_food.register(r'guest' , views.GuestViewSet)

route_food.register(r'outorder' , views.OutorderViewSet)
# route.register(r'upload' , views.get_post)
# route.register(r'account_card' , views.Account_CardViewSet)
# 注册上一级的路由地址并添加
urlpatterns = [
    url('api/', include(route_food.urls)),
    url('uploadshop/', views.upload_shop),
    url('uploadfood/', views.upload_food),
    url('uploadcom/', views.upload_com),
    url('uploadpass/', views.upload_pass),
    url('regshop/', views.reg_shop),
    url('delfood/', views.delete_food),
    url('addfood/', views.add_food),
    url('diancan/', views.diancan),
    url('userreg/', views.userreg),
    url('deposit/', views.deposit),
    url('changeinfo/', views.changeinfo),
    url('getorder/', views.getorder),#处理订单
]



from django.contrib import admin
from .models import RShop,RCom,Food,Riden
# Register your models here.
@admin.register(RShop)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('rno','rname')    #在后台列表下显示的字段

@admin.register(Food)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('rno','cname')    #在后台列表下显示的字段

@admin.register(RCom)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('rno','rcom')    #在后台列表下显示的字段

@admin.register(Riden)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('rno','rpass')    #在后台列表下显示的字段
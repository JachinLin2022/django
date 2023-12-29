from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets
from .models import RShop,Food,RCom,Guest,Outorder, Riden
from .serializers import RShopSerializers,FoodSerializers,RComSerializers,GuestSerializers,OutorderSerializers,RidenSerializers
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from .filters import FoodFilter,RComFilter,RShopFilter,RidenFilter,GuestFilter,OutorderFilter
import csv
from datetime import datetime
# Create your views here.
from rest_framework import filters
import json 

class RShopViewSet(viewsets.ModelViewSet):
    queryset = RShop.objects.all().order_by('-rno')
    serializer_class = RShopSerializers
    filter_class=RShopFilter

class RidenViewSet(viewsets.ModelViewSet):
    queryset = Riden.objects.all().order_by('-rid')
    serializer_class = RidenSerializers
    filter_class=RidenFilter

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all().order_by('cno')
    serializer_class = FoodSerializers
    filter_class = FoodFilter

class RComViewSet(viewsets.ModelViewSet):
    queryset = RCom.objects.all().order_by('-rcdate')
    serializer_class = RComSerializers
    filter_class = RComFilter
    # pagination_class = PageNumberPagination

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all().order_by('-gid')
    serializer_class = GuestSerializers
    filter_class=GuestFilter


class OutorderViewSet(viewsets.ModelViewSet):
    queryset = Outorder.objects.all().order_by('ono')
    serializer_class = OutorderSerializers
    filter_class=OutorderFilter
#############################################
def upload_shop(request):
    # RShop.objects.all().delete()
    with open('D:\\django\\test.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row)==0:
                continue
            if row[0]=='no':
                continue
            print(row[1])
            RShop.objects.get_or_create(rno=row[6],rname=row[1],rtime=row[5],rhl=0,rimg=row[4],rla=row[2],rlo=row[3])
            obj=RShop.objects.get(rno=row[6])
            Riden.objects.get_or_create(rno=obj,rpass="tongji2021")
            

    return HttpResponse("aoligei")

def upload_food(request):
    # Food.objects.filter(rno="E13829167297277462346").delete()
    with open('D:\django\cuisine.csv', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row)==0:
                continue
            if row[0]=='rno':
                continue
            r1=RShop.objects.get(rno=row[0])
            print(row[1])
            try:
                Food.objects.get_or_create(rno=r1,cname=row[1],cpri=row[2],cdescription=row[3],csale=row[4],cimg=row[5])
            except:
                print(row[1])
            
    return HttpResponse("aoligei")

def uploadfile(request):
    file = request.FILES.get('f1')
    print(file.name)
    with open(file.name, 'wb') as f:
        for i in file:
            f.write(i)
    return HttpResponse('ok')

def upload_com(request):
    # RCom.objects.all().delete()
    with open('D:\django\comment.csv', 'r',encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row)==0:
                continue
            if row[0]=='rno':
                continue
            date=datetime.strptime(row[2], "%Y-%m-%d").date()
            print(date)
            r1=RShop.objects.get(rno=row[0])
            RCom.objects.get_or_create(rno=r1,rcom=row[1],rcdate=date,rcscore=row[3],rcuser=row[4],rcuserimg=row[5])
            # print(date)
            # break
    return HttpResponse('ok')

def upload_pass(request):
    # Riden.objects.all().delete()
    for rshop in RShop.objects.all():
        # print(rshop.rno)
        Riden.objects.get_or_create(rno=rshop.rno,rpass="tongji2021")

    return HttpResponse('ok')

def reg_shop(request):
    rno=request.POST.get('rno')
    rpass=request.POST.get('rpass')
    rname=request.POST.get('rname')
    rtime=request.POST.get('rtime')
    rla=request.POST.get('rla')
    rlo=request.POST.get('rlo')
    rimg=request.POST.get('rimg')
    
    RShop.objects.get_or_create(rno=rno,rname=rname,rtime=rtime,rhl=0,rimg=rimg,rla=rla,rlo=rlo)
    Riden.objects.get_or_create(rno=rno,rpass=rpass)
    return HttpResponse('ok')

def delete_food(request):
    cno=request.GET.get('cno')
    obj=Food.objects.get(cno=cno)
    obj.delete()

    return HttpResponse('ok')

def add_food(request):
    rno=request.POST.get('rno')
    cname=request.POST.get('cname')
    cdescription=request.POST.get('cdescription')
    cpri=request.POST.get('cpri')
    cimg=request.POST.get('cimg')
    r=RShop.objects.get(rno=rno)
    Food.objects.get_or_create(rno=r,cname=cname,cdescription=cdescription,cpri=cpri,cimg=cimg)

    return HttpResponse('ok')

def diancan(request):
    cno=request.GET.get('cno')
    # print(cno)
    obj=Food.objects.get(cno=cno)
    obj=FoodSerializers(instance=obj)
    obj=json.dumps(obj.data,ensure_ascii=False)

    # print(obj.cpri)

    return HttpResponse(obj)

def userreg(request):
    gid=request.POST.get('gid')
    gpass=request.POST.get('gpass')
    gname=request.POST.get('gname')
    gpho=request.POST.get('gpho')
    gadd=request.POST.get('gadd')
    # print(gname)
    try:
        Guest.objects.get_or_create(gid=gid,gpass=gpass,gname=gname,gpho=gpho,gadd=gadd)
        return HttpResponse('注册成功！')
    except:
        return HttpResponse('注册失败，用户ID已经存在！')

def deposit(request):
    gid=request.POST.get('gid')
    gmoney=float(request.POST.get('gmoney'))

    guest=Guest.objects.get(gid=gid)
    money=float(guest.gmoney)
    guest.gmoney=str(round(gmoney+money,2))
    guest.save()
    return HttpResponse('充值成功！')

def changeinfo(request):
    gid=request.POST.get('gid')
    gadd=request.POST.get('gadd')
    gpho=request.POST.get('gpho')
    obj=Guest.objects.get(gid=gid)
    obj.gadd=gadd
    obj.gpho=gpho
    obj.save()
    return HttpResponse('修改成功！')

def getorder(request):
    rno=request.POST.get('rno')
    gid=request.POST.get('gid')
    gmoney=request.POST.get('gmoney')
    omoney=request.POST.get('omoney')
    
    orderlist=request.POST.get('orderlist')
    orderlist=orderlist.split('~')
    orderlist.pop()
    # 遍历所有菜品，增加销量，并生成插入订单的菜品描述
    ofood=""
    for food in orderlist:
        obj=Food.objects.get(cno=food)
        obj.csale=str(int(obj.csale)+1)
        obj.save()
        ofood=ofood+obj.cname+" "
        
    print(omoney)
    # 更新用户的余额
    gobj=Guest.objects.get(gid=gid)
    gobj.gmoney=str(round(float(gmoney)-float(omoney),2))
    gobj.save()
    # 生成订单
    robj=RShop.objects.get(rno=rno)
    odate=datetime.today()
    Outorder.objects.get_or_create(odate=odate,ofood=ofood,opri=str(round(float(omoney),2)),rno=robj,gid=gobj)

    return HttpResponse('下单成功！')
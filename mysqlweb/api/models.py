from django.db import models
import datetime
# Create your models here.
###########################################################################
class RShop(models.Model):
    rno=models.CharField(u'店铺编号',primary_key=True,max_length=150)
    rname=models.CharField(u'店铺名称',max_length=150)
    rtime=models.CharField(u'营业时间',max_length=150)
    rlo=models.FloatField(u'店铺经度',max_length=150)
    rla=models.FloatField(u'店铺纬度',max_length=150)
    rimg=models.CharField(u'店铺图片地址',max_length=1000)
    rhl=models.BooleanField(u'是否高亮显示',default=False)
    def __str__(self):
        return self.rname
class Riden(models.Model):
    rid=models.AutoField(primary_key=True)
    rno=models.ForeignKey(RShop,on_delete=models.CASCADE,verbose_name="所属餐馆",unique=True)
    rpass=models.CharField(u'店铺密码',max_length=150,blank=False)
    def __str__(self):
        return self.rpass

class Food(models.Model):
    rno=models.ForeignKey(RShop,on_delete=models.CASCADE,verbose_name="所属餐馆")

    cno=models.AutoField(primary_key=True)
    cname=models.CharField(u'菜品名称',max_length=50)
    cdescription=models.CharField(u'菜品描述',max_length=50)
    cpri=models.CharField(u'菜品价格',max_length=150)
    csale=models.CharField(u'菜品销量',max_length=150)
    cimg=models.CharField(u'菜品图片地址',max_length=150)
    class Meta:
        unique_together = ('rno', 'cname',)
    def __str__(self):
        return self.cname

class RCom(models.Model):#对店铺的评论
    rno=models.ForeignKey(RShop,on_delete=models.CASCADE,verbose_name="所属餐馆")
    rcid=models.AutoField(primary_key=True)
    rcom=models.CharField(u'店铺评论',max_length=250)
    rcdate=models.DateField(u'评论时间')
    rcscore=models.CharField(u'评论星级',max_length=50)
    rcuser=models.CharField(u'评论用户',max_length=50)
    rcuserimg=models.CharField(u'用户头像',max_length=250)
    def __unicode__(self):
        return '%d: %s' % (self.rcid, self.rcom)

class Guest(models.Model):
    gid=models.CharField(u'用户唯一标识符',primary_key=True,max_length=150)
    gpass=models.CharField(u'用户密码',max_length=200)
    gname=models.CharField(u'用户姓名',max_length=100)
    gpho=models.CharField(u'用户手机',max_length=100)
    gadd=models.CharField(u'用户地址',max_length=255)
    gmoney=models.CharField(u'用户余额',max_length=255,default='0')
    def __str__(self):
        return self.gname

class Outorder(models.Model):
    ono=models.AutoField(primary_key=True)
    odate=models.DateTimeField(u'下单时间',auto_now_add=True)
    ofood=models.CharField(u'下单菜品',max_length=255)
    opri=models.FloatField(u'下单金额')
    rno=models.ForeignKey(RShop,on_delete=models.CASCADE,verbose_name="所属店铺编号")
    gid=models.ForeignKey(Guest,on_delete=models.CASCADE,verbose_name="联系人")
    
    def __str__(self):
        return self.ono
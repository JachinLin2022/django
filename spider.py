import requests
import json
import re
import json
import time
import csv

def get_url(offset):
    url='https://mainsite-restapi.ele.me/pizza/v1/restaurants?'

    url+='&latitude=31.285487'
    url+='&longitude=121.218241'
    url+='&order_by=5'
    url+='&offset='+str(offset)
    url+='&limit=20'
    url+='&terminal=weapp'
    return url
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Cookie': 'loginSucResultAction=loginResult; st=tb_s_ele_1lQlA7xv-hyr7FgmhO5F3lA; loginType=snsLogin; open_id=oQZUI0X2kaSeNYE1wh-_xeD74948; loginScene=miniProgramLogin; resultCode=100; appEntrance=weixin; elemeExt=null; smartlock=false; snsType=weixin_mini_program; sid=17700e9d396a7ddbb0a0bb27f614a9d6; cookie2=17700e9d396a7ddbb0a0bb27f614a9d6; munb=2206268771636; SID=JQAAAAFu8Fhq6AYKAADJCkzHCVpT69HwkfRmko_xBiVnWXO_Hfz7EMgo; loginResult=success; user_id=6156212330; csg=b33e1771; union_id=o_PVDuEwNX6VsE_g0efBLq4wjuWU; USERID=6156212330; UTUSER=6156212330',
        'x-tap':'wx',
        'content-type': 'application/x-www-form-urlencoded'
    }
    

# print(get_url(40))

def get_restaurant():
    headers = ['no','name','latitude','longitude','img_url','opentime','eid']
    f=open('test.csv','w')
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    i=0
    offset=0
    while offset<=80:
        print("正在爬取第",offset,"条数据")
        res=requests.get(get_url(offset), headers=header)
        res=json.loads(res.text)
        for restruant in res:
            i=i+1
            f_csv.writerow([i,restruant['name'],restruant['latitude'],restruant['longitude'],restruant['image_url'],restruant['opening_hours'][0],restruant['id']])
        offset=offset+20

def get_comment():
    urltmp='https://restapi.ele.me/pizza/ugc/restaurants/{0}/batch_comments?&has_content=true&offset=0&limit=50'
    headertmp={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Cookie': 'SID=JQAAAAFu8Fhq6AYKAADJCkzHCVpT69HwkfRmko_xBiVnWXO_Hfz7EMgo; USERID=6156212330; cookie2=1aebe95905404cdc9236c8efe5688ef8',
        'X-Shard': 'shopid={0};loc=121.218241,31.285487'
    }
    # 读取商家的ID
    eidlist=[]
    with open("D:\\django\\test.csv",'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row)==0:
                continue
            if row[0]=='no':
                continue
            eidlist.append(row[6])
    head = ['rno','rcom','rcdate','rcscore','username','imgsrc']
    f=open('comment.csv','w',encoding='utf8')
    f_csv = csv.writer(f)
    f_csv.writerow(head)
    for eid in eidlist:
        url=urltmp.format(eid)
        header["X-Shard"]=headertmp["X-Shard"].format(eid)
        # print(header)
        res=requests.get(url,headers=header)
        res=json.loads(res.text)
        
        for comment in res["comments"]:
            content=[]
            content.append(eid)
            content.append(comment["rating_text"])
            if comment["rating_text"] is None:
                continue
            content.append(comment["rated_at"])
            content.append(comment["rating"])
            content.append(comment["username"])
            img="https://cube.elemecdn.com/"
            if comment["avatar"] is None:
                img="https://cube.elemecdn.com/c/6b/8384f98b8dedfd87fc1450926648cjpeg.jpeg"
            else:
                img="https://cube.elemecdn.com/"+comment["avatar"][0]+"/"+comment["avatar"][1:3]+"/"+comment["avatar"][3:]+".jpeg"
            content.append(img)
            # print(content)
            f_csv.writerow(content)
        

    
    





    
    # print(res.text)


def get_cuisine():
    f = open('json\\1.json',"rb")
    #将json格式的数据映射成list的形式
    info = json.load(f)

    # 获取某一列的菜品信息
    headers = ['rno','cname','cpri','cdescription','csale','imgsrc']
    f=open('cuisine.csv','w',encoding="utf-8")
    f_csv = csv.writer(f)
    f_csv.writerow(headers)

    eid=info["data"]["resultMap"]["storeHead"]["storeInfo"]["storeId"]
    # print(eid)
    for group in info["data"]["resultMap"]["menu"]["itemGroups"]:
        items=group["items"]
        for item in items:
            if(item["itemType"]==-1):
                continue
            if(len(item["tipTextList"])==0):
                continue
            irem="不存在"
            imgsrc="https://cube.elemecdn.com/"
            if 'itemRecommend' in item:
                irem=item["itemRecommend"]["reasons"][0]["text"]
            if 'imageHash' in item:
                imgsrc=imgsrc+item['imageHash'][0]+'/'+item['imageHash'][1:3]+'/'+item['imageHash'][3:]+".jpeg"

            f_csv.writerow([eid,item["name"],item["price"],irem,item["tipTextList"][0][3:],imgsrc])
            # print("菜名：%s,价格：%s,描述：%s,销量：%s" % (item["name"],item["price"],irem,item["tipTextList"][0][3:]))

def get_food():
    urltmp='https://h5.ele.me/pizza/shopping/restaurants/{0}/batch_shop?user_id=6156212330&code=0.07890730491125297&extras=%5B%22activities%22%2C%22albums%22%2C%22license%22%2C%22identification%22%2C%22qualification%22%5D&terminal=h5&latitude=31.285487&longitude=121.218241'
    header={
        'Cookie':'cna=OIsaGRWWjWUCATopzarbtEAm; perf_ssid=cvugvtr25tcx5tuwsvixui81xgm3tv7g_2021-06-06; ubt_ssid=m3poaok1fqs02i644p0i0n47evkhabyu_2021-06-06; t=66c15417173f3e7564306143888a395f; _bl_uid=45kbRpgwoFRvO42ad31y38mib7OO; xlly_s=1; track_id=1623206342|fdb754b9875308eb39362ff031f6df7cdb42eb701649b7609d|bfe42589cadbad8b54f8efd15cedb2b0; USERID=6156212330; UTUSER=6156212330; SID=LQAAAAFu8Fhq-QAEAABoPs77LWh2_oSIpTIyRcj-oqX7lWrPwV9HrzXH; ZDS=1.0|1623206343|nWQhlgJ3MXkhe6HSqcif8+NPQL6EV4EpIstn/qML395q/E3Xb1+Ozke6XnjuBMV+Ne758XKf94W5hH/ICbLI3w==; x5check_ele=0jui9GF/EfKumCq1tI0AZSVnyR/RkPhDo0499plXdC8=; tzyy=320c0a819826fe69eddc5379da94be7c; tfstk=czKdB3g87fc3NfH1ie3iVBhqHktdZCDAZc5a2vGrWf_4YsrRiwKDDE_0_OBOoAC..; l=eBjryXxej3alfMhNBOfZlurza77OSIRYHuPzaNbMiOCP_VCe5L3GB6Ovbg8wC3hRh629R38YsXPuBeYBqIqwzCOfhm8WYHkmn; isg=BO7uMZaRAhneCHYFaWzDDD_LP0Sw77LpSQiL-Ri3WvGs-45VgH8C-ZT9tmEXeaoB',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    }

    # 读取商家的ID
    start=26
    end=26
    eidlist=[]
    # eidlist.append("E16854064637350123593")
    with open("D:\\django\\test.csv",'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row)==0:
                continue
            if row[0]=='no':
                continue
            if int(row[0])<start:
                continue
            if int(row[0])>end:
                break
            # print(row[6])
            eidlist.append(row[6])

    # 初始化csv
    headers = ['rno','cname','cpri','cdescription','csale','imgsrc']
    f=open('cuisine.csv','w',encoding="utf-8")
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    # 开始爬取
    for eid in eidlist:
        print(eid)
        url=urltmp.format(eid)
        res=requests.get(url=url,headers=header)
        res=json.loads(res.text)
        for menutag in res["menu"]:
            # print(menutag["name"])
            for food in menutag["foods"]:
                if food["price"]=='0':
                    continue
                if food["image_path"]=="":
                    continue
                if food["description"]=="":
                    food["description"]="没有描述"
                if food["description"][0]=='\n':
                    food["description"]=food["description"][1:]
                imgsrc="https://cube.elemecdn.com/"+food["image_path"][0]+'/'+food["image_path"][1:3]+'/'+food["image_path"][3:]+".jpg"
                f_csv.writerow([eid,food["name"],food["price"],food["description"],food["month_sales"],imgsrc])
                # print("菜名：%s,价格：%s,描述：%s,销量：%s" % (food["name"],food["price"],food["description"],food["month_sales"]))


# get_comment()
# get_restaurant()
# get_cuisine()
get_food()

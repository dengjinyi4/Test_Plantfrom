# encoding=utf-8
__author__ = 'aidinghua'
import requests
import time
import datetime
from utils.db_info import  *

##创建一个建订单的类

class Create_ad(object):


    ##初始化函数 调用登陆接口

    def __init__(self,advertiser_id,run_type,budget,price,env_value=True):
        self.r = requests.session()
        self.r.get('http://api.demand.adhudong.com/api/advert/login.htm?name=OCPA%E6%B5%8B%E8%AF%95%E4%BB%A3%E7%90%86%E5%95%86&password=lyj123456')
        self.s=requests.session()
        self.s.get('http://api.admin.adhudong.com/login/login_in.htm?name=test&pwd=!Qq123456')
        self.advertiser_id=advertiser_id
        self.run_type=run_type
        self.budget=budget
        self.price=price
        self.t=datetime.datetime.now().strftime("%Y%m%d%H%M")
        self.today=datetime.datetime.now().strftime("%Y-%m-%d")
        self.db=DbOperations(env_value=env_value)
###查询所属广告主


    def advertiser_list(self):
        list=[]
        sql = ''' SELECT NAME FROM voyager.advertiser WHERE id IN (SELECT advertiser_id FROM voyager.agent_advertiser WHERE agent_id =2222557 AND TYPE =1 )'''
        advertiser_list=self.db.execute_sql(sql)

        for i in range(0,len(advertiser_list)):
           list.append(advertiser_list[i][0])
        return list




##创建测试计划

    def create_adplan(self):

        url = 'https://apidemand.adhudong.com/api/voyager/plan/add.htm'
        params={'aid':self.advertiser_id,'name':'测试计划'+self.t}

        plan=self.r.get(url=url,params=params)
        code=plan.json()['code']
        if code==200:
           return "广告计划已创建成功"
        else:
           return "广告计划创建失败",plan.text

    ##获取测试计划ID

    def get_planid(self):

        sql = '''SELECT id FROM voyager.ad_plan WHERE NAME LIKE '%测试计划%' ORDER BY id DESC LIMIT 1 '''
        result = self.db.execute_sql(sql)

        return result[0][0]


    ##添加有效订单
    def validorder(self):
        url='https://apidemand.adhudong.com/api/voyager/order/valid.htm'
        param={"aid":self.advertiser_id,"id":"","name":"测试订单"}
        validtt=self.r.get(url=url,params=param)
        return validtt.text

    ##添加基本信息
    def add_baseinfo(self):
        plan_id=Create_ad(2222559,1,100,0.4,True).get_planid()
        url = 'https://apidemand.adhudong.com/api/voyager/order/addBaseInfo.htm'
        params={'name':'测试订单'+self.t,'aid':self.advertiser_id,'plan_id':plan_id,'advertise_long':1,'advertise_start':'2019-09-20','advertise_end':'','advertise_time_type':'1','advertise_time_start':'','advertise_time_end':24,'advertise_time_perid':'{}','budget':self.budget,'payment_mode':2,'payment_mode_update':2,'payment':self.price,'payment_update':self.price,'frequency_control':1,'frequency':3,'time':24,'budget_allocation':1,'run_type':self.run_type}
        add_base=self.r.get(url=url,params=params)
        code=add_base.json()['code']
        if code==200:
            return "广告订单基本信息已创建完成"
        else:
            return "广告订单基本信息创建失败",add_base.text


    ###获取订单ID

    def get_orderid(self):

        sql ='''SELECT id FROM voyager.ad_order WHERE NAME LIKE '%测试订单%' ORDER BY id DESC LIMIT 1  '''
        result= self.db.execute_sql(sql)
        return result[0][0]


    ###添加定向信息

    def add_directinfo(self):

        oid=Create_ad(2222559,1,100,0.4,True).get_orderid()
        url = 'https://apidemand.adhudong.com/api/voyager/order/addDirection.htm'
        params={'aid':self.advertiser_id,'oid':oid,'region_direction':0,'position_direction':0,'media_direction':0,'device_direction':0,'region':'','media':''}
        add_direction=self.r.get(url=url,params=params)
        code=add_direction.json()['code']
        if code==200:
            return "广告订单定向信息已创建完成"
        else:
            return "广告订单定向信息创建失败",add_direction.text


##添加创意有效信息

    def validcreative(self):

        validcr=self.r.get("https://apidemand.adhudong.com/api/voyager/creative/valid.htm?aid={}&id=&name='{}'".format(self.advertiser_id,'测试创意'+self.t))
        return validcr.text

##添加创意信息

    def add_creative(self):
        oid=Create_ad(2222559,1,100,0.4,True).get_orderid()
        url='https://apidemand.adhudong.com/api/voyager/creative/add.htm'
#        params={'aid':self.advertiser_id,'oid':oid,'':'cid','':'','name':'测试创意'+self.t,'profile':'','paper_word':'%3Cp%3E%3Cbr%3E%3C%2Fp%3E','image':'https://img0.adhudong.com/creative/201909/17/e9297c6142b10afc78c222a8cff15255.jpg','thumb':'https://img2.adhudong.com/creative/201909/17/a290f94e06c8acfbddd3ebea35e3f117.jpeg','link_type':1,'device_type':0,'jump_type':1,'type':0,'link_common':'https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171','quali_imgs':''}
        params={'aid':self.advertiser_id,'oid':oid,'':'cid','':'','name':'测试创意'+self.t,'profile':'','paper_word':'%3Cp%3E%3Cbr%3E%3C%2Fp%3E','image':'https://img0.adhudong.com/creative/201909/17/e9297c6142b10afc78c222a8cff15255.jpg','thumb':'https://img2.adhudong.com/creative/201909/17/a290f94e06c8acfbddd3ebea35e3f117.jpeg','link_type':1,'device_type':0,'jump_type':1,'type':0,'link_common':'https://hongbao.chinayoupin.com/#/landing?chn=hudongtui','quali_imgs':''}
#         params={'aid':self.advertiser_id,'oid':oid,'':'cid','':'','name':'测试创意'+self.t,'profile':'','paper_word':'%3Cp%3E%3Cbr%3E%3C%2Fp%3E','image':'https://img0.adhudong.com/creative/201909/17/e9297c6142b10afc78c222a8cff15255.jpg','thumb':'https://img2.adhudong.com/creative/201909/17/a290f94e06c8acfbddd3ebea35e3f117.jpeg','link_type':1,'device_type':0,'jump_type':1,'type':0,'link_common':'http://static.adhudong.com/display/public/countly/test/countly-test.html','quali_imgs':''}

        add_creative=self.r.get(url=url,params=params)
        code=add_creative.json()['code']
        if code==200:
            return "广告订单创意已创建完成"
        else:
            return "广告订单创意信息创建失败",add_creative.text

##获取创意ID
    def get_creativeid(self):

        sql ='''SELECT id FROM voyager.ad_creative WHERE NAME LIKE '%测试创意%' ORDER BY id DESC LIMIT 1  '''
        result= self.db.execute_sql(sql)
        return result[0][0]


##保存草稿
    def draft_order(self):
        oid=Create_ad(2222559,1,100,0.4,True).get_orderid()
        url='https://apidemand.adhudong.com/api/voyager/order/draft.htm'
        params={'oid':oid,'aid':self.advertiser_id}

        draft_order=self.r.get(url=url,params=params)
        code=draft_order.json()['code']
        if code==200:
            return "订单已创建成功"
        else:
            return "订单创建失败",draft_order.text






##订单提交审核

    def subview_order(self):
        oid=Create_ad(2222559,1,100,0.4,True).get_orderid()
        url='https://apidemand.adhudong.com/api/voyager/order/review.htm'
        params={'oid':oid,'aid':self.advertiser_id}

        subview_order=self.r.get(url=url,params=params)
        code=subview_order.json()['code']
        if code==200:
            return "订单已提交审核"
        else:
            return "订单提交审核失败",subview_order.text
##后台审核创意
    def review_creative(self):
        cid=Create_ad(2222559,1,100,0.4,True).get_creativeid()
        url='http://api.admin.adhudong.com/advertiser/creativeReview.htm'
        param={'id':cid,'status':2,'level':1,'tagIds':82,'brandTagId':0}
        review_creative=self.s.get(url=url,params=param)
        code=review_creative.json()['code']
        if code==200:
            return "创意审核成功"
        else:
            return "创意审核失败",review_creative.text











if __name__=='__main__':

    ca = Create_ad(2222559,1,100,0.4,True)

    # print ca.get_time()

    # print ca.create_adplan()
    # print ca.validorder()
    # print ca.add_baseinfo()
    # print ca.get_orderid()
    # print ca.add_directinfo()
    # print ca.validcreative()
    # print ca.add_creative()
    # print ca.draft_order()
    # print ca.subview_order()
    # print ca.review_creative()
    print ca.advertiser_list()
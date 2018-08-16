# -*- coding: utf-8 -*-
# @Time    : 2018/2/24 15:03
# @Author  : wanglanqing

import requests
import sys
import time
from utils.db_info import *


class TemplateActCreation(object):
    def __init__(self, templateTypeName, act_name, award_num):
        '''
        :param templateTypeName:模板类型名称
        :param act_name: 活动名称
        :param award_num: 奖品数量，该参数由前台页面提供，分别为6和8
        :return:
        '''
        self.s = requests.session()
        self.s.get('http://api.admin.adhudong.com/login/login_in.htm?name=test&pwd=!Qq123456')
        self.templateTypeName = templateTypeName
        self.act_name = act_name
        self.award_num = award_num
        self.db = DbOperations()
        self.adzone = 467
        self.appkey="https://display.adhudong.com/site_login_ijf.htm?app_key=adhu48787abbd74d4808"

    def get_actId(self):
        '''
        :return:返回act_id
        '''
        sql_act = "select id from voyager.base_act_info where act_name='" + self.act_name + "'"
        print(sql_act)
        re_act = self.db.execute_sql(sql_act)
        if len(re_act)!= 1:
            print('get_actId,有问题')
        else:
            act_id = int(re_act[0][0])
            return act_id
    def get_awards_count(self):
        sql_ac= " select count(*) from voyager.act_award where act_id=" + str(self.get_actId())
        re_ac = self.db.execute_sql(sql_ac)
        return int(re_ac[0][0])

    def get_templateTypeId(self):
        '''
        通过全局参数templateTypeName，获得templateTypeId
        :return:返回templateTypeId
        '''
        sql_ttpye = "select id from voyager.template_type where name='" + self.templateTypeName + "'"
        print(sql_ttpye)
        re_ttpye = self.db.execute_sql(sql_ttpye)
        if len(re_ttpye) != 1:
            print('get_templateTypeId , 名称有问题')
        else:
            templateTypeId = int(re_ttpye[0][0])
            return templateTypeId

    def get_templateId(self):
        '''
        :return:返回templateId
        '''
        templateTypeId=str(self.get_templateTypeId())
        sql_ttid = "select id from voyager.base_template_info where template_type_id=" + templateTypeId
        print(sql_ttid)
        re_ttid = self.db.execute_sql(sql_ttid)
        print('&&&***^')
        print(re_ttid)
        if len(re_ttid) != 1:
            print('get_templateId, 有问题')
        else:
            templateId = int(re_ttid[0][0])
            return templateId

    def create_template_type(self, locationAdress, preview="https://img0.adhudong.com/template/201802/24/999337a35a1a9169450685cc66560a05.png",classifi=1):
        '''
        name：模板类型名称
        classifi: 模板分类，抽奖（1）、签到（2）、聚合页（3）,
        prizesNum: 要求奖品数量,
        locationAdress: 代码地址,
        preview: 模板预览图
        '''
        json_body = {
            'name': self.templateTypeName,
            'classifi': classifi,
            'prizesNum': self.award_num,
            'locationAdress': locationAdress,
            'preview': preview
        }
        post_url = "http://api.admin.adhudong.com/template/typeInsert.htm"
        re = self.s.post(post_url, data=json_body)
        print(sys.argv[0], re)
        return re
        # print(re.json()['code'])
        # if re.json()['code'] == 200:
        #     return ('200')
        # else:
        #     # try:
        #     # return myException('create_template_type, 失败了')
        #     return ('300')
        #     # except Exception as e:
        #     #     return e


    def create_template(self,templateName, templateStyleUrl, positionId=1, template_conf_items=None):
        '''
        :param templateName，模板名称
        :param templateStyleUrl， 模板样式地址，css
        :param positionId ，坑位
        :template_conf_items,  默认为空，接收前台传入的参数
        '''
        templateTypeId=self.get_templateTypeId()
        post_url ="http://api.admin.adhudong.com/template/modefy.htm"
        json_body = {
            "positionId": positionId,
            "templateTypeId": templateTypeId,
            "templateName": templateName,
            "templateStyleUrl" : templateStyleUrl,
            "templateStyleImage" : "https://img3.adhudong.com/template/201802/25/2c6f4700db7982447348db4d0960e3ad.png",
            "remark":template_conf_items
        }
        re = self.s.post(post_url, data=json_body)

        print(sys.argv[0], re)
        return re
        # if re.json()['code'] == 200:
        #     return ('create_template, 成功了')
        # else:
        #     try:
        #         # raise myException('create_template, 失败了')
        #         raise SystemExit
        #     except Exception as e:
        #         return e.message

    def create_act(self, free_num):
        '''

        '''
        #创建活动sql, act_name,award_num,free_num,template_id
        template_id=self.get_templateId()
        print('=================================' + str(template_id))
        time.sleep(10)
        post_url = "http://api.admin.adhudong.com/act/modefy.htm"
        json_body = {
            "status": 1,
            "awardNum": 3,
            "expand1": 1,
            "changeTimes": 2,
            "bannerImageUrl": "https://img3.adhudong.com/award/201802/25/9867c921ca0178820b8a37c677876223.jpg",
            "actRuleInfo": "<p>参与活动即有机会获得大奖。活动为概率中奖，奖品数量有限，祝君好运。</p><p>惊喜一：1000元现金</p><p>惊喜二：500元现金</p><p>惊喜三：200元现金</p><p>惊喜四：100元现金</p><p>惊喜五：50元现金</p><p>惊喜六：幸运奖</p><p>重要声明：</p><p>1、实物类奖品将在活动结束后5-10个工作日内安排发货，请耐心等待</p><p>2、卡券类奖品使用规则详见卡券介绍页</p><p>3、通过非法途径获得奖品的，主办方有权不提供奖品</p>",
            "isPopupAd":"1",
            "popupTemplateId":"17"
        }
        json_body['actName'] = self.act_name
        json_body['templateId'] = template_id
        json_body['freeNum'] = free_num
        re = self.s.post(post_url, data =json_body)
        return re
        # act_sql="""
        # INSERT INTO voyager.base_act_info (act_type,act_name,banner_image_url,cover_image_url,award_num,free_num,begin_time,end_time,act_rule_info,`STATUS`,update_time,create_time,template_id,expand1,expand2,expand3,expand4,expand5,expand6,expand7,expand8,expand9,change_times
        # )VALUES(1,{0},'https://img4.adhudong.com/award/201802/22/089c376e9519c85ab8ce5fced7c9ea49.jpg',
        #         NULL,{1},{2},NULL,NULL,
        #         '<p>参与活动即有机会获得大奖。活动为概率中奖，奖品数量有限，祝君好运。</p><p>惊喜一：1000元现金</p><p>惊喜二：500元现金</p><p>惊喜三：200元现金</p><p>惊喜四：100元现金</p><p>惊喜五：50元现金</p><p>惊喜六：幸运奖</p><p>重要声明：</p><p>1、实物类奖品将在活动结束后5-10个工作日内安排发货，请耐心等待</p><p>2、卡券类奖品使用规则详见卡券介绍页</p><p>3、通过非法途径获得奖品的，主办方有权不提供奖品1</p>',
        #         1,now(),now(),{3},1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL
        #     );""".format("'"+self.act_name+"'", self.award_num, free_num, templateId)
        # print(act_sql)
        # try:
        #     self.db.execute_sql(act_sql)
        #     self.db.mycommit()
        #     if self.get_actId():
        #         return ('create_act,成功了')
        #     else:
        #         try:
        #             raise myException('create_act, 失败了')
        #         except Exception as e:
        #             return e.message
        # except:
        #     self.db.myrollback()


    def create_awards(self):
        act_id = str(self.get_actId())
        # act_id = str(self.get_actId('淘粉吧转盘0228'))
        #创建奖品的sql
        award_ths =    ''',0,15,1,now(),now(),'谢谢参与','https://img0.adhudong.com/association/201802/22/10bf5888ea77ea198db1dbadc663b05f.jpg',
                  6,NULL,NULL,NULL,'<p>商品详情的信息</p>','<p>&nbsp;1.实物类奖品将在活动结束后5-10个工作日内安排发货，请耐心等待；</p><p>2.卡券类奖品使用规则详见卡券介绍页&nbsp;</p>')'''
        award_onemore= ''',0,15,2,now(),now(),'再抽一次奖品','https://img4.adhudong.com/association/201802/22/49b99fca05649598059cc2dc733509f4.jpg',
                  5,NULL,NULL,NULL,'<p>商品详情的信息</p>','<p>&nbsp;1.实物类奖品将在活动结束后5-10个工作日内安排发货，请耐心等待；</p><p>2.卡券类奖品使用规则详见卡券介绍页&nbsp;</p>')'''
        award_lucky1=  ''',0,70,3,now(),now(),'百元现金红包','https://img3.adhudong.com/association/201802/22/2c6f4700db7982447348db4d0960e3ad.png',
                7,NULL,NULL,NULL,'<p>商品详情的信息</p>','<p>&nbsp;1.实物类奖品将在活动结束后5-10个工作日内安排发货，请耐心等待；</p><p>2.卡券类奖品使用规则详见卡券介绍页&nbsp;</p>')'''
        award_lucky2=   ''',0,0,4,now(),now(),'20G流量','https://img2.adhudong.com/association/201802/22/d1c54c0eb8259f992f500015f67f8907.png',
                7,NULL,NULL,NULL,'<p>商品详情的信息</p>','<p>&nbsp;1.实物类奖品将在活动结束后5-10个工作日内安排发货，请耐心等待；</p><p>2.卡券类奖品使用规则详见卡券介绍页&nbsp;</p>')'''
        award_lucky3 =  ''',0,0,5,now(),now(),'第3个大奖品','https://img0.adhudong.com/association/201802/22/a4a40a28a4b21c1b50011102f07801a0.png',
                7,NULL,NULL,NULL,'<p>商品详情的信息</p>','<p>&nbsp;1.实物类奖品将在活动结束后5-10个工作日内安排发货，请耐心等待；</p><p>2.卡券类奖品使用规则详见卡券介绍页&nbsp;</p>')'''
        award_lucky4 =  ''',0,0,6,now(),now(),'第4个奖品','https://img0.adhudong.com/association/201802/22/a4a40a28a4b21c1b50011102f07801a0.png',
                7,NULL,NULL,NULL,'<p>商品详情的信息</p>','<p>&nbsp;1.实物类奖品将在活动结束后5-10个工作日内安排发货，请耐心等待；</p><p>2.卡券类奖品使用规则详见卡券介绍页&nbsp;</p>')'''
        award_lucky5 = ''',0,0,7,now(),now(),'第5个奖品','https://img3.adhudong.com/association/201801/09/7f7b527213eccb7e2279b428379bf193.png',
            7,NULL,NULL,NULL,'<p>商品详情的信息</p>','<p>&nbsp;1.实物类奖品将在活动结束后5-10个工作日内安排发货，请耐心等待；</p><p>2.卡券类奖品使用规则详见卡券介绍页&nbsp;</p>')'''
        award_lucky6 = ''',0,0,8,now(),now(),'第6个奖品','https://img2.adhudong.com/association/201801/09/8f3e1ae44f5f69d1f7d9730243f5a2ec.png',
            7,NULL,NULL,NULL,'<p>商品详情的信息</p>','<p>&nbsp;1.实物类奖品将在活动结束后5-10个工作日内安排发货，请耐心等待；</p><p>2.卡券类奖品使用规则详见卡券介绍页&nbsp;</p>')'''

        award_6_list = [award_ths, award_onemore, award_lucky1, award_lucky2, award_lucky3, award_lucky4]
        award_8_list = [award_ths, award_onemore, award_lucky1, award_lucky2, award_lucky3, award_lucky4, award_lucky5, award_lucky6]
        if int(self.award_num) == 6:
            award_list = award_6_list
        else:
            award_list = award_8_list
        for award in award_list:
            award_sql = '''INSERT INTO act_award (act_id,award_id,award_rate,
                priority,update_time,create_time,show_copy,award_icon,act_award_type,begin_time,end_time,award_num,
                award_details,award_get_instructions)
            VALUES (''' + act_id + award
            print(award_sql)
            try:
                self.db.execute_sql(award_sql)
                self.db.mycommit()
            except:
                self.db.myrollback()
        if self.get_awards_count() == self.award_num:
            return '奖品添加成功,奖品个数为' +  str(self.award_num)
        else:
            return '奖品添加失败'

    def __del__(self):
        self.db.close_cursor()
        self.db.close_db()


    def create_volidate_info(self):
        sql = "select id from voyager.advertiser where type=2 and state in (2,3,5) limit 15"
        adv_ids = self.db.execute_sql(sql)
        adv_id = ''
        post_url = "http://api.admin.adhudong.com/adver/violationInsert.htm"

        adv_count = len(adv_ids)
        for i in range(adv_count):
            adv_id = str(adv_ids[i][0])
            remark = '测试违规记录分页数据'+str(i)
            params = {'violationType': '1',
                      'violationRemark': remark,
                      'violationLink': 'http://music.baidu.com/songlist/tag/%E7%BA%AF%E9%9F%B3%E4%B9%90?orderType=1',
                      'advertiserId': adv_id
                      }
            print(params)
            # re = self.s.post(post_url, data=params)
            # print(re.url)

    def get_list(self):
        url = "http://api.admin.adhudong.com/advertiser/creativelist.htm?page=1&page_size=200"
        re = self.s.get(url).json()['data']['data']
        re_len = len(re)
        # print(re)
        for i in range(re_len):
            print(re[i]['id'],re[i]['state'], re[i]['lastSubReviewTime'], re[i]['createTime'])
            # print(re[i]['state'])

    def adzone_act(self):
        dsql=r"delete from voyager.adzone_act where adzone_id in ({});".format(self.adzone)
        self.db.execute_sql(dsql)
        isql=r'''INSERT  INTO voyager.adzone_act (adzone_id,act_id,act_begin_time, act_end_time,priority ) VALUES
            ( '{}','{}','2018-06-20 00:00:00', '2019-09-21 00:00:00', '1' );'''.format(self.adzone, self.get_actId())
        self.db.execute_sql(isql)
        return self.appkey

if __name__=='__main__':
    #为模板类型名称
    #__init__(self, templateTypeName, act_name, award_num):
    ct = TemplateActCreation('九宫格ce2',"九宫格ce2",8)
    #创建模板类型，create_template_type(self, classifi, locationAdress, preview="https://img0.adhudong.com/template/201802/24/999337a35a1a9169450685cc66560a05.png",prizesNum=6)
    ct.create_template_type('https://display.adhudong.com/new/nineBlockBox.html')
    # ct.get_list()
    #创建模板 ct.create_template(templateName, templateStyleUrl)
    ct.create_template('九宫格ce2',"https://display.adhudong.com/new/nineBlockBox.html",template_conf_items=r'''背景(750*1206)|bg|image||1|\n
    全屏底色|bodyBgColor|string||0|\n
    剩余次数文字颜色|leftTimesColor|string||0|/n
剩余次数数字颜色|leftTimesNumColor|string||0|)''')
    # #创建活动，    create_act(self, act_name,free_num=20, award_num=6)
    # ct.create_act()
    # #创建活动关联的奖品，
    # ct.create_awards()

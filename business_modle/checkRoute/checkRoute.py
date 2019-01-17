# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 17:05
# @Author  : wanglanqing

import requests
import re
from hdt_tools.utils.db_info import *


class checkNodeRoute(object):
    def __init__(self, env, adzoneLink):
        env_dict = {'1': True, '0': False}
        self.db = DbOperations(env_value=env_dict[env])
        self.adzoneLink = adzoneLink
        self.split_keyword = '.com/'

    def get_template_url(self):
        """
        :return:返回list，返回[{'route':'','actId':''}]
        """
        #查询模板表，查询所有新框架的模板信息
        sql = """SELECT DISTINCT (location_adress) FROM voyager.template_type WHERE
            location_adress LIKE "%.html"AND location_adress not like "%spread%" """
        sql_re = self.db.execute_sql(sql)
        urls = []
        for item in sql_re:
            #根据模板，查此模板的上线状态的活动id，只查活动id最大的那个活动
            act_sql = """SELECT a.id FROM base_act_info a
            INNER JOIN base_template_info t ON a.template_id = t.id LEFT JOIN template_type v ON t.template_type_id = v.id
            WHERE v.location_adress like '%{}%' and a.status=1 ORDER BY a.id desc limit 1;""".format(item[0].encode("utf-8"))
            act_id=self.db.execute_sql(act_sql)
            route_actId={}
            #如果查询的模板有活动id，则添加到字典中
            if act_id:
                route_actId['route']=item[0].split(self.split_keyword)[1]
                route_actId['actId']=int(act_id[0][0])
                urls.append(route_actId)
        return urls

    # @staticmethod
    def get_base_url(self):
        """
        :return:返回tuple，返回(session, 域名，参数部分)
        """
        # base_url = "https://display.adhudong.com/site_login_ijf.htm?app_key=adhud3fa7ec718584104"
        req_s = requests.session()
        req = req_s.get(self.adzoneLink)
        #处理status_code为200，但未打开活动页的情况，如303广告位无效的情况
        if req.status_code == 200 and req.content.__contains__('code'):
            return req.text
        #处理status_code为404的情况
        elif req.status_code == 404:
            return req.text
        #处理活动页正常打开的情况，拆分url
        else:
            domain_part = req.url.split('?')[0].encode("utf-8").split(self.split_keyword)[0] + self.split_keyword
            param_part = req.url.split('?')[1].encode("utf-8")
            return req_s, domain_part, param_part

    def join_url(self):
        """
        :return:当有404,500的页面时，返回list；当广告位点击无效时，返回str；当广告位点击有效，但无异常页面时，返回str
        """
        base_url_info = self.get_base_url()
        if isinstance(base_url_info, tuple):
            route_actId_dict = self.get_template_url()
            getUrl_re = []
            pattern = re.compile(r'&actId=\d+')
            tmp_rel = ''
            for item in route_actId_dict:
                tmp_rel = '&actId='+str(item['actId'])
                tmp={}
                #拼接url，域名+路由+替换actId后的参数
                target_url = base_url_info[1] + item['route'] + '?' + re.sub(pattern,tmp_rel,base_url_info[2])
                try:
                    re_tmp = base_url_info[0].get(target_url)
                except Exception as e:
                    raise e
                print re_tmp, re_tmp.url
                #将status_code为404,500的请求，路由，状态码返回
                if re_tmp.status_code in (404,500):
                    tmp['status_code']=re_tmp.status_code
                    tmp['route'] = item
                    tmp['target_url'] = target_url
                    getUrl_re.append(tmp)
            if len(getUrl_re)>0:
                return getUrl_re
            else:
                return '未发现404的落地页，路由正常'
        else:
            return base_url_info


if __name__ == '__main__':
    # https://display.adhudong.com/site_login_ijf.htm?app_key=adhueab091a2c0194285 404,none
    # https://display.adhudong.com/site_login_ijf.htm?app_key=adhueab091a2c01942 303,200
    # https://display.adhudong.com/site_login_ijf.htm?app_key=adhud3fa7ec718584104
    # cr = checkNodeRoute('1', "https://display.adhudong.com/site_login_ijf.htm?app_key=adhueab091a2c0194285")
    # cr = checkNodeRoute('1', "https://display.adhudong.com/site_login_ijf.htm?app_key=adhueab091a2c01942")
    cr = checkNodeRoute('1', "https://display.adhudong.com/site_login_ijf.htm?app_key=adhud3fa7ec718584104")
    # print cr.get_template_url()
    cr.join_url()

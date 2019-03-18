# -*- coding: utf-8 -*-
# @Time    : 2019/1/21 16:16
# @Author  : wanglanqing

import requests.sessions

def login_admin():
    # user_name = 'test'
    # pwd = '!Qq123456'
    base_url = 'http://api.admin.adhudong.com/login/login_in.htm?name=test&pwd=!Qq123456'
    admin_session  = requests.session()
    admin_session.get(base_url)
    return admin_session
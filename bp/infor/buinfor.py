#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:dengjinyi date:2020-04-01
# 对外提供页面查询信息
from business_modle.querytool import db

def getmediainfor():
    tmpsql='''SELECT ad_click_tag,act_id from voyagerlog.ad_effect_log_04 LIMIT 20;'''
    res=db.selectsql('devvoyager',tmpsql)
    return res
if __name__ == '__main__':
    res=getmediainfor()
    print res
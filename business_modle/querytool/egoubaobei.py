#!/usr/bin/env python
#coding=utf-8
__author__ = 'jinyi'
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests as r

def orderpay(orderno):
    url='http://api.chinayoupin.com/wx/paytest.htm'
    para={"orderNo":orderno}
    re=r.get(url,params=para)
    return re

if __name__ == '__main__':
    re=orderpay('3177999956447295')
    print re.text
    print type(str(re.text))
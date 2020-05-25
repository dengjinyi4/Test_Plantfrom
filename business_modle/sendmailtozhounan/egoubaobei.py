#!/usr/bin/env python
#coding=utf-8
__author__ = 'jinyi'
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')
import requests as r
from openpyxl import  Workbook

def orderpay(orderno):
    url='http://api.chinayoupin.com/wx/paytest.htm'
    para={"orderNo":orderno}
    re=r.get(url,params=para)
    return re

def makequdaoexcel():
    strtime=str(time.strftime("%Y%m%d-%H%M%S", time.localtime()))
    wb=Workbook()
    sheet=wb.active
    tmplist=[]
    sheet.append(["渠道id","渠道订单号","spuid","skuid","商品名称","购买数量","买家下单时间","会员信息","收货人","收货人电话","收货地址-省","收货地址-市","收货地址-区/县","收货地址","商家备注","平台备注"])
    for i in range(20000):
        tmp=[]
        tmp.append('146')
        tmp.append(strtime+str(i))
        # tmp.append(119531)
        # tmp.append(146123)
        tmp.append(119560)
        tmp.append(146200)
        tmp.append('测试批量结算')
        tmp.append(1)
        tmp.append('')
        # tmp.append(15)
        tmp.append('')
        tmp.append('收货人1')
        tmp.append('13811501646')
        tmp.append('北京')
        tmp.append('朝阳区')
        tmp.append('双桥')
        tmp.append('意菲克大厦4层')
        tmp.append('当天发货')
        tmp.append('当天发货')
        sheet.append(tmp)
        # path='{}.xlsx'.format(i)
        # wb.save(path)
        tmplist.append(tmp)
    # for i in range(len(tmplist)):
    #     sheet.append(tmplist[i])
    wb.save("qudao{0}.xlsx".format(strtime))
    return 1

if __name__ == '__main__':
    # makequdaoexcel()

    print(type(random.randint(1,5)))
    # strtime=str(time.strftime("%Y%m%d-%H%M%S", time.localtime()))
    # print strtime
    # tmp=['2','3']
    # tmp.append('4')
    # print tmp
    # re=orderpay('106470989663047704')
    # print re.text
    # print type(str(re.text))
    # print 1
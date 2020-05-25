#encoding:utf-8
import requests as r
import random,json
requrl='http://101.254.242.11:17490/'
# 后台接口api
reqhoutaiurl='http://101.254.242.11:17450/'
def getrandom():
    tmp=''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9','0'], 7))
    return tmp
def gettoken():
    url=requrl+'marketing/v1/account'
    params={ 'username':'manager','password':'8106ed08cf89abe215b5a0e5925e13a6'}
    res=r.get(url,params = params)
    print res.url
    token=res.json()['data']['uid']
    print token
    return token

# 供销平台下单接口
def getaccount():
    # r=r.session()
    url1=requrl+'oms/v1/orders'
    # head={"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
    head={"Content-Type":"application/json","token":"{0}".format(gettoken()),}
    # params={"orderInfoBuildParameter":{"buyerMessage":"张三","buyerRemark":"准点到达","channel":0,"cityId":1,"countyId":1,"detailAddress":"大马路边边","marketingAppKey":"EM0002","marketingOrderNo":"yigoubaobei00221212","orderItems":[{"advisePrice":1,"amount":3,"buyerPaid":1234,"dealerSkuId":"1387","dealerSpuId":"1375","providerSkuId":1,"skuCost":1,"skuFreight":3092,"skuPrice":12354}],"orderType":1,"provinceId":1,"receiveName":"丽思","receivePhone":"13927123130881","townId":1}}
    params={
 "marketingOrderNo": "auto{0}".format(getrandom()),
 "buyerMessage": "u18510993269", "receivePhone": "18510993269",
 "receiveName": "优化下单", "provinceId":1,
 "cityId":72, "countyId":2839, "townId":2839,
 "detailAddress": "亦菲克大厦新零售",
 "orderType": "1",
 "orderItems": [{  "dealerSpuId": "8401",  "dealerSkuId": "12929",  "amount": "1",
                   "buyerPaid": "10",  "skuPrice": "300",  "skuFreight": "0" }]}
    params=json.dumps(params, indent=4,sort_keys=True)
    res=r.post(url1,headers=head,data=params)
    print res.url
    # dealerChildOrderNo=res.json()['data']['childrenOrders'][0]['dealerChildOrderNo']
    dealerChildOrderNo=res.json()['data']['childrenOrders'][0]['dealerChildOrderNo']
    print 'dealerChildOrderNo is {0}'.format(dealerChildOrderNo)
    return 1

def gettokenhoutai():
    url=reqhoutaiurl+'v1/system/login/account'
    params={ 'username':'test','password':'5b3c1c40aa8aeaeb34aca6b207d288ba',"verifyCode":"123456"}
    res=r.post(url,params = params)
    # print res.url
    # print res.text
    token=res.json()['data']['uid']
    # print token
    return token
# 后台商品管理商品列表-商品搜索搜索接口
def getproductlsit():
    url1=reqhoutaiurl+'gms/v1/list'
    head={"Content-Type":"application/json","token":"{0}".format(gettokenhoutai())}
    params={"name":"test"}
    params=json.dumps(params, indent=4,sort_keys=True)
    res=r.get(url1,headers=head,data=params)
    print res.url
    print res.text
    # 后台商品管理商品列表-商品搜索搜索接口
# 后台营销平台管理营销选品-商品搜索接口
def getyingxiao_productlsit():
    url1=reqhoutaiurl+'gms/v1/librarys'
    head={"Content-Type":"application/json","token":"{0}".format(gettokenhoutai())}
    # params={'appKey':'EM0001','name':'test','pageNum':1,'pageSize':20,'isToAddShelfs':0}
    params={'appKey':'EM0001','name':'ok'}
    # params=json.dumps(params, indent=4,sort_keys=True)
    res=r.get(url1,headers=head,params=params)
    print res.url
    print res.text
# 后台营销平台管理营销选品-我的货架搜索接口
def getmyhuojia_productlsit():
    url1=reqhoutaiurl+'gms/v1/shelfs'
    head={"Content-Type":"application/json","token":"{0}".format(gettokenhoutai())}
    params={'name':'test','appKey':'EM0001'}
    # params=json.dumps(params, indent=4,sort_keys=True)
    res=r.get(url1,headers=head,params=params)
    print res.url
    print res.headers
    print res.text

# 后台订单搜索接口
def getorderlsit():
    url1=reqhoutaiurl+'oms/v1/orders'
    head={"Content-Type":"application/json","token":"{0}".format(gettokenhoutai())}
    params={"spuName":"ok"}
    params=json.dumps(params, indent=4,sort_keys=True)
    res=r.get(url1,headers=head,data=params)
    print res.url
    print res.text
# 售后
def sales():
    url1=reqhoutaiurl+'oms/v1/after/sales'
    token=gettokenhoutai()

    head={"Content-Type":"application/json","token":"{0}".format(token)}
    tmplist=["c202005191126565030112420001","c202005191126570010112420001","c202005191126572810112420001","c202005191126577740112420001","c202005191126581030112420001","c202005191126584390112420001","c202005191126588010112420001","c202005191126591760112420001","c202005191126595040112420001","c202005191126599290112420001","c202005191127002870112420001","c202005191127006520112420001","c202005191127010210112420001","c202005191127013350112420001","c202005191127018100112420000","c202005191127021540112420001","c202005191127025120112420001","c202005191127029200112420001","c202005191127034550112420001","c202005191127037930112420001","c202005191127088410112420001","c202005191127091780112420001","c202005191127095610112420001","c202005191127099370112420001","c202005191127101510112420001","c202005191127104450112420001","c202005191127108350112420001","c202005191127111430112420001","c202005191127114160112420001","c202005191127116590112420001","c202005191127119180112420000","c202005191127122500112420000"]
    for i in tmplist:
        params={"afterReasonId":"1","afterSalesType":"1","dealerChildOrderNo":"c202005161149105100112420001","dealerReasonImg":"",
                "dealerReason":"auto","dealerReturnMarketingMoney":10,"providerReturnDealerMoney":20,
                "returnAmount":"1","returnMarketingMoney":30}
        params['dealerChildOrderNo']=i
        print type(params)
        print params
        params=json.dumps(params, indent=4,sort_keys=True)
        res=r.post(url1,headers=head,data=params)
        print res.url
        print res.text

# 后台还款接口
def repayment():
    url1=reqhoutaiurl+'mfs/v1/repayment'
    head={"Content-Type":"application/json","token":"{0}".format(gettokenhoutai())}
    params={"appKey":"145","repaymentAmount":1650,"remark":"auto"}
    params=json.dumps(params, indent=4,sort_keys=True)
    res=r.put(url1,headers=head,data=params)
    # print res.url
    # print res.text
# 渠道扣款
def punish():
    url1=reqhoutaiurl+'mfs/v1/punish'
    head={"Content-Type":"application/json","token":"{0}".format(gettokenhoutai())}
    params={"appKey":"139","punishAmount":1,"remark":"auto"}
    params=json.dumps(params, indent=4,sort_keys=True)
    res=r.put(url1,headers=head,data=params)
    # print res.url
    print res.text
if __name__ == '__main__':
    # for i in range(1,10,1):
    # for i in range(1,2):
    # getproductlsit()
    # getorderlsit()
    # getmyhuojia_productlsit()
    # getproductlsit()
    # getmyhuojia_productlsit()
    # getyingxiao_productlsit()
    # re=sales()
    for i in range(200):
        re=repayment()
    print re
    # print 1


#!/usr/bin/env python
#coding=utf-8
__author__ = 'jinyi'
import sys,json
reload(sys)
sys.setdefaultencoding('utf8')
import requests as r
import egoubaobei_jd_product as jd_goods
from business_modle.querytool import db
class con_jd(object):
    def __init__(self,price):
        self.price=price

    URL='https://bizapi.jd.com/api'
    para={'token':'EZ0xUo6l5123AP0lzJ5qO3gqz'}
    para['verify']='False'
    header={'Content-Type':'application/x-www-form-urlencoded'}
    r=r.session()
    def getprice(self):
        # 红包抵扣前价格（心仪购加价后的sku商品价格），单位分
        xyg_sell_price=0
        # 心仪购当前sku最多可用的红包额度 单位分
        xyg_max_redpacket=0
        # 运费
        freight=0
        if self.price<4900:
            freight=800
        if self.price>=4900 and self.price<9900:
            freight=600
        if self.price>=9900:
            freight=0
        xyg_max_redpacket=int(self.price*0.1*0.8)
        xyg_sell_price=int(self.price+freight+self.price*0.1)
        return xyg_max_redpacket,xyg_sell_price



        return 1
class product_jd(object):
    def __init__(self,skuid):
        cjd=con_jd(1)
        self.ur=cjd.URL
        self.para=cjd.para
        self.header=cjd.header
        self.r=cjd.r
        self.skuid=skuid
        # self.pageNum=pageNum
    # 4.1 查询商品池编号
    def get_productpagenum(self):
        url=self.ur+'/product/getPageNum'
        re=self.r.post(url,data=self.para,headers=self.header)
        return re
    # 4.2 查询池内商品编号 skuIds
    def getSkuByPage(self):
        url=self.ur+'/product/getSkuByPage'
        allproduct={}
        allpagenum_products=[]
        page=json.loads(self.get_productpagenum().text)['result']
        # 取得page_num 转换成list
        pagenum=[]
        for page in page:
            pagenum.append(page['page_num'])
        for i in pagenum:
            self.para['pageNum']=str(i)
            self.para['pageNo']='1'
            re=self.r.post(url,data=self.para,headers=self.header)
            allproduct[i]=json.loads(re.text)['result']['skuIds']
            allpagenum_products.append(allproduct)
        # print allproduct
        return allproduct
    # 4.2 查询单个商品池内skuids编号
    def getSkuByPage1(self):
        url=self.ur+'/product/getSkuByPage'
        self.para['pageNum']='135238'
        re=self.r.post(url,data=self.para,headers=self.header)
        return re
    # 4.2 查询单个商品池内skuids编号和对应的价格
    def getSkuByPageandprice(self):
        # 取得固定商品池内的skuids
        re=json.loads(self.getSkuByPage1().text)['result']['skuIds']
        tmpskuids=[]
        tmpprice=[]
        for i in range(0,120):
            skuid=str(re[i])
            sellprice=json.loads(self.getSellPrice(skuid).text)['result']
            if len(sellprice)==1:
                price=sellprice[0]['price']
                print '第%s个skuid,skuid is %s'%(i,re[i])
            else:
                price=0
                print '第%s个skuid,skuid is 零零零'%(i)
            tmpskuids.append(re[i])
            tmpprice.append(price)
        print tmpprice,tmpskuids
        return tmpprice,tmpskuids
    # 查询sku是否可售
    def getskucheck(self):
        skuids=json.loads(self.getSkuByPage1().text)['result']['skuIds']
        for i,skuid in enumerate(skuids):
            skuid=str(skuid)
            re=json.loads(self.check(skuid).text)
            result=re['result']
            # print re
            if len(result)<=0:
                print re
            # 可售
            else:
                sellprice=json.loads(self.getSellPrice(skuid).text)['result']
                if len(sellprice)==0:
                    print 'skuid is %s'%skuid
                    print 'sellprice is %s '%(json.loads(self.getSellPrice(skuid).text))
        return 1
    # 4.3 查询商品详情
    def getDetail(self):
        url=self.ur+'/product/getDetail'
        self.para['sku']=self.skuid
        re=self.r.post(url,data=self.para,headers=self.header)
        return re
    # 4.4 查询商品图片;
    def skuImage(self):
        url=self.ur+'/product/skuImage'
        self.para['sku']=self.skuid
        re=self.r.post(url,data=self.para,headers=self.header)
        return re
    #4.5 查询商品上下架状态
    def skuState(self):
        url=self.ur+'/product/skuState'
        self.para['sku']='258217'
        re=self.r.post(url,data=self.para,headers=self.header)
        return re
    #4.6 验证商品可售性
    def check(self,myskuid):
        url=self.ur+'/product/check'
        self.para['skuIds']=myskuid
        self.para['queryExts']='noReasonToReturn '
        re=self.r.post(url,data=self.para,headers=self.header)
        return re
    #4.6 验证商品可售性
    def check1(self):
        url=self.ur+'/product/check'
        self.para['skuIds']=self.skuid
        self.para['queryExts']='noReasonToReturn '
        re=self.r.post(url,data=self.para,headers=self.header)
        return re
    #4.7 查询商品区域购买限制
    def checkAreaLimit(self):
        url=self.ur+'/product/checkAreaLimit'
        self.para['skuIds']='258217'
        self.para['queryExts']='noReasonToReturn '
        re=self.r.post(url,data=self.para,headers=self.header)
        return re
    # 4.12 查询同类商品
    def getSimilarSku(self):
        url=self.ur+'/product/getSimilarSku'
        self.para['skuId']=self.skuid
        re=self.r.post(url,data=self.para,headers=self.header)
        return re
    #5.1 查询商品售卖价
    def getSellPrice(self,mysku):
        url=self.ur+'/price/getSellPrice'
        self.para['sku']=mysku
        # self.para['queryExts']='noReasonToReturn '
        re=self.r.post(url,data=self.para,headers=self.header)
        # print re.text
        return re
    #5.1 查询商品售卖价
    def getSellPrice1(self):
        url=self.ur+'/price/getSellPrice'
        self.para['sku']=self.skuid
        # self.para['queryExts']='noReasonToReturn '
        re=self.r.post(url,data=self.para,headers=self.header)
        # print re.text
        return re
    #6.1 查询商品库存
    def getNewStockById(self):
        url=self.ur+'/stock/getNewStockById'
        self.para['skuNums']="[{skuId:%s,num:89}]"%(str(self.skuid))
        self.para['area']='1_0_0'
        re=self.r.post(url,data=self.para,headers=self.header)
        print re.text
        return re
    # 获取各个价格区间的skuid
    def getProduc(self):
        skuids=json.loads(self.getSkuByPage().text)['result']['skuIds']
        print len(skuids)
        print skuids
        tmp1=[]
        tmp2=[]
        tmp3=[]
        for skuid in skuids:
            if (len(tmp1)>1 and len(tmp2)>1 and len(tmp3)>1):
                break
            else:
                # 判断售价
                r=long(json.loads(self.getSellPrice(skuid).text)['result'][0]['price'])
                if r<49:
                    tmp1.append(skuid)
                if r>49 and r<99:
                    tmp2.append(skuid)
                if r>99:
                    tmp3.append(skuid)
        return tmp1,tmp2,tmp3


        return 11
    # 获取每个商品池里有多少skuid
    def getpageproduct(self):
        tmpdit={}
        re=self.getSkuByPage()
        for k,y in re.items():
            tmpdit[k]=len(y)
        print tmpdit
        count=0
        for k,v in tmpdit.items():
            count=count+int(v)
        print '一共的skuid是%s'%count
        return 1
    # jd商品详情
    def get_jd_goods(self):
        jd=jd_goods.jd_Product()
        jd.skuid=self.skuid
        # 商品详情
        tmp=json.loads(self.getDetail().text)['result']
        # 商品名字
        jd.goods_name=tmp['name']
        # 京东分类，分别是1、2、3级分类
        jd.category=tmp['category']
        # 用的是接口里的 主图
        jd.small_img=tmp['imagePath']
        # 同类商品 主要是获取规格 这里也有img_url
        tmp=json.loads(self.getSimilarSku().text)['result']
        jd.goods_spec_1_name=tmp[0]['saleName']
        for i in tmp[0]['saleAttrList']:
            if int(self.skuid) in i['skuIds']:
                jd.img_url=i['imagePath']
                jd.goods_spec_1_value=i['saleValue']
        # 详情图从图片接口获取，isPrimary=0
        tmp=json.loads(self.skuImage().text)['result']
        jd.detail_img=[]
        for i in tmp[self.skuid]:
            if i['isPrimary']==0:
                jd.detail_img.append(i['path'])
        # 是否可售
        tmp=json.loads(self.check1().text)
        jd.sale_status=tmp['result'][0]['saleState']
        tmp=json.loads(self.getSellPrice1().text)['result']
        # print tmp
        # 采购价格（平台从经销商买入的价格），单位分
        tmprice=tmp[0]['price']*10
        jd.platform_buy_price=int(tmprice*10)
        print jd.platform_buy_price
        jdprice=con_jd(jd.platform_buy_price)
        xyg_max_redpacket,xyg_sell_price=jdprice.getprice()
        jd.xyg_max_redpacket=xyg_max_redpacket
        jd.xyg_sell_price=xyg_sell_price
        return jd
    # 对比京东价格和normandy.normandy_jd_goods表中价格
    def jd_price_db(self):
        normandysql='SELECT jd_sku_id,platform_buy_price,xyg_max_redpacket,xyg_sell_price from normandy_jd_goods limit 100'
        re=db.selectsql('nomandytest',normandysql)
        tmplist=[]
        for i in re:
            jd_platform_buy_price=0
            xyg_max_redpacket=0
            xyg_sell_price=0
            jd_platform_buy_price=int(json.loads(self.getSellPrice(str(i[0])).text)['result'][0]['price']*100)
            jdprice=con_jd(jd_platform_buy_price)
            xyg_max_redpacket,xyg_sell_price=jdprice.getprice()
            if (jd_platform_buy_price!=int(i[1]) or xyg_max_redpacket!=int(i[2]) or xyg_sell_price!=int(i[3])):
                tmplist.append(str(i[0])+"_"+str(i[1])+"_"+str(i[2])+"_"+str(i[3]))
        return tmplist


if __name__ == '__main__':
    # price=con_jd(1500)
    # print price.getprice()
    jd=product_jd('180405')
    # jd=product_jd('154248')
    # x=jd.get_jd_goods()
    # 对比价格
    print  jd.jd_price_db()
    # print jd.getProduc()
    # print jd.getSellPrice1().text
    # print jd.getDetail().text
    # print jd.getSimilarSku().text
    # print jd.getNewStockById().text
    # print jd.get_productpagenum().text
    # print jd.getpageproduct()
    # print jd.getSkuByPage1().text
    # print jd.get_jd_goods()
    # print jd.getSkuByPageandprice()
    # print jd.getskucheck()
    # print jd.getSellPrice().text
    # print jd.skuImage().text
    # print jd.skuState().text
    # print jd.check().text
    # print re.json()
    # print json.loads(re.content)['result']
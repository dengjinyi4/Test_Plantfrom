#!/usr/bin/env python
#coding=utf-8
__author__ = 'jinyi'
import sys,json
reload(sys)
sys.setdefaultencoding('utf8')
from business_modle.querytool import db
# 定义jd商品类
class jd_Product():
    # 经销商商品id
    skuid=''
    # 商品名称
    goods_name=''
    # 商品副标题 没有
    goods_sub_name=''
    # 商品小图集合
    small_img=''
    # 商品大图集合（轮播图） 没有
    big_img=''
    # 详情描述文本 没有
    detail_text=''
    # 详情描述图集合（10张图左右）
    detail_img=[]
    # 状态：0初始 1可同步 2已同步
    status=''
    # 状态：0未下架 1已下架
    sale_status=''
    # 红包抵扣前价格（心仪购加价后的sku商品价格），单位分
    xyg_sell_price=''
    # 采购价格（平台从经销商买入的价格），单位分
    platform_buy_price=0
    # 心仪购当前sku最多可用的红包额度 单位分
    xyg_max_redpacket=''
    # 京东分类
    category=''
    # saleName 销售名称-> 商品规格1名称
    goods_spec_1_name=[]
    # saleValue 标签名称-> 商品规格1值
    goods_spec_1_value=''
    # 规格缩略图 应该是处理过的
    img_url=''

def checkcate():
    sql= '''SELECT  spu_id,COUNT(1) from normandy_jd_goods where spu_id is not null GROUP BY spu_id HAVING COUNT(1)>1  ORDER BY COUNT(1) desc'''
    re=db.selectsql('nomandytest',sql)
    tmpspuid=[]
    # # 最终有问题的spuid
    tmpspucat=[]
    for i in re:
        tmpspuid.append(str(i[0]))
    # print tmpspuid
    # tmpspuid=['1012439','1012451','1012519','1058908','1315798','1315806','1328750','1328761','1603742','1875992','1875996','1887518','1887526','2141148','2141152','2141153','2141154','2217736','2217746','2217750','2218385','2218387','530233','971067','971592']
    for i in tmpspuid:
        catsql='''SELECT DISTINCT category_id_level_1,category_id_level_2 from normandy_jd_goods where spu_id={}'''.format(str(i))
        recat=db.selectsql('nomandytest',catsql)
        print tmpspuid.index(i)
        if len(recat)>1:
            tmpspucat.append(str(i))
    print tmpspucat
    return 1



if __name__ == '__main__':
   # print 1111
   # j=jd_Product
   # j.skuid='2222'
   # print j.__dict__['skuid']
   print checkcate()

    # print jd.getSkuByPageandprice()
    # print jd.getskucheck()
    # print jd.getSellPrice().text
    # print jd.skuImage().text
    # print jd.skuState().text
    # print jd.check().text
    # print re.json()
    # print json.loads(re.content)['result']
# encoding: utf-8
import requests,datetime,time
def login():
    param={'name':'test','pwd':'qq'}
    url='login/login_in.htm?'
    print url
    s=requests.session()
    s.get(url,params=param)
    # r=s.get('http://admin.adhudong.com:17071/user/ListUser.htm?username=coldman&status=1&descn=jack&create_time=1')
    return s
# 调用接口
def getcod(url):
    s=requests.session()
    jar = requests.cookies.RequestsCookieJar()
    # 后台cookie
    # jar.set('YQFJSESSIONID','8DC44EA9A30E4AE6868A0CDF1AC4B2BA',domain='221.122.127.41')
    # jar.set('JSESSIONID','614C260AFC70499EB2F4376D27EBFDD3',domain='weixin.eqifa.com')
    # jar.set('eqifaUser','ZWdvdUBlbWFyLmNvbS5jbi8vLy8xNTUvL2Vhcm5lci8vbWVuZ3hpYW5neWFuQGVtYXIuY29tLmNuLy8vLy8vMDEwLTU4NzkzOTgwLTg2MzkvLzM0MzEyMjE0MTUvL21lbmdtZW5nOTIxODI4QGhvdG1haWwuY29tLy9tZW5neGlhbmd5YW5AZW1hci5jb20uY24vLy8vLy8wMTAtNTg3OTM5ODAtODYzOS8vMzQzMTIyMTQxNS8vbWVuZ21lbmc5MjE4MjhAaG90bWFpbC5jb20vL9PQ0KcvLzI5NS8vMS8vOGE1ZGFiZmQ=',domain='.eqifa.com')
    try:
        r=requests.get(url, timeout=2)
        # count= r.json()['fanye']['count']
        # if int(count)>0:
        #     print'count %s' %count
        # else:
        #     print'nnnnnn'
    except Exception as e:
        return str(e.message)
    result=str(r.status_code)
    return result
# 写文件
def writefile(t,url,code):
    f=open('f1.txt','a')
    f.write(t+','+url+','+code+'\n')
    # f.write('----------------')
    f.closed
def f(url):
    code=getcod(url)
    now=datetime.datetime.now()
    writefile(str(now),str(url),str(code))
    # print str(now),str(url),str(code)+'\n'
def do():
     while 1==1:
        urllist=[
        # 后台地址
        # 'http://221.122.127.41:19100/benefitlist.do',
        # 'http://221.122.127.206:19100/benefitlist.do',
        # 'http://221.122.127.63:19100/benefitlist.do',
        # 'http://221.122.127.202:19100/benefitlist.do',
        # 'http://221.122.127.204:19100/benefitlist.do',
        # 'https://admin.yiqifa.com/benefitlist.do'
        # 'http://weixin41.eqifa.com:19120/earner/search/list?pn=1&ps=20&mType=china&region=%E4%B8%AD%E5%9B%BD',
        # 'http://weixin63.eqifa.com:19120/earner/search/list?pn=1&ps=20&mType=china&region=%E4%B8%AD%E5%9B%BD',
        # 'http://weixin206.eqifa.com:19120/earner/search/list?pn=1&ps=20&mType=china&region=%E4%B8%AD%E5%9B%BD',
        # 'http://weixin207.eqifa.com:19120/earner/search/list?pn=1&ps=20&mType=china&region=%E4%B8%AD%E5%9B%BD',
        # 'http://weixin192.eqifa.com/earner/search/list?pn=1&ps=20&mType=china&region=%E4%B8%AD%E5%9B%BD',
        # 'http://weixin193.eqifa.com/earner/search/list?pn=1&ps=20&mType=china&region=%E4%B8%AD%E5%9B%BD',
        # 'http://weixin194.eqifa.com/earner/search/list?pn=1&ps=20&mType=china&region=%E4%B8%AD%E5%9B%BD',
        # 'https://www.yiqifa.com/',
        # 'http://www.yiqifa.com/',
        # 'https://www.eqifa.com/',
        # 'https://weixin.eqifa.com/',
        # 'https://weixin.eqifa.com/earner/search/list?pn=1&ps=20&mType=china&region=%E4%B8%AD%E5%9B%BD',
        #'http://weixin.eqifa.com/earner/dataReport/cpshighdata?creatdate=2017-08-01+%2F+2017-08-28&searchOption=wap&ps=20&pn=1&status=4',
        #'http://weixin.eqifa.com/earner/dataReport/cpshighdata?creatdate=2017-08-01+%2F+2017-08-28&searchOption=wap&ps=20&pn=1&status=3',
        #'http://weixin.eqifa.com/earner/dataReport/cpshighdata?creatdate=2017-08-01+%2F+2017-08-28&searchOption=wap&ps=20&pn=1&status=2',
        #'http://weixin.eqifa.com/earner/dataReport/cpshighdata?creatdate=2017-08-01+%2F+2017-08-28&searchOption=wap&ps=20&pn=1&status=1'
        'http://www.baidu.com',
        'http://www.taobao.com',
        'https://m.dianniu98.com/wap/regist/recordRegist3.htm?channelSource=190',
        'http://www.18183g.cn/by91.html',
        'http://app.ftzhu.com/hd2/ ',
        'http://www.029hch.com/ice/index.html?source=icegame7',
        'http://www.nasiosoft.com/mobile/goods3.php?act=quick_buy&id=180',
        'http://app.woifh.com/hd2/',
        'http://kongddz.com:8080/table/index.html?file=table/index.html&channel_id=hudong1&v=3.1',
        'http://x.jumei.com/activity/ad/index?hash=2cd77032&channel=hudongtui',
        'https://itunes.apple.com/cn/app/%E4%BD%93%E8%82%B2%E5%BD%A9%E7%A5%A8-%E5%8D%87%E7%BA%A7%E5%8A%A0%E5%BC%BA%E7%89%88/id1234893802?mt=8',
        'http://s.kuangxiangshid.com/YingHuangfree.html?channel_id=hdt&v=5.7.1',
        'http://m.template.51jiabo.com/hz/174?src=hdt&uid=hzlanse',
        'http://99999tv.com ',
        'http://dwz.cn/68PP4I ',
        'https://ecentre.spdbccc.com.cn/creditcard/indexActivity.htm?data=P1218757&itemcode=hayj000010 ',
        'http://www.chuangkegang.cn/wz02/',
        'http://app.woifh.com/hd2',
        'http://m.template.51jiabo.com/ks/172?src=hdt&uid=ks0913-quan',
        'http://abc.wanmeilr.com/Bao/Index3?id=9084&tc=yiqifa',
        'http://win.jdcf88.com/new/20170911',
        'http://app.bgsht.com/br/',
        'http://95508.com/zctikB2s',
        'http://bsympj.com',
        'https://phone.0451idc.com/3Dapp/3dbuyu_B098.apk ',
        'http://dan.yuzhikun.com/item/888.htm?gzid=1',
        'http://app.jgyee.com/ht/',
        'https://abc.wanmeilr.com/Bao/Index3?id=9098&tc=yiqifa',
        'http://kongddz.com:8080/hongbao/index.html?file=summer&channel_id=kupai&v=1.00',
        'http://down.23d5.com/gamecenter-release-android-lanyue-481.apk',
        'https://jq.qq.com/?_wv=1027&k=5s9XoKe',
        'http://lunhb.com/?from=groupmessage&isappinstalled=0',
        'http://zyjj1688.com/',
        'http://app.58duoshou.com/brs2/',
        'http://www.xinxingcun.net/',
        'http://ly.yyjm188.com/',
        'http://999.wawj58.cn/',
        'http://app.yule176.com/hd2',
        'http://app.qingyi1314.com/dong/',
        'http://www.jrfazh.cn/daikuan/ykjk/hdtui/?cid=B4-4101',
        'http://dp.zjyanxing.com/item/hu3?gzid=',
        'https://www.036745.com/#hdtui08',
        'https://m.qmcai.com/hd/qd/huTuiWheel0930/index.html',
        'https://hpmj.734399.com/wap/hpnn.html',
        'http://down.3h6x.com/gamecenter-release-android-baiying-410.apk',
        'http://app.wanju12345.com/hdt/',
        'http://rng5.com/in/?300037 ',
        'http://lfslaw.cn/',
        'http:// http://lfslaw.cn/',
        'http://hk20170905.w138-e1.ezwebtest.com/',
        'http://rng5.com/in/?300050',
        'https://down.dyndes.com/android/A_6306_20170920.apk',
        'https://down.dyndes.com/android/A_6308_20170920.apk',
        'http://wap.habhk.com/',
        'https://html.ttjingpai.com/362d859c-b2ef-11e7-a521-00163e04ac98.html',
        'https://ecentre.spdbccc.com.cn/creditcard/indexActivity.htm?data=P1218757&itemcode=hayj000012',
        'http://adds.slsma.cn/',
        'http://osi.xf120.com/jxs/zre?pid=887327&uyc=aHR0cDovL2FwcC56YjF0LmNvbS90Yi8=',
        'https://c.pingan.com/ca/index?sign=7c02d27ee4ff291ec3f2606e8787dde2&versionNo=R10310&scc=910000167&channel=WX&onlineSQFlag=N&isDisplayRecommend=N&isDisplaySales=N&ccp=1a',
        'http://rng5.com/in/?300018',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT83',
        'http://wzz.zbxhw.com.cn/',
        'https://www.d88portal.net/d88_app_1000842391.html',
        'http://www.eqianzhuang.com/cpc_dsp/index.html?eqz_id=yc_dsp_11#/',
        'http://app.bzzys.com/hdt2',
        'http://hdt.helmos.com.cn/',
        'http://app.wudao9.com/bk ',
        'http://app.jmjjj.com/hdt/',
        'http://ta.shouyiwl.com/',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT87',
        'http://813320.top',
        'https://shop.xm9m.com/html/naunfengshan_20171020_102_1828.html?_c=',
        'http://app.aixmgo.com/hdt/',
        'https://mbank.bankofshanghai.com/pweixin/static/index.html?_TransactionId=CreditCardApply&_CardType=0300001616&YLLink=630074',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT80',
        'http://www.qing-hei.com/mobile.php/Landing?ad=hudongtui2',
        'http://app.woifh.com/hdt2/',
        'https://h5.jdd.com/activities/channel/index.html?code=98',
        'http://vvvvvv.18183g.cc/jipinzjh_2319_141.apk',
        'https://mp.weixin.qq.com/s?__biz=MzA3OTA1NzI4NA==&mid=2650953359&idx=2&sn=e8f5006788ed54b8fdc8041a790bf753&chksm=844fae64b33827724354e8c79e59c348662eb1914720c2086605ba033a32fc0f1b949a953dfa#rd',
        'http://lm.yzw669.com/ju2',
        'http://dp.zjyanxing.com/item/hu4?gzid=',
        'http://wx.aolaigo.com/app/activity/html/other/newbie-page.html?id=5050&hs_from=26',
        'http://app.cmxww.com/hdt/',
        'http://fhm.bigins.cn/metlife/freeins?channel=9',
        'http://www.qing-hei.com/mobile.php/Landing?ad=hudongtui1',
        'http://www.sjclyx.com/adsm/qsce.html?=ads',
        'http://app.bzzys.com/kmt/',
        'http://win.newwinner.com.cn/wap2/szhg20171018/index.html?bid=110527&reffer=1 ',
        'https://stat.yfegame-download.com/gametrack?method=downtrack&market=30&downtype=1&platform=4',
        'https://stat.99game.me/gametrack?method=downtrack&market=151&downtype=1&platform=4',
        'https://m.invest.ppdai.com/landinginfonew.html?regsourceid=yima',
        'http://app.10000nn.com/hmly/',
        'https://h5.egou.com/pop/info.html?id=129',
        'https://ccshop.cib.com.cn:8010/application/cardapp/newfast/ApplyCard/toSelectCard?id=de1123ae9bf54e28b81379f12f4859f1',
        'https://www.citibank.com.cn/sim/ICARD/RCE/index.html?ecid=AFECTT60043',
        'https://www.citibank.com.cn/sim/ICARD/RCE/index.html?ecid=AFECHDT10071',
        'http://www.qing-hei.com/mobile.php/Landing?ad=tuiba3',
        'https://www.citibank.com.cn/sim/ICARD/RCE/index.html?ecid=AFECHDT10074',
        'http://ddz.down.3332game.com/sale_num32/kuaiyin_sale_num32_v2.6.2.apk',
        'http://www.jrfazh.cn/daikuan/ykjk/hdtui/?cid=B4-4115',
        'https://mbank.bankofshanghai.com/pweixin/static/index.html?_TransactionId=CreditCardApply&_CardType=0300001616&YLLink=630073',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT76',
        'https://www.citibank.com.cn/sim/ICARD/RCE/index.html?ecid=AFECXL20184',
        'http://app.3ddov.com/zca/',
        'https://www.citibank.com.cn/sim/ICARD/RCE/index.html?ecid=AFECXL20185',
        'https://activity.hspiaohao.com/newbieTwo/toFHRedPacketRegister.html?channelIdentify=hdt1020&channelVersion=1.0.&channelId=615451733424390144',
        'https://www.citibank.com.cn/sim/ICARD/RCE/index.html?ecid=AFECXL20186',
        'http://811554.top/',
        'http://www.qc2588.com/down/qc_258800063_1.0.2.apk',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT59',
        'http://channel.wxshy.net/l/hudongtui01701',
        'http://channel.wxshy.net/l/hudongtui01702',
        'http://down.5e47.com/gamecenter-release-android-weilan-162.apk ',
        'http://update.youyou80.com/download/171011/dd_v110101717_124.apk',
        'https://vip.iqiyi.com/firstsix-new-h50.html?fv=449bf6f675b48d6e3fd9ec607fd72523',
        'http://app.dmkyy.com/bxm/',
        'https://creditcardapp.bankcomm.com/applynew/front/apply/track/record.html?trackCode=A0920153711876',
        'https://down.dyndes.com/android/A_6392_20170920.apk',
        'https://ccshop.cib.com.cn:8010/application/cardapp/newfast/ApplyCard/toSelectCard?id=19d1ab736cb4418b9b4ad7d3892f1c66',
        'https://c.pingan.com/apply/mobile/apply/index.html?scc=900000330&ccp=9a1a2a3a4a5a8a10a11a12a13&xl=01a02a03a04a05&showt=0',
        'http://www.yml365.cn/bxnjxb2001hdt.htm?gzid=bxnjxb2001hdt_8',
        'http://jj.wangfengyi.cc/',
        'http://ibeidian.com',
        'http://app.0416sp.com/ygg/',
        'http://u4787464.viewer.maka.im/k/OJVCYBTC',
        'http://campaign.rong360.com/applanding/rongapp/landing_22.html?android=rong360-c_hdt_new_1-release.apk&utm_source=hdt&utm_medium=new&utm_campaign=1',
        'http://m.bigou.cn/h5/landing.html?chn=yibo',
        'http://app.9daiyun.com/dr/',
        'http://www.newqiming.top/jf-ht1030/',
        'https://as-vip.missfresh.cn/ug/landing-page.html?fromSource=hdt',
        'http://fhm.bigins.cn/cebao/dlb/?channel=1',
        'http://apk.kuangxiangshid.com/GameCity_yhgj_hdt2.apk',
        'https://m.rong360.com/express?from=sem32&utm_source=hdt&utm_medium=cpc&utm_campaign=sem32',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT89',
        'http://www.114jin.com/addwx1027/',
        'http://down.3h6x.com/gamecenter-release-android-baiying-340.apk',
        'http://app.slycg.com/tx5/',
        'http://apple.xintongzhou.net.cn/hhgz020.htm?gzid=',
        'http://app.dishik.com/hdt/',
        'http://www.weloan.com/regApp?un=ODI2Mzc5',
        'http://www.114jin.com/gettel0918/',
        'https://ultimavip.cn/m/mposter.html?source=hudongtui_001_t_mposter',
        'https://ultimavip.cn/m/mposter.html?source=hudongtui_002_t_mposter',
        'https://as-vip.missfresh.cn/ug/landing-page.html?fromSource=hdt-2',
        'https://ultimavip.cn/m/lposter.html?source=hudongtui_001_t_lposter',
        'http://api.huoyanzichan.com/weixinH5/templates/regin.html?channelId=71',
        'http://m.template.51jiabo.com/sh/167?src=hdt&uid=sh1031',
        'http://www.gotojp.org/tb2/',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT60',
        'http://www.114jin.com/gettel1017',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT58',
        'http://m.imtou.com/reg/index_hk?dfrom=hdttyj&versionID=1.0&channelID=18 ',
        'https://ccshop.cib.com.cn:8010/application/cardapp/newfast/ApplyCard/toSelectCard?id=5ad10465a93644119386b9cc64b47b20',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT65',
        'http://www.newqiming.top/jf-ht1027/',
        'http://down.5e47.com/gamecenter-release-android-weilan-180.apk',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT77',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT88',
        'https://as-vip.missfresh.cn/ug/landing-page.html?fromSource=hdt-1',
        'https://creditcard.ecitic.com/citiccard/cardshop-h5/wap/initCardInfo.do?pid=CS0002&sid=SJVTXSHT63',
        'https://creditcard.ecitic.com/h5/shenqing/yan/index.html?sid=SJVTXSHT68',
        'https://m.wselearning.com/1500giftsqa/index.aspx?winType=HDT709WGQA',
        'https://m.wselearning.com/Registernetworkj/pro-1.aspx?winType=HDT1709SNJ',
        'http://910youxi.com/tools/Down.aspx?TGCode=19055',
        'https://ultimavip.cn/m/mposter.html?source=hudongtui_003_t_mposter'
        ]
        for url in urllist:
            wf(url)
        time.sleep(5)

if __name__ == '__main__':
    do()
    # url='http://weixin.eqifa.com/earner/dataReport/cpshighdata?creatdate=2017-08-01+%2F+2017-08-28&searchOption=wap&ps=20&pn=1&status=3'
    # getcod(url)
    # while 1==1:
    #     urllist=['http://221.122.127.41:19100/benefitlist.do','http://221.122.127.206:19100/benefitlist.do','http://221.122.127.63:19100/benefitlist.do','https://admin.yiqifa.com/benefitlist.do']
    #     for url in urllist:
    #         wf(url)
    #     time.sleep(5)



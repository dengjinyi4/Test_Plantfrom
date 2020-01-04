#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json,time
from business_modle.querytool import db
from collections import Counter
from elasticsearch import Elasticsearch

def order_reson():
    tmp={"A":"同一用户cookie24小时内重复展现","B":"订单无效或当前时间不可投放","C":"今日没有预算","D":"预算已不足","E":"投放状态错误（冻结或暂停或结束）","F":"出价过低","G":"订单对应广告主无效或状态错误","H":"订单对应广告计划无效或错误",
                "I":"被此广告位定向过滤过滤","J":"被此广告位URL定向过滤","K":"该订单过滤该广告位媒体","L":"被订单的地域限制过滤","M":"被订单的设备限制过滤","N":"被用户频次限制过滤","O":"坑位类型不匹配","P":"没有广告着陆页地址","Q":"广告链接重复",
                "R":"广告着陆页域名被封","S":"广告图片相似","T":"创意无效或状态错误","U":"被广告位次配置过滤","V":"没有小时预算","W":"小时预算不足","X":"广告位和广告创意等级不匹配","Y":"隐藏过滤时间","Z":"隐藏过滤地域","a":"广告订单媒体资质定向不符",
                "b":"广告订单媒体广告位定向不符","c":"媒体不可以投放百度广告,活动不支持百度广告","d":"广告位高级屏蔽","e":"小程序广告在非小程序广告位","f":"非小程序广告在小程序广告位","g":"出价过低","h":"活动定制过滤","i":"订单没有坑位尺寸的创意","j":"该广告位达到订单设置的投放数量限制",
                "k":"托底广告主过滤","l":"商品不存在或不支持cps","m":"商品不在推广期","n":"商品CPS账户保证金账户余额不足","o":"不是微信游戏配置订单",
                "p":"不是指定的广告订单","q":"ocpa出价过低","r":"ocpa暂停","s":"媒体不支持ocpa","t":"被订单的地域限制(后台)过滤","u":"不在广告位出价范围内",
                "v":"媒体不支持A3A5广告主通投订单","w":"未找到对应cvr","x":"旧A3A5定向订单","y":"此广告位在该ocpa订单投放范围之外","z":"强推订单不在非强推坑位出现",
                "A1":"ocpa未找到对应首效果类型","A2":"不是纸巾宝指定广告类型","A3":"微信流量过滤支付宝广告","A4":"ocpa教育客户过滤非综合支付媒体",
                "A5":"北上广深杭过滤棋牌","A6":"加粉订单在新媒体上消耗超过10%","TT1":"媒体id=2759上的活动id=710，用户点击未成年人签，抽奖时，过滤掉加粉类型的广告",
                "A7": "广告位不接受低于1毛的定向订单","A8":"广告主A1出价大于等于0.2元","A9":"广告主A1在IOS出价大于等于0.3元",
                "A10":"广告主A3出价大于等于0.5元","A11":"广告主A3在IOS出价大于等于0.6元","A12":"广告主A5出价大于等于0.6元",
                "B1":"内部推广坑位定向,5,6,7坑位只展示指定订单","B2":"内部推广坑位定向,订单只能在5,6,,7,8坑位展示","B3":"该坑位不支持展示广点通广告", "B4":"直跳活动不出现广点通广告","B5":"活动模版不支持展示广点通广告","B6":"域名配置信息不支持广点通广告","B7":"订单实时消耗大于预期消耗，不满足OCPA扩量条件","B8":"OCPA扩量订单,效果数为0时，只能在指定广告位出现:",
                "B9": "OCPA扩量订单,排除按 cps结算广告位,实时消耗已达标,（实时消耗—预期消耗）/预期消耗=",
                "B10": "非智能增量的ocpa通投订单，不可投放",
                "TT1": "媒体id=2759上的活动id=710，用户点击未成年人签，抽奖时，过滤掉加粉类型的广告"
         }
    return tmp
def getorder_rs(mydit):
    orderreson=order_reson()
    alldit={}
    orderreson=order_reson()
    for (j,k) in mydit.items():
        if j in orderreson:
            alldit[orderreson[j]]=k
        else:
            alldit[j]=k
    return json.dumps(alldit, encoding='UTF-8', ensure_ascii=False)
# 对未出的广告订单进行汇总
def getorderreson(mydit):
    # mydit={"6350":"Q","8894":"B","8891":"B","8892":"B","8777":"K","8895":"B","9061":"L","9062":"Y","9065":"B","8098":"M","8890":"B","9063":"Y","9064":"K","8090":"L","8648":"K","8526":"B","8768":"B","8889":"L","8783":"K","8781":"K","9078":"K","8782":"K","9079":"K","8664":"Q","8665":"D","9072":"B","9073":"B","9071":"K","9076":"K","9077":"L","9074":"K","9075":"K","8537":"A","8658":"B","8779":"K","5041":"B","8673":"A","8552":"B","8674":"Y","7343":"L","8671":"Y","8672":"Y","8793":"D","8675":"Y","7346":"L","8676":"Y","8670":"K","6491":"A","9080":"L","5956":"K","8326":"K","8323":"B","7903":"K","8332":"M","8572":"A","8457":"K","8578":"A","8214":"K","8577":"A","8570":"B","8450":"A","8448":"Q","5979":"L","6168":"A","8588":"B","6169":"Q","8596":"A","8475":"B","8352":"K","8593":"Q","8907":"L","8908":"K","8901":"Y","8902":"M","8349":"B","8905":"L","8906":"K","8903":"L","8904":"B","8363":"F","8483":"K","8918":"K","8919":"M","8912":"B","8917":"B","8914":"K","8135":"K","8374":"B","8495":"L","8375":"B","8930":"K","8810":"L","8378":"K","8258":"Q","8252":"K","8370":"B","8491":"B","8371":"K","8809":"D","8924":"K","8921":"A","8801":"B","8806":"A","8805":"L","8264":"M","8028":"B","8821":"B","8027":"B","8384":"K","8936":"B","8937":"Q","8036":"B","9004":"B","9002":"L","9007":"K","8832":"L","9008":"Q","8950":"B","9005":"K","7742":"B","8830":"B","9006":"A","8031":"K","8032":"A","8709":"B","414":"A","415":"A","416":"A","5798":"B","417":"A","5799":"B","418":"A","9014":"Q","8960":"A","9015":"Q","7992":"K","9012":"Q","9013":"Q","8963":"B","8722":"K","8961":"A","9010":"Q","9011":"A","421":"A","422":"A","423":"A","7747":"B","9009":"Q","8713":"Q","8955":"B","7746":"B","7867":"K","7627":"B","7748":"B","8716":"A","8717":"A","8959":"B","8838":"K","8299":"B","8850":"B","8971":"K","8851":"B","8972":"K","8292":"B","8847":"B","6548":"Q","8602":"B","8965":"B","8845":"B","6547":"Q","8849":"B","8860":"B","8069":"B","8864":"L","8502":"B","8744":"Q","8865":"L","8862":"Q","8863":"A","9039":"B","9030":"B","8614":"B","8735":"B","8750":"B","9047":"B","9048":"B","9046":"B","8512":"B","8997":"D","9049":"B","8511":"B","9040":"A","9041":"A","9042":"K","8868":"B","7777":"K","8503":"B","8745":"A","8746":"Q","8749":"A","9058":"K","8520":"B","9059":"L","9056":"A","8880":"K","9057":"A","7796":"B","8523":"B","8524":"B","8521":"B","8522":"B","9050":"B","9051":"B","8081":"M","9054":"A","9055":"A","9052":"M","9053":"Q","8637":"B","8759":"B","8756":"K","8519":"B"}
    # orderreson={"A":"同一用户cookie24小时内重复展现","B":"订单无效或当前时间不可投放","C":"今日没有预算","D":"预算已不足","E":"投放状态错误（冻结或暂停或结束）","F":"出价过低","G":"订单对应广告主无效或状态错误","H":"订单对应广告计划无效或错误","I":"被此广告位定向过滤过滤","J":"被此广告位URL定向过滤","K":"该订单过滤该广告位媒体","L":"被订单的地域限制过滤(前台)","M":"被订单的设备限制过滤","N":"被用户频次限制过滤","O":"坑位类型不匹配","P":"没有广告着陆页地址","Q":"广告链接重复","R":"广告着陆页域名被封","S":"广告图片相似","T":"创意无效或状态错误","U":"被广告位次配置过滤","V":"没有小时预算","W":"小时预算不足","X":"广告位和广告创意等级不匹配","Y":"隐藏过滤时间","Z":"隐藏过滤地域","a":"广告订单媒体资质定向不符","b":"广告订单媒体广告位定向不符","c":"媒体不可以投放百度广告,活动不支持百度广告","d":"广告位高级屏蔽","e":"小程序广告在非小程序广告位","f":"非小程序广告在小程序广告位","g":"小于IOS最低出价配置表中","h":"活动定制过滤","i":"订单没有坑位尺寸的创意","j":"达到广告位投放数量限制","k":"托底广告主过滤","l":"商品不存在或不支持cps","m":"商品不在推广期","n":"商品CPS账户/保证金账户余额不足","o":"不是微信游戏配置订单","p":"不是微信和强推中指定的广告订单","q":"ocpa出价过低","r":"ocpa暂停","s":"媒体不支持ocpa","t":"被订单的地域限制(后台)过滤"}
    orderreson=order_reson()
    # 分组未出订单原因 字典
    count=Counter(mydit.values())
    # print count
    # 相同原因未出广告订单列表
    orderlist=[]
    alldit={}
    for (j,k) in count.items():
        for(mykey,myv) in mydit.items():
            if myv==j:
                orderlist.append(mykey)
        alldit[j]=orderlist
        orderlist=[]
    # 与错误原因的字典进行匹配替换key值
    for (j,k) in alldit.items():
        for (rj,rk) in orderreson.items():
            if j==rj:
                alldit[rk]=alldit.pop(j)
    return json.dumps(alldit, encoding='UTF-8', ensure_ascii=False)
# 根据点击id查询出所有的过滤原因的订单
def orderbylog(zclk):
    es=Elasticsearch([{"host":"221.122.127.41"}],port=9200);
    # res = es.search(index="logstash-voyagerjavalog-*", body={"query": {"zclk":"B3J3JDC11HP5D1KDOM"}, "_source": "BID_INFO"})
    body={
	"sort": {
		"@timestamp": "desc"
	},
	"size": 13,
	"query": {
		"bool": {
			"must": [{
				"query_string": {
					"query": "\"B0H3CDC01HQJHIYMTD\"",
					"analyze_wildcard": True
				}}]}}}
    body['query']["bool"]['must'][0]['query_string']['query']='path:bidding  AND message:"{0}"'.format(zclk)
    # print body
    res = es.search(index="logstash-voyagerjavalog-*", body=body)
    # print res
    tmplist=[]
    tmpwadlist=[]
    tmpdict={}
    for hit in res["hits"]["hits"]:
        # print 5555555555555555555555555555
        tmpwad=str(hit["_source"]["message"][0]).split("bid:")[1].split(", wad:")[1]
        # 不出广告订单列表
        tmpdit=str(hit["_source"]["message"][0]).split("bid:")[1].split(", wad:")[0].split("fad:")[1]
        tmpdit=eval(tmpdit)
        tmpdict[tmpwad]=tmpdit
        tmplist.append(tmpdict)
    return tmplist

# 根据点击id查询出所有的过滤原因的订单
def orderbylognew(zclk,env):
    # es=Elasticsearch([{"host":"221.122.127.41"}],port=9200);
    if env=='dev':
        es=Elasticsearch(["123.59.17.100:9200","123.59.17.221:9200",],timeout=1000);
        # es=Elasticsearch(["123.59.17.45:9200","123.59.17.158:9200","221.122.127.101:9200","221.122.127.64:9200","221.122.127.79:9200","221.122.127.83:9200",
        #                     "123.59.17.178:9200","123.59.17.78:9200","123.59.17.112:9200","123.59.18.227:9200"]);
        body={
	"sort": {
		"@timestamp": "desc"
	},
	"size": 20,
	"query": {
		"bool": {
			"must": [{
				"query_string": {
					"query": "\"B0H3CDC01HQJHIYMTD\"",
					"analyze_wildcard": True
				}}]}}}
        body['query']["bool"]['must'][0]['query_string']['query']="path:bidding AND message:\"{0}\"".format(zclk)
    if env=='test':
        es=Elasticsearch(["101.254.242.11:9200",]);
        body= { "query": {
        "query_string" : {
            "query" : "B3W1CD6H1IROZUCK81" } }}
        body['query']["query_string"]["query"]=zclk
    # print body
    time.sleep(1)
    # res = es.search(index="logstash-voyagerjavalog-*", body=body)
    res = es.search(index="logstash-voyagerjavalogwarn-*", body=body)
    # print res
    tmplist=[]
    for hit in res["hits"]["hits"]:
        if 'wad:' in str(hit["_source"]["message"]):
            tmpdict={}
            # 时间
            mytime=str(hit["_source"]["message"])[3:22]
            # 新增加的计算因子
            if 'exp'in str(hit["_source"]["message"]):
                print 11
                # 选出来的订单列表
                print 3333
                tad=str(hit["_source"]["message"]).split("tad:[")[1].split("], exp:")[0]
                exp=str(hit["_source"]["message"]).split("exp:")[1].split(", fad:")[0]
            else:
                # 选出来的订单列表
                tad=str(hit["_source"]["message"]).split("tad:[")[1].split("], fad:")[0]
                exp='{}'
            # 筛选条件
            bid=str(hit["_source"]["message"]).split("bid:")[1].split(", tad:")[0]
            #选出来的订单 wad:none
            if "},wad:"in str(hit["_source"]["message"]):
                tmpwad=str(hit["_source"]["message"]).split("},wad:")[1].split("'")[0].split(',config:')[0].split(', config:')[0]
                config=str(hit["_source"]["message"]).split("},wad:")[1].split("'")[0].split(',config:')[0].split(', config:')[1]
            if "}, wad:"in str(hit["_source"]["message"]):
                tmpwad=str(hit["_source"]["message"]).split("}, wad:")[1].split("'")[0].split(',config:')[0]
                config=str(hit["_source"]["message"]).split("}, wad:")[1].split("'")[0].split(',config:')[1]

            # 不出广告订单列表
            tmpdit=str(hit["_source"]["message"]).split("bid:")[1].split(", wad:")[0].split("fad:")[1].split(",wad")[0]
            print 22222222222
            # print tmpdit
            tmpdit=eval(tmpdit)
            tmpdict["wad"]=tmpwad
            tmpdict["tmpdit"]=tmpdit
            tmpdict["config"]=config
            tmpdict["fad"]=eval(getorderreson(tmpdit))
            tmpdict["mytime"]=mytime
            tmpdict["bid"]=eval(bid)
            tmpdict["tad"]=tad.split(",")
            tmpdict["exp"]=eval(exp)
            tmplist.append(tmpdict)
    return tmplist
# 按照订单和广告位查找 查找订单在广告位上不出现原因汇总 tad在选中列表中 wad真正选中
def allorderdit(begindate='',enddate='',adzone_id='',ad_order_id='',myenv='',adzone_click_id=''):
    # 筛选的所有广告位点击id
    if len(adzone_click_id)>0:
        # adzone_click_ids=adzone_click_id
        tpladzone=[]
        adzone_click_ids=[]
        for i in adzone_click_id:
            tpladzone=[i]
            adzone_click_ids.append(tpladzone)
    else:
        adzone_click_ids=alladzonetup(begindate,enddate,adzone_id,ad_order_id,myenv)
    myfad={}
    tadcount=0
    wadcount=0
    mydit={}
    # ad_order_id='1993'
    for i in adzone_click_ids:
        print '处理到第{}个广告位点击id'.format(str(adzone_click_ids.index(i)))
        if myenv=='dev':
            tmpdit=orderbylognew(i[0],'dev')
        else:
            tmpdit=orderbylognew(i[0],'test')
        # key为订单过滤原因 value为数量
        for dit in tmpdit:
            # print type(dit)
            # print dit['tmpdit']
            if ad_order_id in dit['tmpdit']:
                print 999999999999999
                # print dit['tmpdit']
                # print dit['tmpdit'][ad_order_id]
                if dit['tmpdit'][ad_order_id] in myfad:
                    myfad[str(dit['tmpdit'][ad_order_id])]=myfad[str(dit['tmpdit'][ad_order_id])]+1
                else:
                    myfad[str(dit['tmpdit'][ad_order_id])]=1
            # 判断订单是否在选中列表中，如果有就+1 如果没有还需要判断下个数是否大于0 如果大于0则不动，否则置为0
            if (ad_order_id in dit['tad']) :
                tadcount=tadcount+1
            else:
                if tadcount > 0:
                    tadcount=tadcount
                else:
                    tadcount=0
            mydit[u'订单在筛选列表中次数']=tadcount
            # 筛选出来的订单有可能是多个订单，比如纸巾宝接口返回4个订单，判断字符串中是否包含该订单
            if (ad_order_id == dit['wad']) or (ad_order_id in dit['wad'].split(',')) :
                wadcount=wadcount+1
            else:
                if wadcount > 0:
                    wadcount=wadcount
                else:
                    wadcount=0
            mydit[u'订单最终选中次数']=wadcount
        mydit.update(myfad)
    # print mydit
    mydit[u'广告位点击id为']=str(adzone_click_ids)
    mydit=eval(getorder_rs(mydit))
    return mydit
def alladzonetup(begindate,enddate,adzone_id,ad_orderid,myenv):
    tmptable=begindate[0:10].replace('-','')
    # print tmptable
    sql='''SELECT adzone_click_id FROM voyagerlog.ad_show_log{0} where create_time>'{1}'
     and create_time<'{2}' and adzone_id={3} limit 10'''.format(tmptable,begindate,enddate,adzone_id,)
    print sql
    if myenv=='dev':
        result=db.selectsql('devvoyager',sql)
    else:
        result=db.selectsql('testvoyager',sql)
    print result
    return result
def getadvertiser_deduction(day,orderid):
    day=day.replace('-','')
    sql=''' SELECT create_time,amount,case charge_status when '1' THEN '投放' ELSE '暂停' END 投放状态 from voyager.advertiser_balance_pre_deduction  where consumer_date='{0}' and order_id={1}
    '''.format(day,str(orderid))
    print sql
    result=db.selectsql('devvoyager',sql)
    print result
    return result

if __name__ == '__main__':
    # mydit={"6350":"Q","8894":"B","8891":"B","8892":"B","8777":"K","8895":"B","9061":"L","9062":"Y","9065":"B","8098":"M","8890":"B","9063":"Y","9064":"K","8090":"L","8648":"K","8526":"B","8768":"B","8889":"L","8783":"K","8781":"K","9078":"K","8782":"K","9079":"K","8664":"Q","8665":"D","9072":"B","9073":"B","9071":"K","9076":"K","9077":"L","9074":"K","9075":"K","8537":"A","8658":"B","8779":"K","5041":"B","8673":"A","8552":"B","8674":"Y","7343":"L","8671":"Y","8672":"Y","8793":"D","8675":"Y","7346":"L","8676":"Y","8670":"K","6491":"A","9080":"L","5956":"K","8326":"K","8323":"B","7903":"K","8332":"M","8572":"A","8457":"K","8578":"A","8214":"K","8577":"A","8570":"B","8450":"A","8448":"Q","5979":"L","6168":"A","8588":"B","6169":"Q","8596":"A","8475":"B","8352":"K","8593":"Q","8907":"L","8908":"K","8901":"Y","8902":"M","8349":"B","8905":"L","8906":"K","8903":"L","8904":"B","8363":"F","8483":"K","8918":"K","8919":"M","8912":"B","8917":"B","8914":"K","8135":"K","8374":"B","8495":"L","8375":"B","8930":"K","8810":"L","8378":"K","8258":"Q","8252":"K","8370":"B","8491":"B","8371":"K","8809":"D","8924":"K","8921":"A","8801":"B","8806":"A","8805":"L","8264":"M","8028":"B","8821":"B","8027":"B","8384":"K","8936":"B","8937":"Q","8036":"B","9004":"B","9002":"L","9007":"K","8832":"L","9008":"Q","8950":"B","9005":"K","7742":"B","8830":"B","9006":"A","8031":"K","8032":"A","8709":"B","414":"A","415":"A","416":"A","5798":"B","417":"A","5799":"B","418":"A","9014":"Q","8960":"A","9015":"Q","7992":"K","9012":"Q","9013":"Q","8963":"B","8722":"K","8961":"A","9010":"Q","9011":"A","421":"A","422":"A","423":"A","7747":"B","9009":"Q","8713":"Q","8955":"B","7746":"B","7867":"K","7627":"B","7748":"B","8716":"A","8717":"A","8959":"B","8838":"K","8299":"B","8850":"B","8971":"K","8851":"B","8972":"K","8292":"B","8847":"B","6548":"Q","8602":"B","8965":"B","8845":"B","6547":"Q","8849":"B","8860":"B","8069":"B","8864":"L","8502":"B","8744":"Q","8865":"L","8862":"Q","8863":"A","9039":"B","9030":"B","8614":"B","8735":"B","8750":"B","9047":"B","9048":"B","9046":"B","8512":"B","8997":"D","9049":"B","8511":"B","9040":"A","9041":"A","9042":"K","8868":"B","7777":"K","8503":"B","8745":"A","8746":"Q","8749":"A","9058":"K","8520":"B","9059":"L","9056":"A","8880":"K","9057":"A","7796":"B","8523":"B","8524":"B","8521":"B","8522":"B","9050":"B","9051":"B","8081":"M","9054":"A","9055":"A","9052":"M","9053":"Q","8637":"B","8759":"B","8756":"K","8519":"B"}
    # mydit={"8893":"B","9102":"D","6350":"D","8894":"B","8135":"K","9100":"D","9189":"D","7202":"K","8930":"D","7201":"K","8777":"D","8810":"L","6871":"K","8895":"B","8896":"K","9105":"D","9061":"L","9182":"L","9183":"B","9180":"L","9181":"L","9186":"L","9066":"D","8098":"B","9187":"L","8252":"K","8370":"B","9184":"K","8371":"B","9064":"K","8090":"K","8922":"D","8526":"B","8768":"B","8889":"L","8805":"L","8783":"D","8781":"D","9199":"K","8782":"D","8661":"B","8028":"B","8821":"K","8268":"K","8664":"D","8027":"K","8665":"D","9193":"D","9194":"D","9191":"D","9192":"K","8384":"K","9077":"L","9198":"B","8260":"M","9195":"B","9196":"B","9190":"K","8658":"K","8779":"D","8937":"D","8673":"D","9004":"B","8036":"B","7343":"L","8671":"Y","9002":"B","8672":"Y","8793":"D","9007":"K","8798":"B","8435":"B","8832":"K","9008":"D","9129":"K","9005":"K","8830":"B","9083":"D","9084":"B","8270":"K","9081":"L","9082":"L","7180":"K","9087":"L","8031":"K","8670":"K","9088":"K","8032":"D","9121":"L","9085":"L","6491":"B","9086":"D","5956":"K","9014":"D","9015":"D","9012":"D","7199":"K","9013":"D","8601":"B","8961":"D","9098":"D","9010":"D","9099":"D","9011":"D","9096":"L","7196":"D","9090":"B","9091":"K","8318":"B","9009":"D","8438":"K","8713":"D","8955":"K","7867":"K","7903":"K","8716":"D","8959":"B","8717":"D","8332":"D","8850":"B","8851":"B","8214":"K","8292":"B","8605":"B","6548":"B","6547":"B","8860":"B","9036":"K","8864":"K","6168":"D","8502":"B","8865":"K","9039":"B","6169":"D","8588":"B","9154":"L","9030":"K","8735":"B","8856":"K","8614":"B","9168":"K","8596":"K","9169":"D","9048":"B","9166":"B","8352":"K","9167":"B","9046":"B","8512":"B","8997":"B","8755":"B","8598":"K","8511":"B","9165":"K","8593":"K","9162":"B","8908":"K","8901":"B","7777":"K","8869":"B","8902":"B","8229":"B","8906":"K","9058":"K","8640":"B","8520":"B","9059":"L","8880":"B","9177":"B","8363":"F","9178":"B","7796":"K","8523":"B","8524":"B","8521":"B","8885":"K","8522":"B","9171":"K","9050":"B","9172":"D","9170":"D","9175":"K","9176":"B","8483":"K","9173":"K","9174":"K","8918":"K","8919":"K","8912":"B","8917":"K","8519":"B"}
    # tmpdit=orderbylognew('B2V6ZDC11JHYZHUOCH','dev')
    # tmpdit=orderbylognew('B0H3CDC11JI6THVHY9','dev')
    tmpdit=orderbylognew('B0H3ADC11JI7R5RBT0','dev')
    print tmpdit
    # result=allorderdit('2019-03-15 11:25:03','2019-03-15 11:25:10','3397','27841','dev')
    # print '1111111111111'
    # res=getadvertiser_deduction('2019-07-23','22833')
    # for i in res:
    #     print i[0]
        # print type(i[0])
    # ts=getorder_rs(result)
    # print ts
    # print mydit
    # print tmpdit
    # print len(tmpdit)
    # for i in tmpdit:
    #     print i['tad']
    # print tmpdit
    # print type(tmpdit[0])
    # print type(tmpdit[0]["wad"])
    # print type(tmpdit[0]["fad"])
    # print type(tmpdit[0]["mytime"])
    # print type(tmpdit[0]["bid"])
    # print type(tmpdit[0]["tad"])
    # print type(tmpdit['tad'])


    # tmpalldict={}
    # for i in tmpdit:
    #     for (j,k) in i.items():
    #         # print j
    #         # print getorderreson(k)
    #         tmpalldict[j]=getorderreson(k)
    # print tmpalldict


        # print getorderreson(i)


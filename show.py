#!/usr/bin/env python
#encoding: utf-8
#version:2018/07/10,增加接口统计视图函数
import os

from flask import jsonify,redirect,session
from flask import Flask,request,render_template,flash
from business_modle.report import hdtmonitor as m
from business_modle.testtools import hdt_cssc as cssc
from business_modle.report import reportdata as r
from business_modle.report import tuodi_day_order as myorder
from business_modle.launch import launchlistdb as lc
from business_modle.querytool import bidding_analysis as ba
from business_modle.querytool.confparas import *
from business_modle.querytool.get_act import *
from business_modle.querytool.updateAdId import *
from business_modle.querytool.QueryAppkey import *
from business_modle.report import tuodi_oneviw as tuodi_oneviw
from business_modle.testtools import houtai as ht
from business_modle.querytool import plantfromwtf as ft
from business_modle.querytool.plantfromwtf import *
from business_modle.VersionTracker.VersionTracker import VersionTracker
from business_modle.testtools.Recharge import *
from business_modle.testtools.cpa_api import *
from business_modle.querytool.crm_order import *
from business_modle.testtools.adinfo_collect import *
from business_modle.testtools.del_minipragram import *
from business_modle.testtools.auto_activity import *
from utils.Emar_SendMail_Attachments import *
from config import mail_template,sqls
from business_modle.Crm.CrmOrderEffectCheck import Crm
from business_modle.querytool.phoneVaildCode import *
from bp.hdt_act.hdt_act import act
from bp.hdt_redis.hdt_redis import  hdtredis
from bp.miniprogram.miniprogram import miniprogram
from bp.ocpa.ocpa import ocpa
from bp.test_case.test_case import testCase
#引用亿起发类
from bp.yiqifa.finance import *
from bp.yiqifa.cdp import *
from bp.yiqifa.shortjump import *
from bp.yiqifa.egoubaobei import *
from business_modle.querytool.orderQueryCreative import *
from bp.TestToolsTracker.ToolsTracker import ToolsTracker
from business_modle.querytool.report_byadzone import *
from bp.TestToolsTracker.ToolsTrackerForm import ToolsTrackerForm
from business_modle.querytool.ddyzinfo import *
from bp.tools.tools import *
from bp.login.login import mylogin
from bp.miniprogram.activity_form import *

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC_TXT = os.path.join(APP_ROOT, 'txt') #设置一个专门的类似全局变量的东西
app = Flask(__name__)
#将亿起发蓝图注册到app
app.register_blueprint(Finace,url_prefix='/finace')
app.register_blueprint(cdpRoute,url_prefix='/cdp')
app.register_blueprint(shortJumpRoute,url_prefix='/yiqifa')
app.register_blueprint(egoubaobei,url_prefix='/yiqifa')
#将活动蓝图注册到app
app.register_blueprint(act,url_prefix='/act')
app.register_blueprint(hdtredis,url_prefix='/hdtredis')
app.register_blueprint(ocpa,url_prefix='/ocpa')
app.register_blueprint(miniprogram,url_prefix='/miniprogram')
app.register_blueprint(testCase,url_prefix='/tc')
app.register_blueprint(tools,url_prefix='/tools/jobAdReason')
app.register_blueprint(mylogin,url_prefix='/login')
app.register_blueprint(tools,url_prefix='/tools')


# app.jinja_env.add_extension("chartkick.ext.charts")
# app.config.from_object('config')
# app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config.from_object('config')
@app.route('/monitor/yiqifahoutaif/<fname>', methods=['GET'])
def yiqifa_houtai1(fname):
    # filenanme='f1.txt'
    # print type(str(fname))
    fname=fname.encode('utf-8')
    # print type(fname)
    # print fname
    f=open('log/'+fname)
    s=f.readlines()
    f.closed
    return  render_template("file.html",user='aaa',title = 'Home',posts = s)
@app.route('/monitor/filelistok/', methods=['GET'])
def filelist():
    flist=ht.filelist(r'D:\work\auto\yiqifa\test_case\wending\log')
    # print flist
    return render_template('flist.html',filelist=flist)
@app.route('/monitor/yiqifahoutai')
def yiqifahoutai():
    f=open('f1.txt')
    s=f.readlines()
    # yield '',.join(s)+'\n'
    # sorted(student_tuples, key=itemgetter(2), reverse=True)
    sorted(s,reverse=True)
    f.closed
    return  render_template("file.html",title = 'yiqifahoutai',posts = s)
@app.route('/monitor/error/<err_msg>')
def error(err_msg):
    # err_msg1=err_msg
    # return err_msg
    # print type(err_msg)
    err_msg=err_msg.encode('unicode-escape').decode('string_escape')
    # print type(err_msg)
    # print err_msg
    return render_template('error.html',err_msg1=err_msg)
# 托底广告
@app.route('/adtuodi1/<days>')
def adtuodi(days):
    title=u'托底'
    # xvalue=['Acccc','B','C','d']
    # dat=[1000,1200,1300,1000]
    xvalue,dat,tmpsqllist=r.mydb(days)
    # return "ttttttt"
    return render_template('highchartsline.html',xvalue=xvalue,title=title,data=dat,tmpsqllist=tmpsqllist)

# 托底广告订单按照时间分布
@app.route('/adtuodiorder/')
def adtuodiorder():
    title=u'托底订单按照时间分布'
    # xvalue=['Acccc','B','C','d']
    # dat=[1000,1200,1300,1000]
    day=request.args.get('day')
    order=request.args.get('order')
    xvalue,dat,tmpsqllist,adtuodi_order,adtuodi_order_count=myorder.mydb(int(day),int(order))
    # return "ttttttt%s，%s"%(str(day),str(order))
    return render_template('tuodi_day_order.html',xvalue=xvalue,title=title,data=dat,tmpsqllist=tmpsqllist,adtuodi_order=adtuodi_order,adtuodi_order_count=adtuodi_order_count)
# 按照广告主展示广告投放
@app.route('/ad_by_advertiser_id/')
def testhightchar():
    day=request.args.get('day')
    advertiser_id=request.args.get('advertiser_id')
    (xvalue,data,sql)=tuodi_oneviw.mydbnew(int(day),str(advertiser_id))
    print xvalue,data
    return render_template('ad_by_advertiser_id.html',xvalue=xvalue,d=data,sql=sql)
@app.route('/')
def index():
    print 'ok'
    return render_template("index.html")
@app.route('/summary/')
# 简介介绍
def summary():
    return render_template('summary.html')
@app.route('/flistok', methods=['GET'])
def flistok():
    path=r'd:'
    flist=os.walk(path)
    # return json.dumps(flist)
    print flist
    return render_template('flist.html',flist=flist)
# 互动推监控
@app.route('/hdtmonitor/',methods=['GET','POST'])
def hdtmonitor():
    if request.method=='GET':
        # print days
        return render_template('hdtmonitor.html')
    else:
        if request.form.get('myday')=='':
             days=0
        else:
            days=int(request.form.get('myday'))
        jobid=request.form.get('jobid')
        mytitle=''
        if jobid=='44':
            mytitle=u'展现/抽奖'
        # elif jobid=='45':
        #     mytitle=u'谢谢参与次'
        elif jobid=='46':
            mytitle=u'托底广告次数'
        elif jobid=='47':
            mytitle=u'点击/展现'
        elif jobid=='48':
            mytitle=u'负数个数/总个数'
        elif jobid=='45':
            mytitlemedia=u'谢谢参与数媒体分布'
            mytitle=u'谢谢参与次'
            xvaluemedia,datamedia=m.mymedia(days,'media_id','0')
            xvalue,dat,tmpsqllist=m.mydb(days,jobid)
            return render_template('hdtmonitor.html',xvalue=xvalue,mytitle=mytitle,data=dat,tmpsqllist=tmpsqllist,xvaluemedia=xvaluemedia,mytitlemedia=mytitlemedia,datamedia=datamedia)
        elif jobid=='100':
            mytitlemedia=u'媒体中广告位谢谢参与汇总'
            mediaid=str(request.form.get('mymediaid'))
            xvaluemedia,datamedia=m.mymedia(days,'adzone_id',mediaid)
            return render_template('hdtmonitor.html',xvaluemedia=xvaluemedia,mytitlemedia=mytitlemedia,datamedia=datamedia)
        elif jobid=='110':
            redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
            mybudget=myredis.getredis(redis_nodes)
            return render_template('hdtmonitor.html',mybudget=mybudget)
        xvalue,dat,tmpsqllist=m.mydb(days,jobid)
        return render_template('hdtmonitor.html',xvalue=xvalue,mytitle=mytitle,data=dat,tmpsqllist=tmpsqllist)
@app.route('/link/')
def link():
    return render_template('link.html')
@app.route('/hdt_cssc/',methods=['GET','POST'])
def hdt_cssc():
    if request.method=='GET':
        # alladzon=((59L, 101L, '172.16.145.55', 55L, None, 69L, 69L),(59L, 101L, '172.16.145.55', 55L, None, 69L, 69L))
        # for trcout in alladzon:
        #     print trcout
        return render_template('hdt_cssc.html')
    else:
        dbtype=request.form.get('dbtype')
        adzone_click_id=request.form.get('adzone_click_id')
        if request.form.get('myday')=='':
             days=0
        else:
            days=int(request.form.get('myday'))
        alladzon=cssc.mydata(days,dbtype,'adzon',adzone_click_id)
        alllottery=cssc.mydata(days,dbtype,'lottery',adzone_click_id)
        allshow=cssc.mydata(days,dbtype,'show',adzone_click_id)
        allclick=cssc.mydata(days,dbtype,'click',adzone_click_id)
        award_show=cssc.mydata(days,dbtype,'award_show',adzone_click_id)
        return render_template('hdt_cssc.html',alladzon=alladzon,alllottery=alllottery,allshow=allshow,allclick=allclick,award_show=award_show)
@app.route('/hdtapi/',methods=['GET','POST'])
def hdtapi():
    if request.method=='GET':
        print 1111111111
        return render_template('allapi.html')
    else:
        jobid=request.form.get('jobid')
        cmd='''python D:\\work\\auto\\Voyager\\all_tests.py'''
        cmdhdtui='''python D:\\work\\auto\\\Voyageractivity\\all_tests.py'''
        # cmd='''python all_tests.py'''
        if jobid=='100':
            try:
                os.system(cmd)
                data='调用测试环境apidisplay自动化测试case成功'
            except Exception as e:
                print e.message
                data=e.message
        elif jobid=='200':
            try:
                os.system(cmdhdtui)
                data='调用测试环境apidisplay自动化测试case成功'
            except Exception as e:
                print e.message
                data=e.message
        elif jobid=='300':
            try:
                # 调用接口执行国内生产环境自动化测试
                r=requests.get('http://172.16.106.12:3333/auto/')
                data=u'调用接口执行国内生产环境自动化测试成功'
            except Exception as e:
                print e.message
                data=e.message
        elif jobid=='400':
            try:
                # 调用接口执行国内生产环境自动化测试
                r=requests.get('http://172.16.106.17:3333/auto/')
                data=u'调用接口执行新加坡生产环境自动化测试成功'
            except Exception as e:
                print e.message
                data=e.message
        return render_template('allapi.html',data=data)

@app.route('/voyagerlog/',methods=('POST','GET'))
def voyagerlog():
    zclk=request.form.get('zclk')
    if request.method=='GET':
        return render_template('voyagerlog.html')
    else:
        tmpdit=ba.orderbylognew(zclk)
        print 99999999999999999999999
        print tmpdit
        # data=ba.getorderreson(tmplist)
        tmpdata=[]
        # tmpalldit={}
        # for i in tmpdit:
        #     for (j,k) in i.items():
        #         tmpalldit[j]=eval(ba.getorderreson(k))
        #     # tmpdata.append(tmpalldit)
        # print "2333333333333333333333333333333337777777777777"
        # print tmpalldit
        return render_template('voyagerlog.html',data=tmpdit)
@app.route('/voyagerlog1/',methods=('POST','GET'))
def voyagerlog1():
    form = ft.MyForm()
    tmpdit=''
    if form.validate_on_submit():
        zclk=form.data['adzoneClickid']
        env = form.data['myenv']
        tmpdit=ba.orderbylognew(zclk,str(env))
        return render_template('voyagerlog1.html',form=form,data=tmpdit)
    return render_template('voyagerlog1.html',form=form)

@app.route('/reportlist/',methods=('POST','GET'))
def reportlist():
    if request.method=='GET':
        reportlist='''Report.html'''
        return render_template(reportlist)
# http://display.eqigou.com:21312/baidujs/
@app.route('/baidujs/')
@app.route('/1111/')
def baidujs():
    return render_template('baidujs.html')
@app.route('/jssdk/')
def jssdk():
    return render_template('jssdk.html')
@app.route('/launchlist/',methods=['GET','POST'])
def launchlist():
    form=ft.Mylaunchlist()
    x=form.myyear
    if form.is_submitted():
        year=form.myyear.data
        month=form.mymonth.data
        #增加两个字段
        group_id = form.groups.data
        tester_name = form.testers.data
        print month,year
        reslut=lc.getlanuchlist(int(year),int(month),int(group_id),tester_name)
        if len(reslut)>0:
            lc.exportXls(reslut)
        return render_template('launchlist.html',form=form,result=reslut)
    else:
        return render_template('launchlist.html',form=form,result='')

@app.route('/launchlistadd/')
def launchlisadd():
    group=request.args.get('group')
    project=request.args.get('project')
    src_version=request.args.get('src_version')
    Changes=request.args.get('Changes')
    tmpsql=lc.lanuchlisttmpsql(group,project,src_version,Changes)
    try:
        lc.instertsql(tmpsql)
        return jsonify({'code':200})
    except:
        return jsonify({'code':500})
@app.route('/getlanuch/')
def getlanuch():
    id=request.args.get('id')
    result=lc.getlanuch(id)
    return render_template('launchdetial.html',result=result)

@app.route('/confparas/', methods=['POST','GET'])
def confparas():
    title = u'数据库config_parameters配置表'
    if request.method=='GET':
        return render_template("confparas.html",title = title)
    else:
        env = request.form.get('env').strip()
        env_dict={u'测试环境':True,u'生产环境':False}
        print(env_dict[env])
        paras = ConfParas(env_value=env_dict[env]).manager_paras()
        return render_template('confparas.html', title = title, paras = paras,env = env)

@app.route('/ad_simulation/',methods=['post','get'])
def ad_simulation():
    #如果需要增加查询字段，分别在ad_simulation.html中增加显示该字段，在get_act.py中chk_dict增加映射关系
    title ='模拟投放接口查询'
    if request.method == 'GET':
        return render_template("ad_simulation.html", title=title)
    else:
        env_dict={u'测试环境':'T', u'生产环境':'P'}
        env = request.form.get('env').strip()
        adzoneID = request.form.get('adzoneID')
        adOrderID = request.form.get('adOrderId')
        chklist = request.form.getlist('chklist')
        if adzoneID and chklist:
            final = get_ad_simulation_info(adzoneID, adOrderID, chklist, env_value=env_dict[env])
            print('===========',final)
            #chklist返回的为表头，final_k返回的为[[id,id,id],[id,id]] ，final_len返回的有多少个广告
            if isinstance(final,dict):
            # if adzoneID in final:
                chklist.insert(0, u'序号')
                return render_template("ad_simulation.html", title=title, chklist=chklist ,final_k=final.values(),final_len=range(len(final)))
            else:
                print( u'序号')
                return render_template("ad_simulation.html", title=title, emsg=final, knowledge=knowlegde())
        else:
            return render_template("ad_simulation.html", title=title,emsg='请输入广告位id或勾选关键字')


@app.route('/updateAdId/',methods=['POST','GET'])
def UpdateAdId():
    title = u'更新广告主ID'
    if request.method=='GET':
        return render_template("UpdateAdId.html",title=title)
    else:
        BeAd=request.form.get('BeforeAdID')
        AfAd=request.form.get('AfterAdID')
        print(BeAd)
        ua=updateAdId(BeAd,AfAd)
        ua.udpate()
        up_advertiser=ua.select()
        return  render_template("UpdateAdId.html",up_advertiser=up_advertiser,title=title)
@app.route('/queryAppkey',methods=['POST','GET'])
def QueryAppkey():
    title = u'查询广告位Appkey'
    if request.method=='GET':
        return render_template("QueryAppkey.html",title=title)
    else:
        env_dict={u'测试环境':True,u'生产环境':False}
        env=request.form.get('env').strip()
        Adzone_id=request.form.get('Adzone_id')
        print Adzone_id
        qa=QueryAppKey(Adzone_id,env_dict[env])
        appkey=qa.queryAppKey()

        return render_template("QueryAppkey.html",appkey=appkey,title=title,Adzone_id=Adzone_id,env_value='<option selected="selected">'+env+'</option>')

@app.route('/test/')
def test():
    return render_template("test.html")
@app.route('/myiframe/')
def myiframe():
    return render_template("myiframe.html")

@app.route('/version_maintain/<any(new,update):page_name>/',methods=('POST','GET'))
def version_maintain(page_name):
    form = VersionTrackerForm()
    vt = VersionTracker()
    if page_name == 'new':
        if form.is_submitted():
            sql_data = form.data
            print sql_data
            sql_data.pop('csrf_token')
            sql_data.pop('submit')
            #处理多个tester_id的情况,将ids处理为1,2,3的形式
            tester = json.dumps(sql_data['tester'], encoding='utf-8', ensure_ascii=False)[1:-1].replace("\"", "").replace(" ","")
            #使用update将字典tester的值更新
            sql_data.update(tester=tester)
            keys = tuple(sql_data.keys())
            values_list = json.dumps(sql_data.values(), encoding='utf-8', ensure_ascii=False)
            re = vt.insert_version(values_list, keys)
            # re=1
            #根据一个或多个测试人员信息，判断发送者的信息
            f_tester=''
            t_tester = str(tester).split(',')
            if len(t_tester) >= 2:
                f_tester=t_tester[0]
            else:
                f_tester=tester
            if re != 0:
                msg = '添加成功'
                if int(form.data['send_email']) != 0:
                    #拼装邮件内容申请者姓名、审批者姓名和邮件发送者的拼音、jobname信息
                    applicant = vt.get_user_ch_name(sqls['applicant_ch_name'].format(form.data['applicant_id']))[0]
                    approver = vt.get_user_ch_name(sqls['applicant_ch_name'].format(form.data['approver']))[0]
                    #取邮件发送者的全拼信息
                    sender = vt.get_user_ch_name(sqls['ch_name'].format(f_tester))[1]
                    print sender
                    job_name = vt.get_jenkins_job(sqls['jenkins_name'].format(form.data['job_id']))[0][0]
                    send_email(mail_template['normal'], form.data, applicant, approver,sender,job_name)
                    flash("send mail Success")
                else:
                    flash("send mail Success")
            else:
                msg = '添加失败'
                flash("send mail Fali")
            return render_template('VersionTracker/version_maintain.html', form=form, msg=msg)
        return render_template('VersionTracker/version_maintain.html',form = form)
    else:
        print request.form.get('status'),request.form.get('v_desc'),request.form.get('id'),request.form.get('job_name'),request.form.get('tester')
        id = request.form.get('id')
        status = request.form.get('status')
        v_desc = request.form.get('v_desc')
        tester = request.form.get('tester').strip().replace('，',',')
        re=vt.update_version_desc_state(id,status,v_desc,tester)
        if int(re) != 0:
            flash("update Success")
            result=lc.getlanuch(id)
            return render_template("launchdetial.html",result=result)
        else:
            flash("update Falied")
            result=lc.getlanuch(id)
            return render_template("launchdetial.html",result=result)

@app.route('/version_stat/')
def version_stat():
    vt = VersionTracker()
    re = vt.get_version_stat()
    print re
    return render_template("VersionTracker/version_stat.html",re=re)

@app.route('/recharge',methods=['POST','GET'])
def recharge():
    title=u'测试环境模拟联动充值'
    if request.method=='GET':
        return render_template('recharge.html',title=title)
    else:
        advertiser_id = request.form.get('advertiser_id')
        amount=request.form.get('amount')
        re=Recharge(advertiser_id,amount)
        re.localtime()
        re.balance()
        result=re.insert()
        paras=re.manage_review()

        # advertiser_result=re.showreview()[0]
        # recharge_amount=re.showreview()[1]
        # rebate_ratio=re.showreview()[2]
        # rebate_begin=re.showreview()[3]
        # rebate_end=re.showreview()[4]

        return render_template("recharge.html",result=result,title=title,paras=paras)

@app.route('/crm_order',methods=['POST','GET'])
def crm_order():

    title=u'优品购订单统计'
    if request.method=='GET':
        return render_template('crm_order.html',title=title)
    else:
        begin_time = request.form.get('begin_date')
        end_time = request.form.get('end_date')
        beign_time_re=begin_time.replace('-','')
        end_time_re=end_time.replace('-','')
        result_order= Crm_order(beign_time_re,end_time_re,env_value=False)
        paras=result_order.show_result()

        return render_template("crm_order.html",title=title,paras=paras,begin_time=beign_time_re,end_time=beign_time_re,begintime=begin_time,endtime=end_time)

@app.route('/cpa_api',methods=['POST','GET'])
def cpa_api():
    title=u'CPA回调接口测试'
    if request.method == 'GET':
        return render_template('cpa_api.html',title=title)
    else:
        ad_choosen_tag = request.form.get('choosen_tag')
        timestamp=request.form.get('datetime')
        timestamp_new=timestamp+":00"
        timestamp_fal=timestamp_new.replace('T',' ')
        device_id= request.form.get('device_id')
        result1 = Cpa_api(ad_choosen_tag,device_id,timestamp_fal,env_value=True)
        result=result1.cpa_api()
        time.sleep(5)
        paras=result1.show_result()
        return render_template("cpa_api.html",title=title,result=result,timestamp=timestamp,paras=paras,ad_choosen_tag=ad_choosen_tag,device_id=device_id)

@app.route('/render_link',methods=['POST','GET'])
def render_link():
    title = u'广告主数据收集(生成链接)'
    if request.method == 'GET':
        return render_template('advertiser_test.html',title=title)
    else:
        ad_link = request.form.get('url')
        result1 = Advertiser_collect(ad_link,env_value=False)
        ad_click_tag = request.form.get('ad_click_tag')
        utm_click = result1.click_tag()
        print result1
        new_url = str(ad_link)+'?utm_source=hudongtui&utm_click='+str(utm_click)
        paras = result1.show_result()
        print paras

        return render_template("advertiser_test.html",title=title,url=ad_link,new_url=new_url,ad_click_tag=utm_click)

@app.route('/query_result',methods=['POST','GET'])
def query_result():
    title = u'广告主数据收集(查询结果)'
    if request.method == 'GET':
        return render_template('advertiser_test.html',title=title)
    else:
        ad_link = request.form.get('url')
        ad_click_tag = request.form.get('ad_click_tag')
        result1 = Advertiser_collect(ad_link,env_value=False)
        utm_click = result1.click_tag()
        print result1
        paras = result1.show_result()
        new_url = str(ad_link)+'?utm_source=hudongtui&utm_click='+str(utm_click)
        print paras

        return render_template("advertiser_test.html",title=title,url=ad_link,new_url=new_url,paras=paras,ad_click_tag=utm_click)


@app.route('/crm/effect_order/',methods=['GET','POST'])
def effect_order():
    if request.method=='POST':
        date = request.form.get('date')
        ceo=Crm(date)
        re=ceo.cmp_infos(ceo.check_info())
        if re['data']:
            return render_template('Crm/CrmOrderEffectCheck.html',re=re,effect=re['data'][0][0],order=re['data'][1][0])
        else:
            return render_template('Crm/CrmOrderEffectCheck.html', re=re)
    else:
        return render_template('Crm/CrmOrderEffectCheck.html',re={})

@app.route('/del_minipragram',methods=['POST','GET'])
def del_minipragram():
    title=u"删除小程序相关数据"
    if request.method == 'GET':
        return render_template('del_minipragram.html',title=title)
    else:
        openid = request.form.get('openid')

        del_result= Del_minipragram(openid,env_value=True)

        para=del_result.del_sql()
        return render_template('del_minipragram.html',openid=openid,para=para)


@app.route('/phoneVaildCode/',methods=['get','post'])
def phoneVaildCode():
    if request.method=='GET':
        pp = phoneVaild(env='1')
        re = pp.get_valid_code()
        return render_template('phoneVaildCode.html', re=re,pos='1')
    else:
        env = request.values.getlist('env')
        print env[0]
        pp = phoneVaild(env=env[0])
        re = pp.get_valid_code()
        return  render_template('phoneVaildCode.html',re=re,pos=env[0])


@app.route('/orderQueryCreative/',methods=['get','post'])
def orderQueryCreative():
    if request.method=='GET':
        return render_template('orderQueryCreative.html')
    else:
        orderId = request.form.get("orderId").strip()
        creativeUrl = request.form.get("creativeUrl").strip()
        creativeId = request.form.get("creativeId").strip()
        print orderId
        env = request.values.getlist('env')
        print env[0]
        pp = orderCreativeQuery(orderId,env[0])
        if orderId:
            re = pp.queryCreative()
            if isinstance(re,list):
                return render_template("orderQueryCreative.html", re=re,type=1)
            else:
                return render_template("orderQueryCreative.html",type=0)
        if creativeUrl:
            re = pp.queryByCreative(creativeUrl=creativeUrl)
        if creativeId:
            re = pp.queryByCreative(creativeId=creativeId)
        if isinstance(re,list):
            return render_template("orderQueryCreative.html", re=re, type=2)
        else:
            return render_template("orderQueryCreative.html", type=0)


# @app.route('/ttt/<int:post_id>',methods=['get','post'])
# def test_tools_tracker(post_id):
#     form = ToolsTrackerForm()
#     tt = ToolsTracker()
#     re = tt.get_tracker_list()
#     if request.method == 'POST':
#         if post_id == 0:
#             form_datas = form.data
#             form_datas.pop('csrf_token')
#             tt.add_tools_tracker(form_datas)
#             re = tt.get_tracker_list()
#             return render_template('TestToolsTracker.html', re=re, re_len=range(len(re)), form=form)
#     else:
#         if post_id == 0:
#             return render_template('TestToolsTracker.html', re=re, re_len=range(len(re)), form=form)
#         else:
#             re = tt.get_tools_tracker(post_id)
#             return '123333'

@app.route('/ttt/',methods=['get','post'])
def test_tools_tracker():
    form = ToolsTrackerForm()
    tt = ToolsTracker()
    re = tt.get_tracker_list()
    if request.method == 'POST':
        form_datas = form.data
        form_datas.pop('csrf_token')
        tt.add_tools_tracker(form_datas)
        re = tt.get_tracker_list()
        return render_template('TestToolsTracker.html', re=re, re_len=range(len(re)), form=form)
    else:
        return render_template('TestToolsTracker.html', re=re, re_len=range(len(re)), form=form)

@app.route('/report_byadzone/',methods=['get','post'])

def report_byadzone():



    if request.method == 'POST':
        begin_date=request.form.get('begin_date')
        adzone_id = request.form.get('adzone_id')
        rd=Report_byadzone(adzone_id,begin_date,False)

        if adzone_id == '0':
            paras=rd.show_result2()

        else:
            paras=rd.show_result()


        return render_template('report_byadzone.html',paras=paras,begin_date=begin_date,adzone_id=adzone_id)

    else:

        return render_template('report_byadzone.html')


@app.route('/auto_activity/',methods=['get','post'])

def auto_activity():

    title=u'自动化活动管理'
    form=activity_form()

    ma=manage_activity()
    re=ma.activity_list()

    if request.method == 'GET':

        return render_template('auto_activity.html', re=re, re_len=range(len(re)), form=form)
    else:

        form_datas = form.data
        form_datas.pop('csrf_token')
        ma.add_activity(form_datas)
        re =ma.activity_list()
        return render_template('auto_activity.html', re=re, re_len=range(len(re)), form=form)









@app.route('/ddyzinfo',methods=['get','post'])
def ddyzinfo():
    if request.method == 'GET':
        return render_template('ddyzinfo.html')
    else:
        userid = request.form.get('userid')
        myenv=request.form.get('env')
        pp = YzInfo(userid,env=myenv)
        re = pp.show_result()
        return render_template('ddyzinfo.html',re=re)
#登录权限判断
@app.before_request
def islogin():
    businessuser=['lishichun','qiuting','zhounan']
    businessuser1=['houlixiu','meijieyunying']
    if request.path=='/login/login111/':
        return None
    if not session.get('username'):
        return redirect('/login/login111/')
    # 报表
    if (session.get('username') in businessuser) :
        if (request.path != '/report_byadzone/'):
            return redirect('/report_byadzone/')
        # else:
        #     return redirect('/report_byadzone/')
        # if ( request.path !='/hdtredis/myredis_status/'):
        #     return redirect('/hdtredis/myredis_status/')

    if (session.get('username') in businessuser1) & (request.path !='/hdtredis/orderr/'):
        return redirect('/hdtredis/orderr/')


if __name__ == '__main__':
    app.run( host="0.0.0.0",port=21312,debug=True,threaded=True)
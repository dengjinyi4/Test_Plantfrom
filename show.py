#!/usr/bin/env python
#encoding: utf-8
#version:2018/07/10,增加接口统计视图函数
import os
import traceback

from flask import jsonify
from flask import Flask,request,render_template,flash
# from flask_paginate import Pagination,get_page_parameter

from business_modle.report import hdtmonitor as m
from business_modle.testtools import hdt_cssc as cssc
from business_modle.report import reportdata as r
from business_modle.report import tuodi_day_order as myorder
from business_modle.launch import launchlistdb as lc
from business_modle.querytool import bidding_analysis as ba
from business_modle.querytool import myredis as mr
from business_modle.querytool import myredis_status as mrs
from business_modle.querytool.create_template import *
from business_modle.querytool.myException import *
from business_modle.querytool.confparas import *
from business_modle.querytool.get_act import *
from business_modle.querytool.updateAdId import *
from business_modle.querytool.QueryAppkey import *
from business_modle.report import tuodi_oneviw as tuodi_oneviw
from business_modle.testtools import houtai as ht
from business_modle.querytool import plantfromwtf as ft
from business_modle.querytool.plantfromwtf import *
from business_modle.apitool.apiTool import *
from business_modle.VersionTracker.VersionTracker import VersionTracker
from business_modle.testtools.Recharge import *
from business_modle.testtools.cpa_api import *
from business_modle.querytool.crm_order import *
from business_modle.querytool.adjust_ocpa import *
from business_modle.querytool.ocpa_order import *
from business_modle.querytool.punchcard import *
from business_modle.querytool.mini_mediainfo import  *
from business_modle.testtools.adinfo_collect import *
from business_modle.testtools.del_minipragram import *
from utils.Emar_SendMail_Attachments import *
from config import mail_template,sqls
from business_modle.Crm.CrmOrderEffectCheck import Crm
from business_modle.querytool.phoneVaildCode import *
from business_modle.checkRoute.checkRouteForm import *
from business_modle.checkRoute.checkRoute import checkNodeRoute
from business_modle.templateToAct.templateAct import templateAct
from business_modle.templateToAct.templateActForm import templateActForm

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC_TXT = os.path.join(APP_ROOT, 'txt') #设置一个专门的类似全局变量的东西
app = Flask(__name__)
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
@app.route('/myredis/',methods=('POST','GET'))
def myredis():
    if request.method=='GET':
        return render_template('myredis.html')
    else:
        jobid1=request.form.get('jobid')
        # mybudget=''
        # if jobid1=='120':
        #     data='<option selected="selected">缓存中的订单预算：生产</option>'
        #     redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
        #     # mybudget,allcount,negativecount=mr.mygetredis(redis_nodes)
        #     # return render_template('myredis.html',mybudget=mybudget,allcount=allcount,negativecount=negativecount)
        # elif jobid1=='110':
        #     data='<option selected="selected">缓存中的订单预算：测试</option>'
        #     # redis_nodes=[{"host":'172.16.105.11',"port":'17001'},{"host":'172.16.105.12',"port":'17001'},{"host":'172.16.105',"port":'17001'}]
        #     redis_nodes=[{"host":'101.254.242.12',"port":'17001'},]
        mybudget,allcount,negativecount=mr.mygetredis(jobid1,'voyager:budget')
        return render_template('myredis.html',mybudget=mybudget,allcount=allcount,negativecount=negativecount,jobid1=jobid1)

@app.route('/budget_control/')
def budget_control():
    adorder=request.args.get('orderno')
    key='voyager:budget_control:'+str(adorder)
    jobid1=request.args.get('jobid1')
    print key
    tmp_total,tmp_rest=mr.mygetredis(jobid1,key)
    # 当前小时
    myhour=int(time.strftime("%H", time.localtime()))
    return render_template('buggetcontrol.html',tmp_total=tmp_total,tmp_rest=tmp_rest,myhour=myhour)
@app.route('/ocpa_orderadzone/',methods=('POST','GET'))
def ocpa_orderadzone():
    if request.method=='GET':
        # 生产环境
        tmpordeadzon=mr.mygetredis('1','voyager:ocpa_adzones')
        return render_template('ocpaorderadzone.html',tmpordeadzon=tmpordeadzon)
@app.route('/myredis_status/',methods=('POST','GET'))
def myredis_status():
    if request.method=='GET':
        return render_template('myredis_status.html')
    else:
        jobid1=request.form.get('jobid')
        # mybudget=''
        if jobid1=='120':
            data='<option selected="selected">缓存中的订单状态：生产</option>'
            redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
            # mybudget,allcount,negativecount=mr.mygetredis(redis_nodes)
            # return render_template('myredis.html',mybudget=mybudget,allcount=allcount,negativecount=negativecount)
        elif jobid1=='110':
            data='<option selected="selected">缓存中的订单状态：测试</option>'
            redis_nodes=[{"host":'101.254.242.11',"port":'17001'},{"host":'101.254.242.12',"port":'17001'},{"host":'101.254.242.17',"port":'17001'}]
        order_status,allcount,negativecount=mrs.mygetredis(redis_nodes)
        return render_template('myredis_status.html',order_status=order_status,allcount=allcount,negativecount=negativecount,data=data)




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

@app.route('/create_act/', methods=['POST','GET'])
def create_act():
    if request.method=='GET':
        return render_template("create_act.html", template_adr='1111')
    else:
        template_adr= request.form.get('template_adr').strip()
        css_adr =  request.form.get('css_adr').strip()
        template_type_name=request.form.get('template_type_name').strip()
        temlate_name=request.form.get('temlate_name').strip()
        #增加模板配置字段
        template_conf_items= str(request.form.get('template_conf_items')).strip()
        act_name=request.form.get('act_name').strip()
        award_num =int(request.form.get('award_num'))
        free_num = int(request.form.get('free_num').strip())
        request.accept_charsets
        try:
            ct = TemplateActCreation(template_type_name, act_name,award_num)
            # 创建模板类型，create_template_type(self, classifi, locationAdress, preview="https://img0.adhudong.com/template/201802/24/999337a35a1a9169450685cc66560a05.png",prizesNum=6)
            template_type_re = ct.create_template_type(template_adr)
            if template_type_re.json()['code'] == 200:
                template_type_fe = '创建模板类型【' +template_type_name + '】,成功了，返回结果是: \n' + template_type_re.text
            else:
                raise myException('create_template_type ', template_type_re.text)

            # 创建模板 ct.create_template(templateName, templateStyleUrl)
            temlate_name_re = ct.create_template(temlate_name, css_adr, template_conf_items=template_conf_items)
            print(temlate_name_re)
            if temlate_name_re.json()['code'] == 200:
                temlate_name_fe = '创建模板【' + temlate_name + '】,成功了，返回结果是: \n' + temlate_name_re.text
            else:
                # raise myException('create_template ', temlate_name_re.text)
                raise myException('create_template ', temlate_name_re)

            # # 创建活动，create_act(self, act_name,free_num=20, award_num=6)
            act_re = ct.create_act(free_num)
            print(act_re)
            if act_re.json()['code'] == 200:
                act_fe = '创建活动【' + act_name + '】,成功了，返回结果是: \n' + act_re.text
            else:
                raise myException('create_act ', act_re.text)

            # # 创建活动关联的奖品，
            awards_re = ct.create_awards()
            print(awards_re)
            # return render_template("create_act.html",  act_re=template_type_fe, awards_re =awards_re )
             ##关联广告位
            adzone_re = ct.adzone_act()
            return render_template("create_act.html", template_type_re=template_type_fe, temlate_name_re=temlate_name_fe , act_re=act_fe, awards_re =awards_re ,adzone_re=adzone_re)
        except Exception as e:
            traceback.print_exc()
            return render_template("create_act.html", f_re = e.message)

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

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = ft.MyForm()
    if form.validate_on_submit():
        # if form.user.data == 'admin':
        if form.data['user'] == 'admin':
            name='admin'
            return render_template('logintest.html', form=form,name=name)
        else:
            return 'Wrong user!'
    return render_template('logintest.html', form=form)

#新建，修改测试用例
@app.route('/Api_index/TestCase/<sub_system>/<any(new,update):page_name>/', methods=('POST','GET'))
def TestCase(sub_system,page_name):
    form = TestCaseForm()
    at = Api()
    if page_name=='new' and form.is_submitted():
        sql_data = form.data
        sql_data.pop('csrf_token')
        sql_data.pop('submit')
        url_params = at.split_url(sql_data['methodurl'])
        # print url_params[1]
        sql_data['methodurl'] = url_params[0].strip()
        sql_data['param'] = str(url_params[1]).strip()
        sql_data['group'] = sub_system
        print sql_data
        keys = tuple(sql_data.keys())
        values_list = json.dumps(sql_data.values(), encoding='utf-8', ensure_ascii=False)
        re = at.insert_case(values_list, keys)
        if re != 0:
            flash('添加成功')
        else:
            flash('添加失败')
        return render_template('TestCase/testCase.html', form=form, case_detail=None, sub_system=sub_system)
    elif page_name=='update':
        if len(request.args) > 0:
            cid = request.args['id']
            case_detail = at.query_case_detail(cid)[0]
            methodurl = at.merge_url_param(str(case_detail['methodurl']), str(case_detail['param']))
            if form.is_submitted():
                sql_data = form.data
                sql_data.pop('csrf_token')
                sql_data.pop('submit')
                url_params = at.split_url(sql_data['methodurl'])
                sql_data['methodurl'] = url_params[0].strip()
                sql_data['param'] = url_params[1]
                sql_data['group'] = sub_system.strip()
                set_value='''apiState= "{}",apiName= "{}",testCaseName= "{}",`status`= "{}",`level` = "{}",param_type = "{}",
                             methodurl = "{}",param="{}", actresult = "{}", expect_value = "{}", remarks = "{}"
                             '''.format(sql_data['apiState'],sql_data['apiName'],sql_data['testCaseName'],sql_data['status'],
                                        sql_data['level'],sql_data['param_type'],sql_data['methodurl'],sql_data['param'],
                                        sql_data['actresult'],sql_data['expect_value'],sql_data['remarks'])
                print set_value
                at.update_case(set_value,cid)
                case_detail = at.query_case_detail(cid)[0]
                return render_template('TestCase/testCase.html', form=form, case_detail=case_detail,methodurl=methodurl, sub_system=sub_system)
            else:
                return render_template('TestCase/testCase.html', form=form, case_detail=case_detail, methodurl=methodurl,sub_system=sub_system)
        return render_template('TestCase/testCase.html', form=form, case_detail=None, sub_system=sub_system)
    return render_template('TestCase/testCase.html', form = form,case_detail=None,sub_system=sub_system)

@app.route('/Api_index/<sub_system>/<any(stat,detail):page_name>/', methods=['POST','GET'])
def sub_system(sub_system,page_name): #,id=None):
    title = sub_system
    at = Api()
    if page_name=='stat':
        static_data = at.query_api_stat_detail(sub_system)
        return render_template('TestCase/sub_system_static.html',title = title, static_data = static_data, static_count = len(static_data),sub_system=sub_system )
    elif page_name=='detail':
        search = False
        pagesize=20
        q = request.args.get('q')
        if q:
            search=True
        page = request.args.get(get_page_parameter(),type=int,default=1)
        print request.method
        if request.method=='POST':
            cid = request.form.get('id').strip()
            detail_data = at.query_case_list(sub_system, page, pagesize,id=cid)
            print detail_data
            print cid,'is is is is'
        else:
            detail_data = at.query_case_list(sub_system, page, pagesize)
        if isinstance(detail_data[0],list):
            total =detail_data[1]
            pagination=Pagination(page=page,total=total,per_page=pagesize,search=search,record_name='cases')
            return render_template('TestCase/FinalCaseList.html', title=title, detail_data=detail_data[0],pagesize=pagesize, detail_count=detail_data[1],pagination=pagination,system_name=sub_system)
        elif isinstance(detail_data,str):
            return render_template('TestCase/FinalCaseList.html', title=title, detail_data=detail_data,sub_system=sub_system)

@app.route('/Api_index/')
def Api_index():
    at = Api()
    re = at.query_api_stat_summary()
    return render_template('TestCase/apiStatic.html',re =re, col_len = len(re[0]))



@app.route('/test/')
def test():
    return render_template("test.html")
@app.route('/myiframe/')
def myiframe():
    return render_template("myiframe.html")

@app.route('/version_maintain/<any(new,update):page_name>/',methods=('POST','GET'))
def version_maintain(page_name):
    # mail = Mail(app)
    form = VersionTrackerForm()
    vt = VersionTracker()
    if page_name == 'new':
    # form = VersionTrackerForm()
    # vt = VersionTracker()
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
        # job_name = request.form.get('job_name')
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

@app.route('/ocpa_price',methods=['POST','GET'])
def ocpa_price():
    title=u'广告主OCPA调价趋势图'
    if request.method == 'GET':

        return render_template('adjust_ocpa.html',title=title)

    else:
        env_dict={u'测试环境':True,u'线上环境':False}
        env=request.form.get('env').strip()
        ad_order_id = request.form.get('ad_order_id')
        adzone_id = request.form.get('AdzoneId')

        day=request.form.get('begin_date')
        beign_time_re=day.replace('-','')
        oc=adjust_price(day,ad_order_id,env_dict[env],adzone_id=adzone_id)
        xvalue,dat,dat2,init_price,dat3,dat4=oc.timelist(),oc.adjust_ocpa(),oc.actual_payment(),oc.init_price(),oc.adzone(),oc.shownum()
        print xvalue,dat,init_price
        print adzone_id
        return render_template('adjust_ocpa.html',xvalue=xvalue,title=title,data=dat,data2=dat2,data3=dat3,data4=dat4,init_price=init_price,begintime=day,ad_order_id=ad_order_id,adzone_id=int(adzone_id),env_value='<option selected="selected">'+env+'</option>')


@app.route('/ocpa_order',methods=['POST','GET'])
def ocpa_order():
    title=u'OCPA订单查询'
    if request.method == 'GET':

        return render_template('ocpa_order.html',title=title)
    else:
        begin_time = request.form.get('begin_date')
        beign_time_re=begin_time.replace('-','')
        result_order= Ocpa_order(beign_time_re,env_value=False)
        paras=result_order.show_result()

        return render_template("ocpa_order.html",title=title,paras=paras,begin_time=beign_time_re,begintime=begin_time)


@app.route('/ocpaorder_detail')

def ocpaorder_detail(env=False):
    title=u'OCPA订单调价趋势图'
    ad_order_id=request.args.get('ad_order_id')
    day=request.args.get('date')
    adzone_id=request.args.get('adzone_id')
    oc=adjust_price(day,ad_order_id,env,adzone_id=adzone_id)

    xvalue,dat,dat2,init_price,dat3=oc.timelist(),oc.adjust_ocpa(),oc.actual_payment(),oc.init_price(),oc.adzone()
#    adzone_id=request.form.get('AdzoneId')
    return render_template('adjust_ocpa.html',xvalue=xvalue,title=title,data=dat,data2=dat2,data3=dat3,init_price=init_price,begintime=day,ad_order_id=ad_order_id,adzone_id=int(adzone_id),env_value=False)

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
        print re
        print type(re)
        return render_template('phoneVaildCode.html', re=re,pos='1')
    else:
        env = request.values.getlist('env')
        print env[0]
        pp = phoneVaild(env=env[0])
        re = pp.get_valid_code()
        return  render_template('phoneVaildCode.html',re=re,pos=env[0])

@app.route('/checkRoute/',methods=['get','post'])
def checkRoute():
    form = checkRouteForm()
    re = ''
    if request.method == 'GET':
        return render_template('checkRoute.html',form = form,re=re)
    else:
        datas = form.data
        env = datas['env'].strip()
        adzoneLink = datas['adzoneLink'].strip()
        cr = checkNodeRoute(env,adzoneLink)
        re = cr.join_url()
        if isinstance(re,list) and len(re)>0:
            re_len = len(re)
            return render_template('checkRoute.html', form=form, re=re, re_type=1,re_len=re_len)
        else:
            return render_template('checkRoute.html',form = form,re=re,re_type=0)


@app.route('/punchcard',methods=['POST','GET'])
def punchcard():
    title = u"小程序用户信息"
    if request.method == 'GET':
        return render_template('punchcard.html',title=title)

    else:
        begin_date = request.form.get('begin_date')
        end_date = request.form.get('end_date')
        punchcard_result = Punchcard(begin_date,end_date,env_value=False)
        # paras = punchcard_result.user_info()
        total_amount = punchcard_result.total_amount()
        total_addamount=punchcard_result.today_addamount()
        invite_add=punchcard_result.invite_add()
        non_inviteadd=punchcard_result.non_inviteadd()
        today_sign=punchcard_result.today_sign()
        xvalue=punchcard_result.dateRange(begin_date,end_date)
        data=punchcard_result.add_user(begin_date,end_date)
        return render_template('punchcard.html',total_amount=total_amount,today_addamount=total_addamount,today_sign=today_sign,begin_date=begin_date,end_date=end_date,xvalue=xvalue,data=data,invite_add=invite_add,non_inviteadd=non_inviteadd)


@app.route('/templateToAct/<any(query,position):page_name>/',methods=['get','post'])
def templateToAct(page_name):
    form=templateActForm()
    if request.method=='GET' and page_name=='query':
        return render_template('template/templateToAct.html', ts='false', form=form)
    elif request.method == 'POST' and page_name == 'query':
        act_ids = request.form.get('ad_ids')
        env = request.form.get('env')
        template_kws = request.form.get('template_kws')
        tta = templateAct(env)
        # if page_name == 'query':
        #     if request.method == 'POST':
        if template_kws:
            template_kws = template_kws.encode('utf-8')
        re = tta.get_infos(template_kws, act_ids)
        if isinstance(re,list) and len(re)>0:
            tta.exportTemplateXls(re)
            return render_template('template/templateToAct.html', ts='true', form=form,re=re,env=env, flag='true')
        else:
            return render_template('template/templateToAct.html', ts='true', form=form,re=re,env=env, flag='flase')
    elif page_name == 'position' and request.method == 'GET':
        position_id = request.args.get('id')
        env_tmp = request.args.get('env')
        tta2 = templateAct(env_tmp)
        position_re = tta2.get_position(position_id)
        return render_template('template/position.html', re=position_re)
        # else:
        #     return render_template('template/templateToAct.html', ts='false', form=form)

@app.route('/mini_mediainfo',methods=['POST','GET'])
def mini_mediainfo():

    title=u'小程序推广渠道数据统计'
    if request.method=='GET':
        return render_template('mini_mediainfo.html',title=title)

    else:
        begin_time=request.form.get('begin_time')
        media_dict={u"有练换换":"wx0a051787252f83fa",u"步数大联盟":"wxe65c34b4ec242be",u"优质福利所":"wx3c48ef7a45e89118"}
        media_info=request.form.get('media_name').strip()
        mediainfo=Mini_mediainfo(media_dict[media_info],begin_time,env_value=False)
        authorize_user=mediainfo.authorize_user()
        wxstep_user=mediainfo.wxstep_user()
        invite_user=mediainfo.invite_user()
        invited_user=mediainfo.invited_user()
        task_user=mediainfo.task_user()
        return render_template('mini_mediainfo.html',begin_time=begin_time,media_name='<option selected="selected">'+media_info+'</option>',authorize_user=authorize_user,wxstep_user=wxstep_user,invite_user=invite_user,invited_user=invited_user,task_user=task_user)



if __name__ == '__main__':
    app.run( host="0.0.0.0",port=21312,debug=True)
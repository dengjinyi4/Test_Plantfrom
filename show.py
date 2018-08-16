#!/usr/bin/env python
#encoding: utf-8
#version:2018/07/10,增加接口统计视图函数
import os
import traceback

from flask import jsonify
from flask import Flask,request,render_template,flash

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
from utils.Emar_SendMail_Attachments import *
from config import mail_template,sqls

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
        if jobid1=='120':
            data='<option selected="selected">缓存中的订单预算：生产</option>'
            redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
            # mybudget,allcount,negativecount=mr.mygetredis(redis_nodes)
            # return render_template('myredis.html',mybudget=mybudget,allcount=allcount,negativecount=negativecount)
        elif jobid1=='110':
            data='<option selected="selected">缓存中的订单预算：测试</option>'
            redis_nodes=[{"host":'101.254.242.11',"port":'17001'},{"host":'101.254.242.12',"port":'17001'},{"host":'101.254.242.17',"port":'17001'}]
        mybudget,allcount,negativecount=mr.mygetredis(redis_nodes)
        return render_template('myredis.html',mybudget=mybudget,allcount=allcount,negativecount=negativecount,data=data)


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
        kss = form.data['adzoneClickid']
        tmpdit=ba.orderbylognew(zclk)
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
        print month,year
        reslut=lc.getlanuchlist(int(year),int(month))
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
    reslut=lc.getlanuch(id)
    return render_template('launchdetial.html',result=reslut)

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

# @app.route('/baselogin',methods=('POST','GET'))
# def baselogin():
#     form=BaseLogin()
#     #判断是否是验证提交
#     if form.validate_on_submit():
#         #跳转
#         # flash(form.name.data+'|'+form.password.data+'|'+form.begintime.data)
#         flash(form.name.data+'|'+form.password.data)
#         # print form.name.data
#         # print form.password.data
#         return redirect(url_for('hdtapi'))
#     else:
#         #渲染
#         return render_template('baselogin.html',form=form)

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

@app.route('/Api_index/testCase/', methods=('POST','GET'))
def TestCase():
    form = TestCaseForm()
    at = Api()
    if form.is_submitted():
        sql_data = form.data
        sql_data.pop('csrf_token')
        sql_data.pop('submit')
        keys = tuple(sql_data.keys())
        values_list = json.dumps(sql_data.values(), encoding='utf-8', ensure_ascii=False)
        re=at.insert_case(values_list,keys)
        # sql = r"INSERT INTO test.testcase_adv {} VALUES ".format(keys).replace("'","`")
        # sql = sql + "("  + values_list[1:-1] +")"
        # print sql
        # db.execute_sql(sql)
        # db.mycommit()
        if re != 0:
            print 'sussssssss'
            msg = '添加成功'
        else:
            print 'failllllllllll'
            msg = '添加失败'
        return render_template('testCase.html',  form = form, msg=msg)
    return render_template('testCase.html', form = form)


@app.route('/Api_index/')
def Api_index():
    at = Api()
    re = at.query_api_stat_summary()
    return render_template('apiStatic.html',re =re, col_len = len(re[0]))

@app.route('/Api_index/<sub_system>/')
def sub_system(sub_system):
    print sub_system
    title = sub_system
    at = Api()
    static_data = at.query_api_stat_detail(sub_system)
    return render_template('sub_system_static.html',title = title, static_data = static_data, static_count = len(static_data) )

@app.route('/test/')
def test():
    return render_template("test.html")
@app.route('/myiframe/')
def myiframe():
    return render_template("myiframe.html")

@app.route('/version_maintain/',methods=('POST','GET'))
def version_maintain():
    # mail = Mail(app)
    form = VersionTrackerForm()
    vt = VersionTracker()
    if form.is_submitted():
        sql_data = form.data
        print sql_data
        sql_data.pop('csrf_token')
        sql_data.pop('submit')
        #处理多个tester_id的情况,将ids处理为1,2,3的形式
        tester = json.dumps(sql_data['tester'], encoding='utf-8', ensure_ascii=False)[1:-1].replace("\"", "")
        #使用update将字典tester的值更新
        sql_data.update(tester=tester)
        keys = tuple(sql_data.keys())
        values_list = json.dumps(sql_data.values(), encoding='utf-8', ensure_ascii=False)
        re = vt.insert_version(values_list, keys)
        if re != 0:
            msg = '添加成功'
            if int(form.data['send_email']) != 0:
                #拼装邮件内容申请者姓名、审批者姓名和邮件发送者的拼音、jobname信息
                applicant = vt.get_user_ch_name(sqls['ch_name'].format(form.data['applicant_id']))[0]
                approver = vt.get_user_ch_name(sqls['ch_name'].format(form.data['approver']))[0]
                sender = vt.get_user_ch_name(sqls['ch_name'].format(tester))[1]
                job_name = vt.get_jenkins_job(sqls['jenkins_name'].format(form.data['job_id']))[0][0]
                print job_name
                send_email(mail_template['normal'], form.data, applicant, approver,sender,job_name)
                flash("send mail Success")
            else:
                flash("send mail Success")
        else:
            msg = '添加失败'
            flash("send mail Fali")
        return render_template('VersionTracker/version_maintain.html', form=form, msg=msg)
    return render_template('VersionTracker/version_maintain.html',form = form)


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





if __name__ == '__main__':
    app.run( host="0.0.0.0",port=21312,debug=True)
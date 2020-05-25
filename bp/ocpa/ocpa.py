# encoding=utf-8
__author__ = 'aidinghua'

from flask import Blueprint ,render_template,request

from business_modle.querytool.ocpa_order import  *
from business_modle.querytool.adjust_ocpa import *
from business_modle.querytool.ocpa_try import  *
from business_modle.querytool.ocpa_data import *
from business_modle.querytool.ocpa_report import *
from business_modle.querytool import myredis as mr

ocpa = Blueprint('ocpa',__name__)

@ocpa.route('/ocpa_price',methods=['POST','GET'])
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



@ocpa.route('/ocpa_order',methods=['POST','GET'])
def ocpa_order():
    title=u'OCPA订单查询'
    if request.method == 'GET':

        return render_template('ocpa_order.html',title=title)
    else:
        begin_time = request.form.get('begin_date')
        beign_time_re=begin_time.replace('-','')
        result_order= Ocpa_order(beign_time_re,env_value=False)
        paras=result_order.show_result()
        ocpa_consume=result_order.ocpa_consumer()
        ocpa_percent=result_order.ocpa_percent()
        ocpa_alltry=result_order.ocpa_alltry()


    return render_template("ocpa_order.html",title=title,paras=paras,ocpa_consume=ocpa_consume,ocpa_alltry=ocpa_alltry,ocpa_percent=ocpa_percent,begin_time=beign_time_re,begintime=begin_time)

@ocpa.route('/ocpa_orderadzone',methods=('POST','GET'))
def ocpa_orderadzone():
    if request.method=='GET':
        # 生产环境
        tmpordeadzon=mr.mygetredis('1','voyager:ocpa_adzones')
        return render_template('ocpaorderadzone.html',tmpordeadzon=tmpordeadzon)

@ocpa.route('/ocpa_orderadzonedetail',methods=('POST','GET'))
def ocpa_orderadzonedetail():
    if request.method=='GET':
        # 生产环境
        tmpordeadzonedetail=mr.mygetredis('1','voyager:ocpa_adzones_detail')
        return render_template('ocpaorderadzonedetail.html',tmpordeadzonedetail=tmpordeadzonedetail)



@ocpa.route('/ocpa_ordercost',methods=('POST','GET'))
def ocpa_ordercost():
    if request.method=='GET':
        tmpordercost=mr.mygetredis('1','voyager:ocpa_actual_cost')
        return render_template('ocpaordercost.html',tmpordercost=tmpordercost)


@ocpa.route('/ocpaorder_detail')

def ocpaorder_detail(env=False):
    title=u'OCPA订单调价趋势图'
    ad_order_id=request.args.get('ad_order_id')
    day=request.args.get('date')
    adzone_id=request.args.get('adzone_id')
    oc=adjust_price(day,ad_order_id,env,adzone_id=adzone_id)

    xvalue,dat,dat2,init_price,dat3,dat4=oc.timelist(),oc.adjust_ocpa(),oc.actual_payment(),oc.init_price(),oc.adzone(),oc.shownum()
    #    adzone_id=request.form.get('AdzoneId')
    return render_template('adjust_ocpa.html',xvalue=xvalue,title=title,data=dat,data2=dat2,data3=dat3,data4=dat4,init_price=init_price,begintime=day,ad_order_id=ad_order_id,adzone_id=int(adzone_id),env_value=False)

@ocpa.route('/ocpatry_detail')

def ocpatry_detail(env=False):
    title=u'OCPA订单试投明细'
    ad_order_id=request.args.get('ad_order_id')
    day = request.args.get('date')

    ocpa=Ocpa_try(day,ad_order_id,env_value=False)
    ocpatry=ocpa.ocpa_try()
    try_consum=ocpa.try_consum()

    return render_template('ocpa_try.html',ocpatry=ocpatry,try_consum=try_consum)


@ocpa.route('/ocpa_data',methods=('POST','GET'))

def ocpa_data(env=True):
    title=u"OCPA数据准备"
    if request.method == 'GET':

        return render_template('ocpa_data.html',title=title)

    else:
        begin_time=request.form.get('beigin_date')
        url='https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171'
        url2='adz102_https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171_6_2'

        ocpadata=Ocpa_data(begin_time,url,url2,env_value=True)

        ocpadata.show_stat1()

        ocpadata.show_stat2()

        ocpadata.show_stat3()
        ocpadata.before_effect()
        ocpadata.cvr_data()
        ocpadata.cvr_data2()

        ocpadata.del_error()
        ocpadata.adzonedo()
        ocpadata.creative_active()



        return render_template('ocpa_data.html',show1=ocpadata.show_stat1(),show2=ocpadata.show_stat2(),show3=ocpadata.show_stat3(),cvr=ocpadata.cvr_data(),clear=ocpadata.del_error(),adzonedo=ocpadata.adzonedo(),begin_time=begin_time)


@ocpa.route('/ocpa_report',methods=['POST','GET'])

def ocpa_report():

    title='OCPA_Report'

    if request.method=='GET':

        return render_template('ocpa_report.html',title=title)

    else:
        begin_date = request.form.get('begin_date')
        end_date = request.form.get('end_date')
        result= Ocpa_report(begin_date,end_date,env_value=False)
        paras=result.show_result()

    return render_template("ocpa_report.html",title=title,paras=paras,begin_date=begin_date,end_date=end_date)





if __name__=='__main__':

    # print ocpa_price()
    # print ocpa_order()
    # print ocpa_orderadzone()
    print ocpa_data()
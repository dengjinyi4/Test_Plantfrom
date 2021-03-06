# encoding=utf-8
__author__ = 'aidinghua'

from flask import  Blueprint,render_template,request
from business_modle.querytool.ttpt_errorlog import *

ttpt=Blueprint('ttpt',__name__)

@ttpt.route('ttpt_errorlog',methods=['POST','GET'])

def ttpt_errorlog():

    title=u'竞价平台数据抓取错误日志'
    if request.method == 'GET':

        return render_template('ttpt_errorlog.html',title=title)

    else:

        env_dict= {u'测试环境':True,u'生产环境':False}
        platform_dict={u'竞价平台':1,u'自建站':2}
        env=request.form.get('env').strip()
        platform=request.form.get('platform').strip()
        day = request.form.get('begin_date')
        begin_time_re=day.replace('-','')
        te=Ttpt_errorlog(day,env_dict[env])

        if platform=='竞价平台':
            paras=te.show_result()

        else:
            paras=te.show2_result()


        return render_template('ttpt_errorlog.html',paras=paras,begin_time=begin_time_re,begintime=day,env_value='<option selected="selected">'+env+'</option>',platform='<option selected="selected">'+platform+'</option>')

if __name__=='__main__':

    # print ocpa_price()
    # print ocpa_order()
    # print ocpa_orderadzone()
    print ttpt_errorlog()
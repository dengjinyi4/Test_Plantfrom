# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 15:13
# @Author  : wanglanqing


from flask import Blueprint,flash,request,render_template
from .jobAdReason.jobAdReasonForm import JobAdReasonForm
from .jobAdReason.jobAdReason import JobAdReason
from business_modle.querytool.bidding_job_reason import Job_updateAdzoneclickids,jobreason,Jobresult


#创建蓝图
tools = Blueprint('tools',
                  __name__,
                  template_folder='template'
                  )

@tools.route('/JobAdReason/<any(new,query_click_id,query_es,query_chart,query_multi_chart):page_name>',methods=['POST','GET'])
def jobReason(page_name):
    form = JobAdReasonForm()
    jar = JobAdReason()
    if request.method == 'POST' and page_name == 'new':
        form_datas = form.data
        form_datas.pop('csrf_token')
        jar.add_job_ad_reason(form_datas)
        re = jar.get_job_ad_reason_list()
        return render_template('JobReason/jobAdReason.html', form=form, re=re, re_len=range(len(re)))
    elif request.method == 'POST' and page_name == 'query_click_id':
        id = request.args.get('id')
        j = Job_updateAdzoneclickids(id)
        j.start()
        re = jar.get_job_ad_reason_list()
        return render_template('JobReason/jobAdReason.html', form=form, re=re, re_len=range(len(re)))
    elif request.method == 'POST' and page_name == 'query_es':
        id = request.args.get('id')
        job = Jobresult(id)
        x = job.start()
        re = jar.get_job_ad_reason_list()
        return render_template('JobReason/jobAdReason.html', form=form, re=re, re_len=range(len(re)))
    elif request.method == 'GET' and page_name == 'query_chart':
        id = request.args.get('id')
        re = jar.query_chart(id)
        aa = re[0].split(',')
        #把中文字符串，转换为数组
        case_list_righ = str(aa).replace('u\'', '\'')
        dd = case_list_righ.decode("unicode-escape")
        return render_template('JobReason/JobReasonChart.html', rex=dd,rey=re[1])
    elif request.method == 'GET' and page_name == 'query_multi_chart':
        ids = request.args.get('ids')
        if ids:
            re = jar.query_multi_chart(ids)
            aa = re[0]
            # 把中文字符串，转换为数组
            case_list_righ = str(aa).replace('u\'', '\'')
            dd = case_list_righ.decode("unicode-escape")
            return render_template('JobReason/JobReasonChart.html', rex=dd,rey=re[1])
        else:
            return '<p>ids参数，传点值吧，比如1,2,3</p>'
    else:
        re = jar.get_job_ad_reason_list()
        return render_template('JobReason/jobAdReason.html', form=form,re=re, re_len=range(len(re)))
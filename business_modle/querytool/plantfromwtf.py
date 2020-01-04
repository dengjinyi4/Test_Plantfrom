#!flask/bin/env python
#coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField,BooleanField,RadioField,SelectMultipleField,DateTimeField,PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange,Regexp
from config import sub_systems
from config import sub_systems,sqls
from business_modle.VersionTracker.VersionTracker import VersionTracker
import datetime,time
class phoneVaildCode(Form):
    myenv=RadioField('myenv',choices=[('dev',u'生产环境'),('test',u'测试环境')],default='dev')
    mydb=RadioField('mydb',choices=[('normandy',u'易购宝贝'),('voyager',u'互动推')],default='voyager')
    submit=SubmitField(u'查询')
class MyForm(Form):
    adzoneClickid = StringField('adzoneClickid', validators=[Length(min=4, max=25)])
    myenv=RadioField('myenv',choices=[('dev',u'生产环境'),('test',u'测试环境')],default='dev')
    # submit=SubmitField(u'提交')
class Mylogin(Form):
    username = StringField('用户名', validators=[Length(min=1, max=25)])
    password = PasswordField('密   码', validators=[Length(min=1, max=25)])
    submit=SubmitField(u'登录')
class egoubaobei_orderpay(Form):
    order_status=RadioField(u'订单支付状态',choices=[('True',u'支付成功'),('False',u'支付失败'),('ing',u'待支付')],default='True')
    orderid = StringField(u'订单id', validators=[DataRequired(),Length(min=5, max=20,message=u'订单id长度5-20')],render_kw={'placeholder':u'订单id'})
    submit=SubmitField(u'更新')
class egoubaobei_product(Form):
    skuid = StringField(u'skuid', validators=[DataRequired(),Length(min=5, max=20,message=u'订单id长度5-20')],render_kw={'placeholder':u'订单id'})
    submit=SubmitField(u'查找')
class myredis(Form):
    myenv=RadioField('orderstatus',choices=[('dev',u'生产环境'),('test',u'测试环境')],default='dev')
    submit=SubmitField(u'提交')
class orderresion1(Form):
    begindate=StringField(u'开始时间',validators=[DataRequired(),Regexp("^(((20[0-3][0-9]-(0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|(20[0-3][0-9]-(0[2469]|11)-(0[1-9]|[12][0-9]|30))) (20|21|22|23|[0-1][0-9]):[0-5][0-9]:[0-5][0-9])$",0, message="开始时间请输入正确的日期: 2019-03-20 11:27:00")],default= str(datetime.datetime.now())[0:19])
    enddate=StringField(u'结束时间',validators=[DataRequired(),Regexp("^(((20[0-3][0-9]-(0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|(20[0-3][0-9]-(0[2469]|11)-(0[1-9]|[12][0-9]|30))) (20|21|22|23|[0-1][0-9]):[0-5][0-9]:[0-5][0-9])$",0, message="结束时间请输入正确的日期: 2019-03-20 11:27:00")],default= str(datetime.datetime.now())[0:19])
    # enddate=DateTimeField('enddate',validators=[DataRequired()],default=datetime.datetime.now())
    myenv=RadioField('myenv',choices=[('dev',u'生产环境'),('test',u'测试环境')],default='dev')
    adzone_id = StringField(u'广告位id', validators=[DataRequired(),Length(min=1, max=20,message=u'广告位长度1-20')])
    ad_order_id = StringField(u'订单id', validators=[DataRequired(),Length(min=1, max=20,message=u'订单长度1-20')])
    # adzoneClickid = StringField(u'广告位点击id字符串中间逗号分隔',validators=[DataRequired(),Length(min=19, max=2000,message=u'广告位点击id最少两个逗号分隔',default='1')])
    adzoneClickid = StringField(u'广告位点击id字符串中间逗号分隔',validators=[DataRequired()], render_kw={'placeholder': u'广告位点击id;逗号分隔;最少两个','style':'width350'},default='test')
    submit=SubmitField(u'提交')
class orderr(Form):
    begindate=StringField(u'开始时间',validators=[DataRequired(),Regexp("^(((20[0-3][0-9]-(0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|(20[0-3][0-9]-(0[2469]|11)-(0[1-9]|[12][0-9]|30))) (20|21|22|23|[0-1][0-9]):[0-5][0-9]:[0-5][0-9])$",0, message="开始时间请输入正确的日期: 2019-03-20 11:27:00")],default= str(datetime.datetime.now())[0:19])
    enddate=StringField(u'结束时间',validators=[DataRequired(),Regexp("^(((20[0-3][0-9]-(0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|(20[0-3][0-9]-(0[2469]|11)-(0[1-9]|[12][0-9]|30))) (20|21|22|23|[0-1][0-9]):[0-5][0-9]:[0-5][0-9])$",0, message="结束时间请输入正确的日期: 2019-03-20 11:27:00")],default= str(datetime.datetime.now())[0:19])
    # enddate=DateTimeField('enddate',validators=[DataRequired()],default=datetime.datetime.now())
    myenv=RadioField('myenv',choices=[('dev',u'生产环境'),('test',u'测试环境')],default='dev')
    adzone_id = StringField(u'广告位id', validators=[DataRequired(),Length(min=1, max=20,message=u'广告位长度1-20')])
    ad_order_id = StringField(u'订单id', validators=[DataRequired(),Length(min=1, max=20,message=u'订单长度1-20')])
    # adzoneClickid = StringField(u'广告位点击id字符串中间逗号分隔',validators=[DataRequired(),Length(min=19, max=2000,message=u'广告位点击id最少两个逗号分隔',default='1')])
    # adzoneClickid = StringField(u'广告位点击id字符串中间逗号分隔',validators=[DataRequired()], render_kw={'placeholder': u'广告位点击id;逗号分隔;最少两个'},default='test')
    submit=SubmitField(u'提交')

class mypop(Form):
    adzoneClickid = StringField('adzoneClickid',validators=[DataRequired(),Length(min=4, max=25)])
    submit=SubmitField(u'提交',render_kw={'class':'btn btn-primary'})

# class Mylaunchlist(Form):
#     def mymonth(self):
#         return int(datetime.datetime.now().month)
#     def defaultyear(self):
#         return int(datetime.datetime.now().year)
#     myyear =SelectField(u'年', validators=[DataRequired()], choices=[(2018,2018),(2019,2019),(2010,2010),], default=defaultyear)
#     mymonth = SelectField(u'月', validators=[DataRequired()], choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)], default=mymonth)
#     submit = SubmitField(u'查  找')

class TestCaseForm(Form):
    #从config配置文件里，读取子系统，构建页面上的group信息
    sss = sub_systems.values()
    ssl =[]
    for sub_system in sss:
        ssl.append((sub_system,sub_system))

    #定义表单元素
    apiName = StringField(u'apiName', validators=[DataRequired()],render_kw={'placeholder':u'广告计划-列表'})
    apiState = RadioField(u'apiState',validators=[DataRequired()],choices=[('1', u'已编写'), ('0', u'未编写')], default = '1')
    testCaseName = StringField(u'testCaseName',validators=[DataRequired()],render_kw={'placholder':'order/list'})
    # status = SelectField(u'status',choices=[('有效','1'),('无效','0')])
    # group=RadioField('group',validators=[],choices=[('yiiqfa','yiiqfa'),('egou','egou'),('hudongtui','hudongtui')])
    # group=RadioField('group',validators=[DataRequired()],choices=ssl)
    status = RadioField(label=u'status',validators=[DataRequired()],choices=[('1', u'启用'),('0', u'停用')],default='1')
    level = IntegerField(u'level',validators=[],render_kw={'placeholder':u'等级1 2 3'})
    param_type = SelectField(u'param_type', choices=[('A',u'错误信息'), ('B', u'数据结构'), ('C', u'状态码')])
    # methodurl = TextAreaField(u'methodurl', validators=[DataRequired()],render_kw={'placeholder':'http://api.demand.adhudong.com/api/voyager/order/list.htm','style':'height:50px','style':'weight:200px'})
    methodurl = TextAreaField(u'methodurl', validators=[DataRequired()],render_kw={'style': 'height:50px', 'style': 'weight:200px'})
    # param = TextAreaField(u'param',render_kw={'placeholder':"{'aid':'0'}",'style':'height:100px；weight:50px'})
    actresult = IntegerField(u'actresult',render_kw={'placeholder':u'http状态码 e.g 200 302'})
    expect_value=TextAreaField('expect_value')
    remarks=StringField('remarks')
    submit = SubmitField(u'提交保存')


class VersionTrackerForm(Form):
    # 从config配置文件里，读取group，和对应的jobs
    vt = VersionTracker()
    group_choices = list(vt.get_group_info(sqls['group']))
    job_name_choices = list(vt.get_jenkins_job(sqls['jenkins_job']))
    required_name_choices = list(vt.get_jenkins_job(sqls['required']))
    applicant_choices = list(vt.get_user_info(sqls['applicant']))
    tester_choices = list(vt.get_user_info(sqls['tester']))
    approver_choices = list(vt.get_user_info(sqls['approver']))

    group_id = SelectField(u'group', validators=[DataRequired()], choices=group_choices, default=1)
    job_id = SelectField(u'job', choices=job_name_choices) #通过group级联选择？
    required_id = SelectField(u'需求', validators=[DataRequired()], render_kw={'placeholder': u'需求者姓名'}, choices=required_name_choices)  # 是否需要配置
    applicant_id = SelectField(u'开发', validators=[DataRequired()], render_kw={'placeholder': u'开发者姓名'}, choices=applicant_choices)  # 是否需要配置
    approver = SelectField(u'审批人', render_kw={'placeholder': u'审批人姓名'}, choices=approver_choices)  # 是否需要配置
    # ol_type = StringField(u'ol_type', render_kw={'placeholder': u'上线类型'})  #默认为当天时间
    ol_type = SelectField(u'上线类型', validators=[DataRequired()], choices=[(1,'正常上线')], default=1)
    apply_date = StringField(u'apply_date',validators=[DataRequired()], default=vt.get_date()) #默认为当天时间
    ol_date = StringField(u'ol_date',validators=[DataRequired()], default=vt.get_date()) #, validators=[DataRequired()]
    version = StringField(u'version', validators=[DataRequired(message=u'请输入版本号')], render_kw={'placeholder': u'项目版本号信息','pattern':'[0-9A-Za-z.]*'})  # 是否需要配置,Regexp()
    v_tag = StringField(u'tag', render_kw={'placeholder': u'项目版本tag信息'})  # 是否需要配置
    v_desc = TextAreaField(u'v_desc',render_kw={'placeholder':u'上线内容描述'})
    # v_reason = SelectField(u'上线分类')
    tester = SelectMultipleField(u'tester', render_kw={'placeholder': u'测试人姓名', 'style': "height:145px"},choices=tester_choices)
    remark = TextAreaField(u'remark', render_kw={'placeholder': u'备注信息'})
    send_email = RadioField(u'是否发送邮件', choices=[('1', u'是'), ('0', u'否')],default=0)
    submit = SubmitField(u'提交保存')

class Mylaunchlist(Form):
    group_choices=VersionTrackerForm.group_choices
    #copy tester_choices
    tester_list = VersionTrackerForm.tester_choices[:]
    tester_list.insert(0, ('ALL', 'all'))
    def current_month(self):
        return int(datetime.datetime.now().month)

    def defaultyear(self):
        return int(datetime.datetime.now().year)
    #增加获取当前年和月
    current_year= int(datetime.datetime.now().year)
    current_month=int(datetime.datetime.now().month)
    myyear = SelectField(u'年', validators=[DataRequired()], choices=[(2018, 2018), (2019, 2019), (2020, 2020),(2021, 2021), ],
                         default=current_year)
    mymonth = SelectField(u'月', validators=[DataRequired()],
                          choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
                                   (11, 11), (12, 12)], default=current_month)
    #增加两个查询条件
    groups = SelectField(u'业务组', validators=[DataRequired()], choices=group_choices, default=1)
    testers = SelectField(u'tester', choices=tester_list,default=0)
    submit = SubmitField(u'查  找')

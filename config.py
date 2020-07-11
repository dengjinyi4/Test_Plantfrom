#!/usr/bin/env python
#coding=utf-8
CSRF_ENABLED = True
# CSRF_ENABLED = False
SECRET_KEY = 'fdasfdasfds&YUJFGGHNMJKLOL:'

#定义数据库信息
# 'voyager_test': ("221.122.127.183", 5701, "voyager", "voyager", "voyager", "utf8"),
db_config = {
    'voyager_test': ("172.16.105.12",5701,"voyager","voyager","voyager","utf8"),
    'voyager_online': ("221.122.127.168",3306,"voyager","dengjinyi","dengjinyi123456",'utf8'),
    'doc_online': ("123.59.17.245",3306,"doc","doc_reader","fedh0gkM0Wx9",'utf8'),
}

# ['hdt_demand','hdt_admin','hdt_displaynode','egou','yiqigou']
#定义doc子系统id和子系统名称
sub_systems ={
    314: 'hdt_demand',
    313: 'hdt_admin',
    318: 'hdt_displaynode',
    321: 'egou_admin',
    322: 'egou_front',
    317: 'yiqigou',
    323: 'hdt_ypg'
}


#version_tracker的sql
#2019/09/25 增加获取需求提出者的sql
sqls = {
    'group' : "select id, name from test.group where status=1;",
    'applicant' : "select id, ch_name from test.user where status=1 and role in (1,3) ",#and group_id=",
    'required' : "select id, ch_name from test.user where status=1 and role in (4,5) ",#and group_id=",
    'approver' : "select id, ch_name from test.user where status=1 and role=3 ",
    'tester': "select ch_name, ch_name from test.user where status=1 and role=2 ",
    'jenkins_job' : "select id, name from test.jenkins_job where group_id=1 and status=1 ",
    'ch_name': "select ch_name,name from test.user where status=1 and ch_name like '%{}%'",
    'applicant_ch_name' : "select ch_name,name from test.user where status=1 and id in ({})",
    'jenkins_name':"select  name from test.jenkins_job where status=1 and id in ({})",
    'tester_email': "select `name`  from test.user where status=1 and role=2; ",
}

#version_tracker的邮件模板
mail_template = {
    'normal' : """<p>sys：</p><p>&emsp;&emsp;&emsp;请帮忙上线已经灰度%s</p><br>
    <table border=1 cellspacing=0>
    <tr><td>上线业务名称</td><td> %s </td></tr>
        <tr><td>申请人</td><td> %s </td></tr>
        <tr><td>审批人</td><td> %s </td></tr>
        <tr><td>申请时间</td><td> %s </td></tr>
        <tr><td>上线时间</td><td> %s </td></tr>
        <tr><td>版本号</td><td> %s </td></tr>
        <tr><td>tag信息</td><td> %s </td></tr>
        <tr><td>上线内容描述</td><td> %s </td></tr>
    </table>""",
    'check_in': """<p>hi：</p><p>&emsp;&emsp;&emsp;已下功能已提测%s</p><br>
        <table border=1 cellspacing=0>
        <tr><td colspan="2" bgcolor="#32CD32">提测内容</td></tr>
            <tr><td>产品线/模块</td><td> %s </td></tr>
            <tr><td>需求者</td><td> %s </td></tr>
            <tr><td>提测人</td><td> %s </td></tr>
            <tr><td>代码审核人</td><td> %s </td></tr>
            <tr><td>测试接收人</td><td> %s </td></tr>
            <tr><td>修改代码涉及分支</td><td> %s </td></tr>
            <tr><td>提测时间</td><td> %s </td></tr>
            <tr><td>提测内容（修改内容）</td><td> %s </td></tr>
            <tr><td>提测版本号</td><td> %s </td></tr>
            <tr><td>影响功能点</td><td> %s </td></tr>
            <tr><td>测试关注点	</td><td> %s </td></tr>
            <tr><td>风险描述</td><td> %s </td></tr>
        </table>"""
}

mail_suffix = '@emar.com'

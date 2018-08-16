# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 21:33
# @Author  : wanglanqing

import smtplib
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import email.MIMEImage


def send_email(template_type, data, applicant, approver, sender,  job_name, recipients=['dengjinyi','aidinghua','wanglanqing','zhaoyu1','mahui','wangyouju']):

    suffix = '@emar.com'
    sender = sender + suffix
    recipients = [recipient + suffix for recipient in recipients]
    # job_name = '-'.join(data['v_tag'].split('-')[0:2])
    mailSubject = job_name + '--' + data['apply_date'] + '--申请上线'
    mailText = template_type % (job_name, job_name, applicant, approver, data['apply_date'], data['ol_date'], data['version'], data['v_tag'],data['v_desc'])
    try:
        server = smtplib.SMTP("mail.emar.com")
    except Exception as e:
        print e.message
    #构造MIMEMultipart对象做为根容器
    main_msg = email.MIMEMultipart.MIMEMultipart()
    text_msg = email.MIMEText.MIMEText(mailText, 'html', 'utf-8')
    main_msg.attach(text_msg)
    #设置根容器属性
    main_msg['From'] = sender
    main_msg['To'] = ";".join(recipients)
    # print main_msg['To']
    main_msg['Subject'] = mailSubject
    main_msg['Date'] = email.Utils.formatdate()
    # 得到格式化后的完整文本
    fullText = main_msg.as_string()
    main_msg['msg'] = fullText
    # 用smtp发送邮件
    try:
        send_re = server.sendmail(sender, recipients, fullText)
        # send_re = server.sendmail()
        print send_re
    finally:
        server.quit()
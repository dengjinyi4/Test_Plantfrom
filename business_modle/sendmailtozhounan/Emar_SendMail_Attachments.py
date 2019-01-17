# -*- coding: utf-8 -*-  
import smtplib  
import email.MIMEMultipart# import MIMEMultipart  
import email.MIMEText# import MIMEText  
import email.MIMEBase# import MIMEBase  
import os.path  
  
import mimetypes  
import email.MIMEImage# import MIMEImage  
  
def sendTestreport(mailto,mailSubject,mailText):

	From = "dengjinyi@emar.com"

	server = smtplib.SMTP("mail.emar.com")
	# server.login("1","111111") #仅smtp服务器需要验证时  

	# 构造MIMEMultipart对象做为根容器  
	main_msg = email.MIMEMultipart.MIMEMultipart()  

	# 获取html内容
	# f = open(file_name, 'r')#filename，文件路径、名称，如果有\，注意转义或者开头加r，mode读取的模式，r读取，w写入，，
	# read = f.read()#获取内容并储存在变量里
	# f.close()#关闭文件，节省内存

	# 构造MIMEText对象做为邮件HTML样式显示内容并附加到根容器  
	text_msg = email.MIMEText.MIMEText(mailText,'html','utf-8')
	main_msg.attach(text_msg)  
	  
	# 构造MIMEBase对象做为文件附件内容并附加到根容器  
	# ctype,encoding = mimetypes.guess_type(file_name)
	# if ctype is None or encoding is not None:
	#     ctype='application/octet-stream'
	# maintype,subtype = ctype.split('/',1)
	# file_msg=email.MIMEImage.MIMEImage(open(file_name,'rb').read(),subtype)
	# print ctype,encoding
	  
	## 设置附件头  
	# basename = os.path.basename(file_name)
	# file_msg.add_header('Content-Disposition','attachment', filename = basename)#修改邮件头
	# main_msg.attach(file_msg)
	  
	# 设置根容器属性  
	main_msg['From'] = From  
	main_msg['To'] = ",". join(mailto)
	main_msg['Subject'] = mailSubject  
	main_msg['Date'] = email.Utils.formatdate( )  
	  
	# 得到格式化后的完整文本  
	fullText = main_msg.as_string( )  
	  
	# 用smtp发送邮件  
	try:  
	    server.sendmail(From, mailto, fullText)  
	finally:  
	    server.quit()  
def mailtext():
    tmp='''

    '''
if __name__ == '__main__':
	to_list=['dengjinyi@emar.com']
	sendTestreport(to_list,'生产行业类型消耗','</pre><h1>你好</h1><pre>')
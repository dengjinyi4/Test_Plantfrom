#encoding:utf-8
import requests as r
import sendmaildb as mydb
import Emar_SendMail_Attachments as emarmail
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
linkresult=mydb.selectsql('''SELECT a.id,b.creative_id,c.link_common from voyager.ad_order a,voyager.ad_order_creative b,voyager.ad_creative_link c
where a.id=b.order_id and b.creative_id=c.creative_id and a.state=4 and c.is_valid=1 and b.state=1 ;''')
tmplist=[]
req=r.session()
# opener=urllib2.urlopen()
# opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]
for url in linkresult:
   try:
        # opener.open(url)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        result=r.get(str(url[2]).strip(),headers=headers,timeout=2)
        # if str(result.status_code)<>'200' :
        #    # print 'ok'
        # # else:
        #     tmplist.append(url)
        #     print '失败了，订单是：{0}创意id是：{1} url:{2} 返回码是：{3} 错误码是{4}'.format(url[0],url[1],url[2],result.status_code,result.raise_for_status())
   except Exception as e:
       print url
       tmplist.append(url)
print tmplist
mail='''&emsp;&emsp;<table border=1 cellspacing=0><tr><td>订单id</td><td>创意id</td><td>url</td></tr>'''
for i in tmplist:
    mail=mail+'''<tr><td>{}</td><td>{}</td><td>{}</td></tr>'''.format(str(i[0]),str(i[1]),str(i[2]))
mail=mail+'''</table>'''
emarmail.sendTestreport(['dengjinyi@emar.com'],'url检查',mail)
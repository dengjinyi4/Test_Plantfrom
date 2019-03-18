# encoding=utf-8
import urllib, urllib2, sys
import ssl
import requests as r


# re=r.session()
host1 = 'https://api01.aliyun.venuscn.com'
# # re.headers ={'Authorization': 'APPCODE 870b5c272b134c6396bb1f66ad1b588b'}
# headers = {'Authorization': 'APPCODE 870b5c272b134c6396bb1f66ad1b588b'}
# param={'ip':'117.136.57.129'}
# result=r.get(host1,headers=headers,params=param,verify=True)
# print result.url
# print result
# print result.headers

#
path = '/ip'
method = 'GET'
appcode = '870b5c272b134c6396bb1f66ad1b588b'
# querys = 'ip=223.104.36.126'
querys = 'ip=117.136.57.166'
bodys = {}
url = host1 + path + '?' + querys

request = urllib2.Request(url)
request.add_header('Authorization', 'APPCODE ' + appcode)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
response = urllib2.urlopen(request, context=ctx)
content = response.read()
if (content):
    print(content)

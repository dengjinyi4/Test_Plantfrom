# -*- coding: utf-8 -*-
import time
import sys,json
reload(sys)
sys.setdefaultencoding('utf8')

"""
    author：jinyi
    data：2020-05-26
    公共的方法类
"""
class BaseTools(object):
    def __init__(self,tmpstr):
        self.tmpstr=tmpstr
    def do(self):
        re={}
        tmp=int(self.tmpstr[8:18],36)/100000
        shijian=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(tmp))
        re['tag'] = self.tmpstr
        re[u"时间"]=shijian
        tmp=self.tmpstr[:1]
        if tmp=="B":
            re[u"业务"]="广告位点击"
        elif tmp=="E":
            re[u"业务"]="广告点击"
        elif tmp=="D":
            re[u"业务"]="广告展现"
        elif tmp=="C":
            re[u"业务"]="抽奖"
        else:
            re[u"业务"]="不能解析"
        re["ip"]=str(int(self.tmpstr[1:3],36))+"."+str(int(self.tmpstr[3:5],36))
        re[u'端口']=str(int(self.tmpstr[5:8],36))

        return json.dumps(re, ensure_ascii=False)
        # return re
if __name__ == '__main__':
    tmpstr = ['B0H39DC11KFNSFPALD']
    print len(tmpstr)
    result=[]
    for i in range(0,len(tmpstr)):

      tmp=BaseTools('B0H39DC11KFNSFPALD')

      re=tmp.do()
      result.append(re)
    print  result


    # tmp="www.runoob.com"
    # print tmp[4:]
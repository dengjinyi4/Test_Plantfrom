# -*- coding:utf-8 -*-
import datetime
import sys,collections
import db
import json
class media(object):
    # 媒体名称
    media_name=''
    # 媒体id
    media_id=''
    # 日期
    day=''
    def __init__(self,day):
        self.day=day
    #     获取需要汇总的媒体和广告位
    def getmediainfor(self):
        # tmpsql='SELECT rz.media_id,bmi.media_name,rz.adzone_id,bai.adzone_name ' \
        #        'from voyager.report_zone rz ,voyager.base_media_info bmi ,voyager.base_adzone_info bai ' \
        #        'where rz.adzone_id=bai.id and rz.media_id=bmi.id and rz.date=\'{}\' and  rz.adzone_consume>0 and rz.media_id<>2 ORDER BY media_id limit 13 '.format(self.day)
        tmpsql='SELECT DISTINCT adl.media_id, bmi.name,adl.adzone_id,bai.adzone_name from voyagerlog.ad_effect_log_{} adl,voyager.base_media_info bmi ,voyager.base_adzone_info bai ' \
               'where  adl.media_id=bmi.id and adl.adzone_id=bai.id and DAY(adl.update_time)={} and MONTH(adl.update_time)={} ' \
               'and adl.media_id is NOT null and adl.adzone_id is NOT null limit 150'.format(self.day[4:6],self.day[6:8],self.day[4:6])
        result=db.selectsql('devvoyager',tmpsql)
        return result
    # 对接API加粉广告主ID 今天有预算的加粉广告主 广告主状态是审核成功 在eff表查
    def getadver_43_api(self):
        tmpsql='SELECT DISTINCT ad.id from voyager.advertiser ad,voyager.advertiser_balance_pre_deduction abd ' \
               'where ad.id=abd.advertiser_id and abd.consumer_date=\'{}\' and ad.industry_id=43 and ad.state= 2'.format(self.day)
        result=db.selectsql('devvoyager',tmpsql)
        # print result
        return self.tuptolist(result)
    def get_clickcount(self):
        adver43=self.getadver_43_api()
        getmediainfor=self.getmediainfor()
        # 存储每个广告点击效果时间和点击时间差值
        tmplist=[]
        # 存储最终的数据
        tmpalllmedia=[]

        for media in getmediainfor:
            # 存储每个媒体的数据字典形式
            tmpditmedia={}
            tmpadclick='SELECT DISTINCT ade.ad_click_tag,ade.update_time,adc.create_time,min(ade.update_time-adc.create_time) from voyagerlog.ad_effect_log_{} ade ,voyagerlog.ad_click_log{} adc ' \
                       'where MONTH(ade.update_time)={} and  day(ade.update_time)={} and ade.ad_click_tag is NOT NULL ' \
                       'AND  ade.ad_click_tag=adc.ad_click_tag and ade.media_id={} and ade.adzone_id={} and ade.advertiser_id in {} ' \
                       'GROUP BY ade.ad_click_tag;'.format(self.day[4:6],self.day,self.day[4:6],self.day[6:8],media[0],media[2],adver43)
            print tmpadclick
            # 查询出单个广告位上加粉广告主的效果时间和广告点击时间
            result=db.selectsql('devvoyager',tmpadclick)
            tmplist1=[]
            # 将每个媒体中的数据保存在一个list中
            tmplist2=[]
            # 复制微信有效（5,120）PV
            copywxuv=0
            # 首次uv复制有效总用时
            uvfirsttime=0
            if len(result)>0:
                for adclickupdate in result:
                    tmplist=self.tmplist(tmplist1,adclickupdate[3])
                    # uvfirsttime=pvtime+adclickupdate[3]
                    # m=collections.Counter(tmplist)
                tmpuv=collections.Counter(tmplist).items()
                uvlist=['<5uv','>120uv','5120uv']
                for i in uvlist:
                    for j in tmpuv:
                        if j[0]==i:
                            tmpditmedia[i]=j[1]
                            break
                        else:
                            tmpditmedia[i]=0

                copywxuv,fcount=self.tfcount(collections.Counter(tmplist).items())
                tmpditmedia['media_id']=media[0]
                tmpditmedia['media_name']=media[1]
                tmpditmedia['adzone_id']=media[2]
                tmpditmedia['adzone_name']=media[3]
                # tmpditmedia['uvfirsttime']=uvfirsttime
                tmpditmedia['copywxuv']=copywxuv
                # 有效pv停留总时长
                pvtime=0
                tmpsql='SELECT  sum(ade.update_time-adc.create_time) from voyagerlog.ad_effect_log_{} ade ,voyagerlog.ad_click_log{} adc ' \
                       'where MONTH(ade.update_time)={} and  day(ade.update_time)={} and ade.ad_click_tag is NOT NULL ' \
                       'AND  ade.ad_click_tag=adc.ad_click_tag and ade.media_id={} and ade.adzone_id={} and ade.advertiser_id in {}  ' \
                       ';'.format(self.day[4:6],self.day,self.day[4:6],self.day[6:8],media[0],media[2],adver43)
                result=db.selectsql('devvoyager',tmpsql)
                if len(result)>0:
                    tmpditmedia['pvtime']=result[0]
                else:
                    tmpditmedia['pvtime']=0
                tmpuv='SELECT  ade.ad_click_tag,ade.update_time,adc.create_time,ade.update_time-adc.create_time from voyagerlog.ad_effect_log_{} ade ,voyagerlog.ad_click_log{} adc ' \
                       'where MONTH(ade.update_time)={} and  day(ade.update_time)={} and ade.ad_click_tag is NOT NULL ' \
                       'AND  ade.ad_click_tag=adc.ad_click_tag and ade.media_id={} and ade.adzone_id={} and ade.advertiser_id in {}  '.format(self.day[4:6],self.day,self.day[4:6],self.day[6:8],media[0],media[2],adver43)
                result=db.selectsql('devvoyager',tmpuv)
                print tmpuv
                if len(result)>0:
                    tmplist1=[]
                    for i in result:
                        tmplist=self.tmplistpv(tmplist1,i[3])
                tmppv=collections.Counter(tmplist).items()
                pvlist=['<5pv','>120pv','5120pv']
                for i in pvlist:
                    for j in tmppv:
                        if j[0]==i:
                            tmpditmedia[i]=j[1]
                            break
                        else:
                            tmpditmedia[i]=0
                tmplist2.append(tmpditmedia)
            else:
                tmpditmedia[media]=[0,0,0,0,0,0]
                tmplist2.append(tmpditmedia)
            tmpalllmedia.append(tmplist2)
        print '*'*20
        print  str(tmpalllmedia).decode('string_escape')
        print '*'*20
        return tmpalllmedia
    # 将查询数据库返回的tup转换成字符串，为拼接sql使用 暂时没有使用
    def tuptolist(self,tmptup):
        # tmptup=((4261L,), (4234L,), (4260L,), (1283L,), (5074L,), (4689L,), (4861L,))
        tmpstr=''
        for i in tmptup:
            tmpstr=tmpstr+str(i[0])+','
        tmpstr=tmpstr[0:-1]
        tmpstr='('+tmpstr+')'
        # print tmpstr
        return tmpstr
    # 根据时长返回标识位，方便后续统计
    def tmplist(self,tmp,ad_u_c):
        if ad_u_c<5:
            tmp.append('<5uv')
            return tmp
        if ad_u_c>=5 and ad_u_c<120:
            tmp.append("5120uv")
            return tmp
        if ad_u_c>=120:
            tmp.append(">120uv")
            return tmp
            # return tmp.append("B")
    def tmplistpv(self,tmp,ad_u_c):
        if ad_u_c<5:
            tmp.append('<5pv')
            return tmp
        if ad_u_c>=5 and ad_u_c<120:
            tmp.append("5120pv")
            # tmp.append("A")
            return tmp
        if ad_u_c>=120:
            return tmp.append(">120pv")
            # return tmp.append("B")
    def tfcount(self,tpm):
        # tpm=[('小于5',22),('大于120',11),('5到120',13)]
        # 有效uv
        tcount=0
        fcount=0
        for i in tpm:
            if i[0]=='5120uv':
                tcount=tcount+i[1]
            if i[0]=='<5pv' or i[0]=='>120pv':
                fcount=fcount +i[1]
        return tcount,fcount
if __name__ == '__main__':
    test=media(day='20190822')
    # test.getmediainfor()
    test.get_clickcount()
    # test.tuptolist()

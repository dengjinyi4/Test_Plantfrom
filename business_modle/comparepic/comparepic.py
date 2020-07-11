# -*- coding: utf-8 -*-
__author__ = 'jinyi'
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# 图片对比
from PIL import Image
from PIL import ImageChops
import os
import requests as r
from business_modle.querytool import db


class comparepic(object):
    def __init__(self,env='',plantfrom=''):
        self.env=env
        self.plantfrom=plantfrom

    def getactremark(self):
        tmpsql='''SELECT remark from voyager.base_act_info where id=5188'''
        if self.env=='test':
            re=db.selectsql("testvoyager",tmpsql)
        return eval(re[0][0])
    def getactpicpathyiqifa(self):
        tmpsql='''SELECT PRODUCT_NAME,PRODUCT_IMG FROM interest_product where CREATE_TIME>'2020-07-09' '''
        if self.env=='test':
            re=db.selectsql("testtest",tmpsql)
        tmp={}
        for i in re:
            tmp[i[0]]=i[1]
        print tmp
        print type(tmp)
        return tmp
    #     对比图片是否相同
    def diffpic(self,picpath1,picpath2):
        # picpath1='pic/1.jpg'
        # picpath2='pic/2.jpg'
        # picpath1=unicode(picpath1,'utf-8')
        # picpath2=unicode(picpath2,'utf-8')
        print picpath1,picpath2
        dif=ImageChops.difference(Image.open(picpath1),Image.open(picpath2)).getbbox()
        if dif is None:
            return True
        else:
            return False
    #    活动配置一键上传数据
    def getpicpeizhi(self):
        filePath='''D://pic//sunli//configImgs'''
        # 取得文件夹下所有文件的名字
        picname=os.listdir(filePath)
        # picname.remove('__init__.py')
        allpicxuli=['bgImg.png','plotFruit1.png','plotFruit2.png','plotFruit3.png','plotFruit4.png','plotFruit5.png','plotFruit6.png','plotFruit7.png','landBg.png','HandBookLiBg.png','buttonCommon.png','soilFront.png','soil.png','cirrusBg.png','sapling1.png','sapling2.png','sapling3.png','sapling4.png','sapling5.png','sapling6.png','sapling7.png','mainFruits1.png','mainFruits2.png','mainFruits3.png','mainFruits4.png','mainFruits5.png','mainFruits6.png','mainFruits7.png','userGiftPopbg.png','userGiftBalloon.png','userGiftBox.png','lotteryBg.png','offlineBg.png','offlineTWBg.png','coinDoubleLayer.png','pubCloseBtn.png','taskListLiBg.png','taskList.png','bottomBar.png','bottomTitle.png','iconBig.png','moneyBg.png','makeMoneyLibg.png','bottomPopbg.png','bottomPopbgUp.png','bottomPopBTMbg.png','makeMoenyNo.png','farmliBg.png','kettleBg.png','barrow.png','menBg.png','iconAll1.png','iconAll2.png','ruleBg.png','iconMain.png','house.png','windWill2.png','windWill1.png','tipBg.png']
        # tmppeizhipic=[i for i in allpicxuli if i not in picname]
        tmppeizhipic=[i for i in  picname  if i not in allpicxuli ]
        # print tmppeizhipic
        print '8'*10
        tmp=''
        for pic in picname:
            # 只处理图片其他文件类型不处理
            tmppic=['png','jpg','gif']
            if pic.split('.')[1] in tmppic:
                im=Image.open(filePath+'/'+pic)
                # print filePath+'/'+pic
                tmp=tmp+"tu|{name}|image|1|{pictype}|{k}|{g}|".format(name=pic.split('.')[0],pictype=pic.split('.')[1],k=str(im.size[0]),g=str(im.size[1]))+'\n'
                # tmppeizhipic.append(tmp)
        # print tmppeizhipic
        return tmp
    def imgurl(self,url):
        if 'http://' in url or 'https://' in url:
            return url
        else:
            return 'http:'+url
    # 下载图片 并且对比图片
    def downpic(self):
        if self.plantfrom=='hdt':
            # 数据库里的act表中的remark字段
            tmpdict=self.getactremark()
        if self.plantfrom=='yqf':
            tmpdict=self.getactpicpathyiqifa()
        localpicpath='./pic/'
        for i in tmpdict:
            downloadpicname=str(i)+str(tmpdict[i][-4:])
            # picurl='''https://img3.adhudong.com/award/201810/17/b1661caa187eb6f9fb3c6b2c0d8797c8.jpg'''
            re=r.get(self.imgurl(tmpdict[i]))
            downloadpic='./download/{downloadpicname}'.format(downloadpicname=downloadpicname)
            downloadpic=unicode(downloadpic,'utf8')
            with open(downloadpic,'wb') as f:
            # with open(downloadpic.decode('unicode_escape'),'wb') as f:
                f.write(re.content)
            localpic=localpicpath+downloadpicname
            localpic=unicode(localpic,'utf8')
            if not self.diffpic(localpic,downloadpic):
                print '图片不一致，本地图片是{localpic}，服务器图片是：{downloadpic}'.format(localpic=localpic,downloadpic=downloadpic)
            else:
                print '图片一致，本地图片是{localpic}，服务器图片是：{downloadpic}'.format(localpic=localpic,downloadpic=downloadpic)
        return 1
    def downpicyiqifa(self):
        tmpdict=self.getactpicpathyiqifa()
        localpicpath='./pic/'

        return 1

if __name__ == '__main__':
    mypic=comparepic(env='test',plantfrom='yqf')
    re=mypic.downpic()
    # re=mypic.getpicpeizhi()
    # re=mypic.getactpicpathyiqifa()
    print re



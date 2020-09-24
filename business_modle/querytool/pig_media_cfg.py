# encoding=utf-8
__author__ = 'aidinghua'

from business_modle.querytool.utils.db_info  import *
import datetime
import os
from dateutil.relativedelta import relativedelta
from openpyxl import  Workbook,load_workbook
import os


class Mypig(object):

    def __init__(self,env_value):

     self.db=DbOperations(env_value=env_value)

# 导出excel
#     def exportexcel(self,filed,res,excelname):
#         if len(res)<>0:
#             res=list(res)
#             # res.insert(0,headtr)
#             res.insert(0,filed)
#             wb=Workbook()
#             sheet=wb.active
#             for i in range(len(res)):
#                 sheet.append(res[i])
#             try:
#                 # wb.save("../../../static/result/reportall.xlsx")
#                 wb.save("./static/result/{0}.xlsx".format(excelname))
#             except Exception as e:
#                 print e.message
#         return ''

##配置表名以及注释

    def pig_config_table(self):
        tmpsql='''SELECT TABLE_NAME '表名',TABLE_COMMENT '表备注' FROM
                information_schema.`TABLES` WHERE
                `TABLE_SCHEMA` = 'yijifen'
            AND  `TABLE_NAME` LIKE 'pig%'  '''

        res,field=self.db.selectsqlnew(tmpsql)
        return res,field,tmpsql
#####福气值单元配置表

    def pigunit_config_table(self):

        tmpsql=''' SELECT * FROM yijifen.pigs_lucky_unit '''

        res_unit,field_unit=self.db.selectsqlnew(tmpsql)

        return res_unit,field_unit,tmpsql

    def pigunit_conf_note(self):
        tmpsql=''' SELECT column_name 字段名,column_comment 字段释义  FROM information_schema.columns WHERE table_schema = 'yijifen' AND table_name ='pigs_lucky_unit';  '''
        res_unitnote,field_unitnote=self.db.selectsqlnew(tmpsql)
        return res_unitnote,field_unitnote,tmpsql


##养猪媒体相关配置
    def pig_media_conf(self):

        tmpsql=''' SELECT id ID,media_id 媒体ID,user_rating 用户评级,red_packet 红包上限,watch_video_total 观看视频次数限制  FROM yijifen.pigs_media_cfg;  '''
        res,field=self.db.selectsqlnew(tmpsql)

        return res,field,tmpsql

    def pig_media_conf_note(self):
        tmpsql=''' SELECT column_name 字段名,column_comment 字段释义  FROM information_schema.columns WHERE table_schema = 'yijifen' AND table_name ='pigs_media_cfg';  '''
        res,field=self.db.selectsqlnew(tmpsql)
        return res,field,tmpsql

##养猪模块红包分配表

    def pig_red_conf(self):

        tmpsql=''' SELECT *  FROM yijifen.pigs_media_red; '''
        res_red,field_red=self.db.selectsqlnew(tmpsql)

        return res_red,field_red,tmpsql

    def pig_red_conf_note(self):
        tmpsql=''' SELECT column_name 字段名,column_comment 字段释义  FROM information_schema.columns WHERE table_schema = 'yijifen' AND table_name ='pigs_media_red';  '''
        res_rednote,field_rednote=self.db.selectsqlnew(tmpsql)
        return res_rednote,field_rednote,tmpsql

##猪等级配置表
    def pig_level_conf(self):

        tmpsql=''' SELECT *  FROM yijifen.pigs_piglevel; '''
        res_level,field_level=self.db.selectsqlnew(tmpsql)

        return res_level,field_level,tmpsql

    def pig_level_conf_note(self):
        tmpsql=''' SELECT column_name 字段名,column_comment 字段释义  FROM information_schema.columns WHERE table_schema = 'yijifen' AND table_name ='pigs_piglevel';  '''
        res_levelnote,field_levelnote=self.db.selectsqlnew(tmpsql)
        return res_levelnote,field_levelnote,tmpsql

#####视频坑位与操作日志类型对照表

    def pig_positionlog_conf(self):

        tmpsql=''' SELECT *  FROM yijifen.pigs_position_vedio; '''
        res_positionlog,field_positionlog=self.db.selectsqlnew(tmpsql)

        return res_positionlog,field_positionlog,tmpsql

    def pig_positionlog_conf_note(self):
        tmpsql=''' SELECT column_name 字段名,column_comment 字段释义  FROM information_schema.columns WHERE table_schema = 'yijifen' AND table_name ='pigs_position_vedio';  '''
        res_positionlognote,field_positionlognote=self.db.selectsqlnew(tmpsql)
        return res_positionlognote,field_positionlognote,tmpsql

#####基础信息配置表
    def pig_task_conf(self):

        tmpsql=''' SELECT *  FROM yijifen.pigs_tasks_cfg; '''
        res_task,field_task=self.db.selectsqlnew(tmpsql)

        return res_task,field_task,tmpsql

    def pig_task_conf_note(self):
        tmpsql=''' SELECT column_name 字段名,column_comment 字段释义  FROM information_schema.columns WHERE table_schema = 'yijifen' AND table_name ='pigs_tasks_cfg';  '''
        res_tasknote,field_tasknote=self.db.selectsqlnew(tmpsql)
        return res_tasknote,field_tasknote,tmpsql



#####解锁红包类型对照表

    def pig_unlock_conf(self):

        tmpsql=''' SELECT *  FROM yijifen.pigs_unlock_red; '''
        res_unlock,field_unlock=self.db.selectsqlnew(tmpsql)

        return res_unlock,field_unlock,tmpsql

    def pig_unlock_conf_note(self):
        tmpsql=''' SELECT column_name 字段名,column_comment 字段释义  FROM information_schema.columns WHERE table_schema = 'yijifen' AND table_name ='pigs_unlock_red';  '''
        res_unlocknote,field_unlocknote=self.db.selectsqlnew(tmpsql)
        return res_unlocknote,field_unlocknote,tmpsql


######用户等级对照表
    def pig_userlevel_conf(self):

        tmpsql=''' SELECT *  FROM yijifen.pigs_userlevel; '''
        res_userlevel,field_userlevel=self.db.selectsqlnew(tmpsql)

        return res_userlevel,field_userlevel,tmpsql

    def pig_userlevel_conf_note(self):
        tmpsql=''' SELECT column_name 字段名,column_comment 字段释义  FROM information_schema.columns WHERE table_schema = 'yijifen' AND table_name ='pigs_userlevel';  '''
        res_userlevelnote,field_levelnote=self.db.selectsqlnew(tmpsql)
        return res_userlevelnote,field_levelnote,tmpsql




if __name__=='__main__':

    result = Mypig('False').pig_media_conf()

    print result




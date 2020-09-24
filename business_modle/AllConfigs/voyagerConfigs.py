# -*- coding: utf-8 -*-
# @Time    : 2020/7/24 19:16
# @Author  : wanglanqing


from business_modle.querytool import db

class VoyagerConfigs(object):
    def __init__(self, db_env='testvoyager'):
        self.db_env = db_env


    def get_act_game_cfgs(self):
        #查询养成活动的表信息
        # sql1 = """use information_schema;"""
        sql2 = """SELECT TABLE_NAME '表名',TABLE_COMMENT '表备注' FROM
                information_schema.`TABLES` WHERE
                `TABLE_SCHEMA` = 'voyager'
            AND (`TABLE_NAME` LIKE '%cfg%'
						or `TABLE_NAME` LIKE '%config%')
            AND  `TABLE_NAME` LIKE 'act_game%';"""
        print self.db_env
        # db.selectsqlnew(self.db_env, sql1)
        re=db.selectsqlnew(self.db_env, sql2)
        if re:
            return db.selectsqlnew(self.db_env, sql2)
        else:
            return "没有查询到结果"

    def get_other_cfgs(self):
        #查询其他配置表信息
        # sql1 = """use information_schema;"""
        sql2 = """SELECT TABLE_NAME '表名',TABLE_COMMENT '表备注' FROM
                information_schema.`TABLES` WHERE
                `TABLE_SCHEMA` = 'voyager'
            AND (`TABLE_NAME` LIKE '%cfg%' or `TABLE_NAME` LIKE '%config%')
            AND  `TABLE_NAME` not LIKE '%act_game%';"""
        # db.selectsqlnew(self.db_env, sql1)
        re=db.selectsqlnew(self.db_env, sql2)
        if re:
            return db.selectsqlnew(self.db_env, sql2)
        else:
            return "没有查询到结果"
    def get_pig_act_game_cfgs(self):
        #查询养成活动的表信息
        # sql1 = """use information_schema;"""
        sql2 = """  SELECT TABLE_NAME '表名',TABLE_COMMENT '表备注' FROM
                information_schema.`TABLES` WHERE
                `TABLE_SCHEMA` = 'yijifen'
            AND  `TABLE_NAME` LIKE 'pig%';"""
        print self.db_env
        # db.selectsqlnew(self.db_env, sql1)
        re=db.selectsqlnew(self.db_env, sql2)
        if re:
            return db.selectsqlnew(self.db_env, sql2)
        else:
            return "没有查询到结果"

    def get_selected_table_cfg(self,selected_table):
        sql = "select * from voyager.{} order by id desc;".format(selected_table)
        sql2= """select COLUMN_NAME '字段',COLUMN_TYPE '类型',COLUMN_COMMENT '备注' from information_schema.columns where table_schema = 'voyager'
        and table_name = '{}' ;""".format(selected_table)
        print sql,sql2
        re1=db.selectsqlnew(self.db_env, sql)
        re2=db.selectsqlnew(self.db_env,sql2)
        if isinstance(re1,str):
            return re1
        elif isinstance(re1,tuple) and isinstance(re2,tuple):
            return db.selectsqlnew(self.db_env, sql), db.selectsqlnew(self.db_env,sql2)
        else:
            return "没有查询到结果"




    def get_pig_selected_table_cfg(self,selected_table):
        sql = "select * from yijifen.{} order by id desc;".format(selected_table)
        sql2= """select COLUMN_NAME '字段',COLUMN_TYPE '类型',COLUMN_COMMENT '备注' from information_schema.columns where table_schema = 'yijifen'
        and table_name = '{}' ;""".format(selected_table)
        print sql,sql2
        re1=db.selectsqlnew(self.db_env, sql)
        re2=db.selectsqlnew(self.db_env,sql2)
        if isinstance(re1,str):
            return re1
        elif isinstance(re1,tuple) and isinstance(re2,tuple):
            return db.selectsqlnew(self.db_env, sql), db.selectsqlnew(self.db_env,sql2)
        else:
            return "没有查询到结果"




if __name__ == '__main__':
    vc = VoyagerConfigs(db_env='devvoyager')
    print vc.get_selected_table_cfg('config_parameters_copy1')
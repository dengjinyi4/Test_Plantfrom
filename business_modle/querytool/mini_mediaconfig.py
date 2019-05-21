# encoding=utf-8

__author__ = 'aidinghua'

from utils.dtdb_info import *

from business_modle.querytool.utils.adh_bejson import *

class Manage_media(object):

    def __init__(self):

        self.db=DtdbOperations()

    def medialist(self):

        keys = 'id,name,create_time,update_time'

        sql =''' SELECT id,name,create_time,update_time FROM ditandaka.wx_user_source_cfg  '''

        result = self.db.execute_sql(sql)
        print result

        # return result
        return adh_bejson.trans(keys.split(','),result)


    def add_media(self,formdata):

        keys = str(formdata.keys())[1:-1].replace("'","")

        values=json.dumps(formdata.values(),ensure_ascii=False,encoding='utf-8')[1:-1]

        sql = '''insert into ditandaka.wx_user_source_cfg ({}) values({}); '''.format(keys,values)

        self.db.execute_sql(sql)
        self.db.mycommit()




if  __name__=='__main__':

    mc = Manage_media()

    print mc.medialist()





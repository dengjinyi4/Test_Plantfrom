# encoding=utf-8
__author__ = 'aidinghua'

from utils.db_info import *

class Crmproduct_info(object):

    def __init__(self,product_id,env_value=False):

       self.db=DbOperations(env_value=env_value)

       self.product_id = product_id



    def show_result(self):

        sql = '''
              SELECT
              product_id 商品ID,
              NAME 商品名称,
              content 内容,
              CASE
                WHEN STATUS=1  THEN '有效'
                WHEN STATUS=2  THEN '无效'
              END 状态,
              CASE
                WHEN TYPE=1 THEN '套餐'
                WHEN TYPE=2 THEN '属性'
              END 类型
              FROM
              voyager.crm_product_ext
              WHERE product_id = {}
              and status=1
              '''.format(self.product_id)
        result = self.db.execute_sql(sql)

        # print type(result)
        # print result

        # for row in result:
        #     print row
        #     for col in row:
        #         print col

        return result








if __name__=='__main__':

    cpi=Crmproduct_info(808,False)

    print cpi.show_result()



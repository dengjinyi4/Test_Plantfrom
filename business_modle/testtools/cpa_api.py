# encoding=utf-8
__author__ = 'aidinghua'

import requests
import json
import datetime
from utils import db_info

class Cpa_api(object):

  def __init__(self,ad_choosen_tag,device_id,timestamp,env_value=True):

     self.db=db_info.DbOperations(env_value=env_value)
     self.ad_choosen_tag=ad_choosen_tag
     self.device_id = device_id
     self.timestamp = timestamp

  def cpa_api(self):

     url= "http://101.254.242.11:17110/saveEffectCPA.htm"
     postData ={"ad_choosen_tag":self.ad_choosen_tag,"dev_id":self.device_id ,"timestamp":self.timestamp}

     r=requests.post(url,data=postData)

     return r.text
  def month(self):

      month = datetime.datetime.now().month
      if month<10:
          return  "0"+str(month)
      else:
          return  month

  def show_result(self):

      show_sql=r"""

      SELECT
      ad_click_tag,
      TYPE,
      uid,
      adzone_id,
      media_id,
      advertiser_Id,
      ad_order_Id,
      ad_creative_id,
      act_id,
      position_id,
      dev_id,
      price,
      create_time,
      update_time,
      ad_choosen_tag,
      adzone_click_id,
      charge_amount,
      media_income_cash,
      media_income_award,
      ua
      FROM
      voyagerlog.ad_effect_log_{}
      WHERE ad_choosen_tag ='{}' """.format(self.month(),self.ad_choosen_tag)

      result = self.db.execute_sql(show_sql)

      return  result



if __name__=='__main__':
    cpa=Cpa_api("D3W1CD6R1IFO0H6KF5","123123","2018-08-31 00:01:00",env_value=True)
    print cpa.cpa_api()
    print cpa.show_result()


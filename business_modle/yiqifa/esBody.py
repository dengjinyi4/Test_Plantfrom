#!flask/bin/env python
#coding:utf-8
from hdt_tools.utils import DbConnection as fb
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
def Body(actionType,dataSource,esKeyValue,cdpValue,myenv):
    if esKeyValue=="actionNo" and cdpValue!="" and actionType !="all": #查询单个订单号
        body={
    "query": {
        "bool":{
          "must": [
            {"term": {
              "dataSource": {
                "value": ""
              }
            }},
            {"term": {
              "actionType": {
                "value": ""
              }
            }},
            {"term": {
               "actionNo": {
                "value": ""
              }
            }}
          ]
        }
    },
  "sort" : [ {
    "actionTime" : {
      "order" : "desc"
    }
  } ]
}
        body['query']["bool"]['must'][0]['term']['dataSource']="{0}".format(dataSource)
        body['query']["bool"]['must'][1]['term']['actionType']="{0}".format(actionType)
        body['query']["bool"]['must'][2]['term']['actionNo']="{0}".format(cdpValue)
    elif esKeyValue=="actionNo" and cdpValue=="" and actionType !="all": #查询订单List
        body={
    "query": {
        "bool":{
          "must": [
            {"term": {
              "dataSource": {
                "value": ""
              }
            }},
            {"term": {
              "actionType": {
                "value": ""
              }
            }}
          ]
        }
    },
  "sort" : [ {
    "actionTime" : {
      "order" : "desc"
    }
  } ]
}
        body['query']["bool"]['must'][0]['term']['dataSource']="{0}".format(dataSource)
        body['query']["bool"]['must'][1]['term']['actionType']="{0}".format(actionType)
    elif esKeyValue=="actionNo" and cdpValue=="" and actionType =="all":  #查询all信息
        body={
    "query": {
        "bool":{
          "must": [
            {"term": {
              "dataSource": {
                "value": ""
              }
            }}
          ]
        }
    },
  "sort" : [ {
    "actionTime" : {
      "order" : "desc"
    }
  } ]
}
        body['query']["bool"]['must'][0]['term']['dataSource']="{0}".format(dataSource)
    elif esKeyValue=="actionNo" and cdpValue !="" and actionType =="all":
        body={
    "query": {
        "bool":{
          "must": [
            {"term": {
              "dataSource": {
                "value": ""
              }
            }},
            {"term": {
               "actionNo": {
                "value": ""
              }
            }}
          ]
        }
    },
  "sort" : [ {
    "actionTime" : {
      "order" : "desc"
    }
  } ]
}
        body['query']["bool"]['must'][0]['term']['dataSource']="{0}".format(dataSource)
        body['query']["bool"]['must'][1]['term']['actionNo']="{0}".format(cdpValue)
    elif esKeyValue=="cdpid" and cdpValue!="" and actionType =="all":  #查询cdpid信息
        sqlDb="SELECT  * FROM fanxian.cdp_user_mapper WHERE cdp_id ="+cdpValue+"";
        results = fb.ExecuteSelectList(sqlDb,"mysql_fanxian")
        tmplist=[]
        dict ={}
        for rs in results :
            dict = {
      "terms": {
        rs[2]: [
          rs[3],
        ]
    }}
            tmplist.append(dict)
        # should = json.dumps(tmplist, encoding='utf-8', ensure_ascii=False) #搜索条件值
        # print tmplist, type(tmplist)
        body={
"query" : {
"bool" : {
  "must" : [ {
    "term" : {
      "dataSource" : ""
    }
  }
  ],
  "should":''
}
},"sort": [
  {
    "actionTime": {
      "order": "desc"
    }
  }
]
}
        body['query']["bool"]['must'][0]['term']['dataSource']="{0}".format(dataSource)
        body['query']["bool"]['should']=tmplist #替换搜索条件
    elif esKeyValue=="cdpid" and cdpValue!="" and actionType !="all":  #查询cdpid信息
        sqlDb="SELECT  * FROM fanxian.cdp_user_mapper WHERE cdp_id ="+cdpValue+"";
        results = fb.ExecuteSelectList(sqlDb,"mysql_fanxian")
        tmplist=[]
        dict ={}
        for rs in results :
            dict = {
      "terms": {
        rs[2]: [
          rs[3],
        ]
    }}
            tmplist.append(dict)
        body={
"query" : {
"bool" : {
  "must" : [ {
    "term" : {
      "dataSource" : ""
    }
  },
    {
    "term" : {
      "actionType" : ""
    }
  }
  ],
  "should":''
}
},"sort": [
  {
    "actionTime": {
      "order": "desc"
    }
  }
]
}
        body['query']["bool"]['must'][0]['term']['dataSource']="{0}".format(dataSource)
        body['query']["bool"]['must'][1]['term']['actionType']="{0}".format(actionType)
        body['query']["bool"]['should']=tmplist #替换搜索条件
    return body;

def BodyByActionNo(dataSource,actionNo):
     body={
    "query": {
        "bool":{
          "must": [
            {"term": {
              "dataSource": {
                "value": ""
              }
            }},
            {"term": {
               "actionNo": {
                "value": ""
              }
            }}
          ]
        }
    },
  "sort" : [ {
    "actionTime" : {
      "order" : "desc"
    }
  } ]
}

     body['query']["bool"]['must'][0]['term']['dataSource']="{0}".format(dataSource)
     body['query']["bool"]['must'][1]['term']['actionNo']="{0}".format(actionNo)
     return body
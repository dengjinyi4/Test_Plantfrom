#!/usr/bin/env python
#coding=utf-8
__author__ = 'jinyi'
import sys,os,pyotp,qrcode,hashlib,json
reload(sys)
sys.setdefaultencoding('utf8')
from utils import login as l
from business_modle.querytool import plantfromwtf as ft
from flask import session,request,g,jsonify,make_response
from flask import render_template,Blueprint,redirect,url_for,flash
myrestful = Blueprint('yjf_media', __name__,template_folder='templates')

# http://127.0.0.1:21312/media/add/success/
@myrestful.route('/<any(consume,refund,query):path>/',methods=['POST','GET'])
# @myrestful.route('/query/<any(success,fail):page_name>/',methods=('POST','GET'))
def query(path):
    if path == 'query':
        tmp = {"code": "E0000", "message": u"密钥错误", "data": "0"}
        # user_id = request.args['userId']
        # my_key = request.get_json()
        # # sign = request.args['sign']
        # if my_key['userId'] == 'errKey':
        #     tmp = {"code": "E0000", "message": u"密钥错误", "data": "0"}
        # else:
        #     tmp = {"code": "00000", "message": u"查询成功,该用户可用积分为10000", "data": "10000"}
    elif path == 'consume':
        tmp = {"code": "A0002", "message": u"用户不存在", "data": "2"}
        # my_key = request.get_json()
        # print  request.get_json()
        # user_id=my_key['userId']
        # if user_id == '1':
        #     tmp={"code":"00000","message":u"扣减成功","data":"1"}
        #     #userid=2,传参时使用user_id=3
        # elif user_id == '2':
        #     tmp = {"code": "A0001", "message": u"密钥校验失败", "data": "2"}
        # elif user_id == '3':
        #     tmp = {"code": "A0002", "message": u"用户不存在", "data": "2"}
        # elif user_id == '4':
        #     tmp = {"code": "A0003", "message": u"传参不正确", "data": "2"}
        # elif user_id == '5':
        #     tmp = {"code": "B0001", "message": u"用户积分不足", "data": "2"}
        # elif user_id == '6':
        #     tmp = {"code": "B0002", "message": u"订单号重复扣积分", "data": "2"}
        # else:
        #     tmp = {"code": "B0003", "message": u"其他", "data": "2"}
    elif path == 'refund':
        tmp = {"code": "B0003", "message": u"其他", "data": "2"}
        # orderId = request.get_json()['reason']
        # print orderId
        # if orderId == '1':
        #     tmp = {"code":"00000","message":u"退款成功","data":"1"}
        # else:
        #     tmp = {"code": "B0003", "message": u"其他", "data": "2"}
    #支持跨域
    response = make_response(jsonify(tmp))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return  response


# @myrestful.route('/<any(add,minus)>/<any(suc)>/',methods=('GET'))
# if __name__ == '__main__':
#     user=l.login()
#     picpath='../../static/qrcodepic/sssssssss.png'
#     img=user.otppic1()
#     try:
#         img.save(picpath)
#     except Exception as e:
#         print e.message


# if  __name__ == '__main__':
#     url = "http://localhost:21312/media/query/"
#     pyload = {"sign":"a8e492206fb246e3f1d7cbf2f16e9b47","userId":"errKey"}
#     d = request.post(url, data=pyload)
#     print d
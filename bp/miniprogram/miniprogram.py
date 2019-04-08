# encoding=utf-8
__author__ = 'aidinghua'

from flask import Blueprint ,render_template,request

from business_modle.querytool.punchcard import *
from business_modle.querytool.mini_mediainfo import *
from business_modle.querytool.mini_userinfo import *
from business_modle.querytool.media_report import *
from business_modle.querytool.media_reportnew import *


miniprogram=Blueprint('miniprogram',__name__)

@miniprogram.route('/punchcard',methods=['POST','GET'])
def punchcard():
    title = u"小程序用户信息"
    if request.method == 'GET':
        return render_template('punchcard.html',title=title)

    else:
        begin_date = request.form.get('begin_date')
        end_date = request.form.get('end_date')
        punchcard_result = Punchcard(begin_date,end_date,env_value=False)
        # paras = punchcard_result.user_info()
        total_amount = punchcard_result.total_amount()
        total_addamount=punchcard_result.today_addamount()
        invite_add=punchcard_result.invite_add()
        non_inviteadd=punchcard_result.non_inviteadd()
        today_sign=punchcard_result.today_sign()
        xvalue=punchcard_result.dateRange(begin_date,end_date)
        data=punchcard_result.add_user(begin_date,end_date)
        data2=punchcard_result.user_live(begin_date,end_date)
        return render_template('punchcard.html',total_amount=total_amount,today_addamount=total_addamount,today_sign=today_sign,begin_date=begin_date,end_date=end_date,xvalue=xvalue,data=data,data2=data2,invite_add=invite_add,non_inviteadd=non_inviteadd)

@miniprogram.route('/mini_mediainfo',methods=['POST','GET'])
def mini_mediainfo():

    title=u'小程序推广渠道数据统计'
    if request.method=='GET':
        return render_template('mini_mediainfo.html',title=title)

    else:
        begin_time=request.form.get('begin_time')
        media_dict={u"有练换换":"wx0a051787252f83fa",u"步数大联盟":"wxe65c34b4ec242be",u"优质福利所":"wx3c48ef7a45e89118"}
        media_info=request.form.get('media_name').strip()
        mediainfo=Media_report(media_dict[media_info],begin_time,env_value=False)
        authorize_user=mediainfo.authorize_user()
        wxstep_user=mediainfo.wxstep_user()
        invite_user=mediainfo.invite_user()
        invited_user=mediainfo.invited_user()
        task_user=mediainfo.task_user()
        return render_template('mini_mediainfo.html',begin_time=begin_time,media_name='<option selected="selected">'+media_info+'</option>',authorize_user=authorize_user,wxstep_user=wxstep_user,invite_user=invite_user,invited_user=invited_user,task_user=task_user)


@miniprogram.route('/media_report',methods=['POST','GET'])

def media_report():
    title=u'小程序媒体报表'
    if request.method=='GET':
        return render_template('media_report.html',title=title)
    else:
        begin_date=request.form.get('begin_date')
        end_date=request.form.get('end_date')
        media_dict={u"有练换换":"wx239bfcba6aeb0084",u"步数大联盟":"wxe65c34b4ec242be",u"优质福利所":"wx3c48ef7a45e89118",u'易购赚':'wx0a051787252f83fa',
                    u'遇见球球':'wxbb67c77aea9d76a8',u'开心游戏大乱斗':'wx2fa65dcf3dbe5926',u'十一光年':'wx42d12a5790960727',u'福礼惠公众号':'wx4ef839c292cb41ad',
                    u'我蹦我再蹦':'wx85d4b50441231b98',u'弹球大乱斗':'wx4aab7ee381936b54',u'APP-DSP光速动力':'1017757',u'手机弹幕小程序':'wx3fe2d608967de425',
                    u'智行火车票小程序':'wx76dcd806f382ec8e',u'步数换换乐':'wxd8de2f6276406b2a',u'打卡小日历':'wx18a2d299d1482fc0'}

        media_info= request.form.get('media_name').strip()

        if media_info==u'全部':

            mediareport= Media_report('1111',begin_date,end_date,env_value=False)

            adduser=mediareport.show_result2()
            liveuser=mediareport.liveuser2()
            authuser=mediareport.authuser2()

        else:
            mediareport= Media_report(media_dict[media_info],begin_date,end_date,env_value=False)

            adduser=mediareport.show_result()
            liveuser=mediareport.liveuser()
            authuser=mediareport.authuser()

        return render_template('media_report.html',begin_date=begin_date,end_date=end_date,media_name='<option selected="selected">'+media_info+'</option>',adduser=adduser,liveuser=liveuser,authuser=authuser)



@miniprogram.route('/media_reportnew',methods=['POST','GET'])

def media_reportnew():

    title=u'新小程序媒体报表'
    if request.method=='GET':

        live_type_info='<input type="radio" name="live_type" value="新增留存">新增留存'+'<input  type="radio" name="live_type"  value="活跃留存">活跃留存'


        return render_template('media_reportnew.html',title=title,live_type_info=live_type_info)

    else:
        begin_date=request.form.get('begin_date')
        end_date=request.form.get('end_date')
        live_type=request.form.get('live_type')
        print live_type
        media_dict={u"有练换换":"wx239bfcba6aeb0084",u"步数大联盟":"wxe65c34b4ec242be",u"优质福利所":"wx3c48ef7a45e89118",u'易购赚':'wx0a051787252f83fa',
                    u'遇见球球':'wxbb67c77aea9d76a8',u'开心游戏大乱斗':'wx2fa65dcf3dbe5926',u'十一光年':'wx42d12a5790960727',u'福礼惠公众号':'wx4ef839c292cb41ad',
                    u'我蹦我再蹦':'wx85d4b50441231b98',u'弹球大乱斗':'wx4aab7ee381936b54',u'APP-DSP光速动力':'1017757',u'手机弹幕小程序':'wx3fe2d608967de425',
                    u'智行火车票小程序':'wx76dcd806f382ec8e',u'步数换换乐':'wxd8de2f6276406b2a',u'打卡小日历':'wx18a2d299d1482fc0',u'玩赚签到':'wxefda0ea3619d87eb',
                    u'光微科技公众号':'880090',u'番茄小程序矩阵':'582068',
                    u'小麦圈打卡': 'wxd949b04824167683',
                    u'三言app': 'sanyan1017628',
                    u'小集盒': 'wx9bda6799b29d7868',
                    u'超级打投': 'wx5325ee83f4181dab',
                    u'淘新闻app': 'tqoxinwen001',
                    u'付呗':'1018004',
                    u'哆啦宝':'wx5c9a5ce20be8207b',
                    u'今天点餐吃什么':'wxc79d91f3a01dcd31',
                    u'八斗优选':'wxb09486b4d08778c7',
                    u'薪头条':'appID',
                    u'你包我猜':'wxdc39e4684804a8a5',
                    u'悦头条':'yuetoutiao',
                    u'车来了':'wx71d589ea01ce3321',
                    u'同程艺龙':'wx336dcaf6a1ecf632'}

        media_info= request.form.get('media_name').strip()

        if media_info==u'全部':

            if live_type==u'新增留存':

                if begin_date==end_date:

                   mediareport= Media_reportnew('1111',begin_date,end_date,env_value=False)

                   mediainfo=mediareport.add_result_one()
                   live_type_info='<input type="radio" name="live_type" checked  value="新增留存">新增留存'+'<input  type="radio" name="live_type"  value="活跃留存">活跃留存'
                else:
                    mediareport= Media_reportnew('1111',begin_date,end_date,env_value=False)

                    mediainfo=mediareport.add_result()

                    live_type_info='<input type="radio" name="live_type" checked  value="新增留存">新增留存'+'<input  type="radio" name="live_type"  value="活跃留存">活跃留存'


            else:

                if begin_date==end_date:

                  mediareport = Media_reportnew('1111',begin_date,end_date,env_value=False)

                  mediainfo=mediareport.live_result_one()

                  live_type_info='<input type="radio" name="live_type"   value="新增留存">新增留存'+'<input  type="radio" name="live_type" checked  value="活跃留存">活跃留存'
                else:
                    mediareport = Media_reportnew('1111',begin_date,end_date,env_value=False)

                    mediainfo=mediareport.live_result()
                    live_type_info='<input type="radio" name="live_type"   value="新增留存">新增留存'+'<input  type="radio" name="live_type" checked  value="活跃留存">活跃留存'



        else:

            if live_type==u'新增留存':

                mediareport= Media_reportnew(media_dict[media_info],begin_date,end_date,env_value=False)

                mediainfo=mediareport.add_result2()
                live_type_info='<input type="radio" name="live_type" checked  value="新增留存">新增留存'+'<input  type="radio" name="live_type"  value="活跃留存">活跃留存'
            else:

                mediareport=Media_reportnew(media_dict[media_info],begin_date,end_date,env_value=False)
                mediainfo=mediareport.live_result2()
                live_type_info='<input type="radio" name="live_type"  value="新增留存">新增留存'+'<input  type="radio" name="live_type" checked value="活跃留存">活跃留存'




        return render_template('media_reportnew.html',begin_date=begin_date,end_date=end_date,media_name='<option selected="selected">'+media_info+'</option>',mediainfo=mediainfo,live_type=live_type,live_type_info=live_type_info)



@miniprogram.route('/mini_userinfo',methods=['POST','GET'])

def mini_userinfo():
    title = u'小程序用户信息查询'

    if request.method == 'GET':
        return render_template('mini_userinfo.html',title=title)

    else:
        nick_name=request.form.get('nick_name')
        open_id='0'
        mini_info= Mini_userinfo(nick_name,open_id,env_value=False)
        paras=mini_info.userinfo()
        return render_template('mini_userinfo.html',nick_name=nick_name,paras=paras)

@miniprogram.route('/step_detail',methods=['POST','GET'])

def step_detail():
    title=u'小程序用户步数明细'

    if request.method == 'GET':

        open_id=request.args.get('open_id')
        nick_name=request.args.get('nick_name')
        mini_info=Mini_userinfo(nick_name,open_id,env_value=False)
        paras=mini_info.step_detail()

        return render_template('mini_stepdetail.html',paras=paras)


if __name__=='__main__':

    print punchcard()
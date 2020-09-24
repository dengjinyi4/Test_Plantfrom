# encoding=utf-8
__author__ = 'aidinghua'

from flask import request,render_template,Blueprint
from business_modle.querytool.pig_media_cfg import Mypig as mp
mypig = Blueprint('mypig', __name__,template_folder='templates')


@mypig.route('/pig_media_cfg/',methods=['POST','GET'])
def pig_media_cfg():
    title=u'广告主OCPA调价趋势图'
    if request.method == 'GET':

        return render_template('pig_media_config.html',title=title)
    else:
        env_dict={u'测试环境':True,u'线上环境':False}
        env=request.form.get('env').strip()



        tableres,tablefield,tablesql=mp(env_dict[env]).pig_config_table()
        res,field,tmpsql=mp(env_dict[env]).pig_media_conf()

        resnote,fieldnote,tmpsql=mp(env_dict[env]).pig_media_conf_note()
        res_unit,field_unit,tmpsql=mp(env_dict[env]).pigunit_config_table()
        res_unitnote,field_unitnote,tmpsql=mp(env_dict[env]).pigunit_conf_note()
        res_red,field_red,tmpsql=mp(env_dict[env]).pig_red_conf()
        res_rednote,field_rednote,tmpsql=mp(env_dict[env]).pig_red_conf_note()
        res_levelnote,field_levelnote,tmpsql=mp(env_dict[env]).pig_level_conf_note()
        res_level,field_level,tmpsql=mp(env_dict[env]).pig_level_conf()
        res_positionlog,field_positionlog,tmpsql=mp(env_dict[env]).pig_positionlog_conf()
        res_positionlognote,field_positionlognote,tmpsql=mp(env_dict[env]).pig_positionlog_conf_note()
        res_task,field_task,tmpsql=mp(env_dict[env]).pig_task_conf()
        res_tasknote,field_tasknote,tmpsql=mp(env_dict[env]).pig_task_conf_note()
        res_unlock,field_unlock,tmpsql=mp(env_dict[env]).pig_unlock_conf()
        res_unlocknote,field_unlocknote,tmpsql=mp(env_dict[env]).pig_unlock_conf_note()
        res_userlevel,field_userlevel,tmpsql=mp(env_dict[env]).pig_userlevel_conf()
        res_userlevelnote,field_userlevelnote,tmpsql=mp(env_dict[env]).pig_userlevel_conf_note()





    return render_template('pig_media_config.html',tableres=tableres,tablefield=tablefield,
                               tablesql=tablesql,res=res,field=field,env=env,resnote=resnote,fieldnote=fieldnote,
                               res_unit=res_unit,field_unit=field_unit,res_unitnote=res_unitnote,field_unitnote=field_unitnote,
                               res_red=res_red,field_red=field_red,res_rednote=res_rednote,field_rednote=field_rednote,
                               res_level=res_level,field_level=field_level,res_levelnote=res_levelnote,field_levelnote=field_levelnote,
                               res_positionlog=res_positionlog,field_positionlog=field_positionlog,res_positionlognote=res_positionlognote,
                               field_positionlognote=field_positionlognote,res_task=res_task,field_task=field_task,
                               res_tasknote=res_tasknote,field_tasknote=field_tasknote,res_unlock=res_unlock,field_unlock=field_unlock,
                               res_unlocknote=res_unlocknote,field_unlocknote=field_unlocknote,res_userlevel=res_userlevel,
                               field_userlevel=field_userlevel,res_userlevelnote=res_userlevelnote,field_userlevelnote=field_userlevelnote)





if __name__=='__main__':

    # print ocpa_price()
    # print ocpa_order()
    # print ocpa_orderadzone()
    print pig_media_cfg()













#encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import MySQLdb.cursors
class tetplantfrom(object):
    def __init__(self):
        # self.db=MySQLdb.connect(host='221.122.127.183',user='voyager',passwd='voyager',db='test',port=5701,charset='utf8')
        self.db=MySQLdb.connect(host='123.59.17.121',user='voyager',passwd='SIkxiJI5r48JIvPh',db='voyagerlog',port=3306,charset='utf8',cursorclass=MySQLdb.cursors.DictCursor)
        self.db.autocommit(True)
        self.c=self.db.cursor()
    def execsql(self,sql):
        try:
            self.c.execute(sql)
            re=self.c.fetchall()
            return re
        except Exception as e:
            print e.message
    def test(self):
        return 111
def city(sql1):
    tm=tetplantfrom()
    # sql1='''SELECT a.adzone_id ,COUNT(1) as count from voyagerlog.ad_show_log20180601  a
    #         where advertiser_id in (1891,2196,153,2207,2206,2205,2204,1642,2214,1499,1498,2322,1893,1496,1793,2574)
    #         -- and a.adzone_id in (231)
    #         GROUP BY a.adzone_id
    #         -- HAVING COUNT(1)>3000
    #         ORDER BY adzone_id,COUNT(1);'''
    re=tm.execsql(sql1)
    tmplist=[]
    for i in re:
        tmplist.append(i)
    return tmplist
if __name__ == '__main__':
    print 1
    # dict1_fromkeys = dict.fromkeys('q',50)
    # print dict1_fromkeys
    ad_show_log20180601='''SELECT a.adzone_id ,COUNT(1) as count from voyagerlog.ad_show_log20180601  a
            where advertiser_id in (1891,2196,153,2207,2206,2205,2204,1642,2214,1499,1498,2322,1893,1496,1793,2574)
            -- and a.adzone_id in (231)
            GROUP BY a.adzone_id
            -- HAVING COUNT(1)>3000
            ORDER BY adzone_id,COUNT(1);'''
    ad_show_log20180601=city(ad_show_log20180601)
    print ad_show_log20180601
    ad_show_log20180528='''SELECT a.adzone_id ,COUNT(1) as count from voyagerlog.ad_show_log20180528  a
            where advertiser_id in (1891,2196,153,2207,2206,2205,2204,1642,2214,1499,1498,2322,1893,1496,1793,2574)
            -- and a.adzone_id in (231)
            GROUP BY a.adzone_id
            -- HAVING COUNT(1)>3000
            ORDER BY adzone_id,COUNT(1);'''
    ad_show_log20180528=city(ad_show_log20180528)
    print 'ad_show_log20180528'
    print ad_show_log20180528
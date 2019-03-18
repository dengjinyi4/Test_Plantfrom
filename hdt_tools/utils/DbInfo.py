#encoding: utf-8
__author__ = 'Hui Ma'
import ConfigParser
#读取数据库config文件
def ReadDBConfig():
    cp = ConfigParser.ConfigParser()
    cp .read('webconfg.cfg')
    secs = cp.sections()
    #print secs
    #得到所有的section，以列表的形式返回
    section = cp.sections()
    #print(section)

    #得到该section的所有option
    #print(cp.options(section))

    #得到该section的所有键值对
    #print(cp.items(section))

    #得到该section中的option的值，返回为string类型
    #print(cp.get(section, "db"))

    #得到该section中的option的值，返回为int类型
    #print(cp.getint(section, "port"))
    return cp

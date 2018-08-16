# -*- coding: utf-8 -*-
# @Time    : 2018/3/14 16:20
# @Author  : wanglanqing

from utils.db_info import *


class ConfParas(object):
    def __init__(self, env_value):
        self.db = DbOperations(env_value=env_value)
    @classmethod
    def numeric_compare(cls, x, y):
        return x - y

    def query_paras(self):
        q_sql = "select type, `desc`,`value`,value_type from voyager.config_parameters where status='1'"
        conf_re = self.db.execute_sql(q_sql)
        return conf_re

    def manager_paras(self):
        conf_re = self.query_paras()
        conf_all_len = len(conf_re)
        final_re = []
        #取行信息进行处理
        for row_index in range(conf_all_len):
            row = []
            conf_col_len = len(conf_re[row_index])
            #特殊处理type=13这一行的数据，将value转换为a>b>c的样式
            if conf_re[row_index][0] == 13 and len(conf_re[row_index][2]) > 0:
                type13_row = list(conf_re[row_index])
                #取出type=13的value值，将unicode转换为str，通过split转换为list
                value13_list = type13_row[2].encode("utf-8").split(',')
                type13_row.pop(2)
                value_dict = {}
                #将list转换为字典
                for tmp_value in value13_list:
                    value_dict[int(tmp_value.split('/')[1])] = tmp_value.split('/')[0]

                #第一种方法，字典按值倒序排序
                # value13_list = sorted(value_dict.keys(), key=lambda e: e[0], reverse=True)
                value13_list = sorted(value_dict.keys(), cmp=ConfParas.numeric_compare, reverse=True)
                #将value转换为a>b>c的样式
                managed_str = '优先级由高到低依次为：<br>'
                for item in value13_list:
                    managed_str += str(value_dict[item]) + ' > '
                type13_row.insert(2, managed_str[:-2])
                #将该行数据，重新写入row()
                for fitem in type13_row:
                    row.append(fitem)
            #特殊处理type=16这一行的数据，将value值进行分类展示
            elif conf_re[row_index][0] == 16 and len(conf_re[row_index][2]) > 0:
                    type16_row = list(conf_re[row_index])
                    # 取出type=16的value值，将unicode转换为str，通过split转换为list
                    value16_list = type16_row[2].encode("utf-8").split(',')
                    ad_count_set=set()
                    type16_row.pop(2)
                    #使用set(), 进行分类
                    for value16_item in value16_list:
                        ad_count_set.add(value16_item.split('/')[1])
                    #根据分类结果，遍历value值，进行汇总
                    re16 = ''
                    for ad_count_set in ad_count_set:
                        tmp = ''
                        for value16_item in value16_list:
                            print(value16_item)
                            if value16_item.endswith('/' + ad_count_set):
                                # tmp += value16_item[:-2] + ', '
                                tmp += value16_item.split('/')[0] + ', '
                                print(tmp)
                        re16 += '需要展示' + ad_count_set + '个广告的活动为：' + tmp[:-2] + '<br>'
                    type16_row.insert(2, re16)
                    #将该行数据，重新写入row
                    for fitem in type16_row:
                        row.append(fitem)
            elif conf_re[row_index][0] == 18 and len(conf_re[row_index][2]) > 0:
                type18_row = list(conf_re[row_index])
                # 取出type=13的value值，将unicode转换为str，通过split转换为list
                value18_list = type18_row[2].encode("utf-8").split(',')
                type18_row.pop(2)
                value_dict = {}
                # 将list转换为字典
                for tmp_value in value18_list:
                    value_dict[int(tmp_value.split('/')[1])] = tmp_value.split('/')[0]

                # 第一种方法，字典按值倒序排序
                # value13_list = sorted(value_dict.keys(), key=lambda e: e[0], reverse=True)
                value18_list = sorted(value_dict.keys(), cmp=ConfParas.numeric_compare, reverse=True)
                # 将value转换为a>b>c的样式
                managed_str = '优先级由高到低依次为：<br>'
                for item in value18_list:
                    managed_str += str(value_dict[item]) + ' > '
                type18_row.insert(2, managed_str[:-2])
                # 将该行数据，重新写入row()
                for fitem in type18_row:
                    row.append(fitem)
            else:
                for col_index in range(conf_col_len):
                    row.append(conf_re[row_index][col_index])
            final_re.append(row)
        # print(final_re)
        return final_re

    def __del__(self):
        self.db.close_cursor()
        self.db.close_db()

if __name__ == '__main__':
    ConfParas(True).manager_paras()
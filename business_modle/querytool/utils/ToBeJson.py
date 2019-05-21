# -*- coding: utf-8 -*-
# @Time    : 2018/10/1 11:05
# @Author  : wanglanqing


class ToBeJson(object):
    def __init__(self,keys,values):
        self.keys = keys
        self.values = values

    @staticmethod
    def trans(keys,values):
        data = []
        keys_len =len(keys)
        values_len=len(values)
        if keys_len != len(values[0]):
            raise "参数个数不一致"

        for iv in range(values_len):
            tmp_dict = {}
            for i in range(keys_len):
                tmp_dict[keys[i]]=values[iv][i]
            data.append(tmp_dict)
        return data

if __name__=='__main__':
     ToBeJson.trans(['id','name','money'],(('1','sd','22'),('2','gg','33')))


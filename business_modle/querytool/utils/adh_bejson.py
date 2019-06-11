# encoding=utf-8
__author__ = 'aidinghua'

import json

class adh_bejson(object):

    def __init__(self,keys,values):

        self.keys=keys
        self.values=values

    @staticmethod

    def trans(keys,values):

        data=[]
        keys_len = len(keys)
        values_len = len(values)

        if keys_len<>len(values[0]):
            raise "参数个数不一致"

        for v in range(values_len):
            dict={}
            for k in range(keys_len):

                dict[keys[k]]=values[v][k]
            data.append(dict)

        return data



if __name__=='__main__':

    print adh_bejson.trans(['id','name','create_time'],(('4','wx239bfcba6aeb0084','2019-02-15 17:31:04'),('5','wxe65c34b4ec242be','2019-02-16 17:31:04')))






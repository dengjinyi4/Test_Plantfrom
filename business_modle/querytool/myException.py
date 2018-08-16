# -*- coding: utf-8 -*-
# @Time    : 2018/3/6 9:06
# @Author  : wanglanqing

class myException(Exception):
    def __init__(self,method_name, message):
        Exception.__init__(self)
        self.method_name = method_name
        self.message= self.method_name +'  results : ' +  message

class createTemplateTypeException(myException):
    err_str = '创建模板类型失败了'
    def __str__(self):
        return createTemplateTypeException.err_str

class createTemplateException(myException):
    err_str = '创建模板失败了'
    def __str__(self):
        return createTemplateException.err_str
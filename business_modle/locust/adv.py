__author__ = 'emar0901'

def  fun(x):
    return x*2

tmp=[2,3,4,5,6]
print map(fun,tmp)


class person(object):
    def __init__(self,name):
        self.name=name
    def say(self):
        print ('oooook')
class student(person):
    pass
st1=student('tom')
st1.say()
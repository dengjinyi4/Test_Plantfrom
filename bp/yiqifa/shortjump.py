# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from flask import Blueprint, request, render_template
from rediscluster import  RedisCluster

shortJumpRoute = Blueprint('Yiqifa', __name__,template_folder='templates')

@shortJumpRoute.route('shortJump/',methods=['GET','POST'])
def shortJump():
    if request.method=='POST':
         shortValue =  request.form.get('shortValue');
         myenv =  request.form.get('myenv');
         selectRedis =  request.form.get('selectRedis');
         print(selectRedis)
         if myenv == 'test':
            redis_nodes=[
                 {'host':'172.16.17.196','port': 13330},
                 {'host':'172.16.17.196','port': 13331},
                 {'host':'172.16.17.196','port': 13332},
                 {'host':'172.16.17.196','port': 13333},
                 {'host':'172.16.17.196','port': 13334},
                 {'host':'172.16.17.196','port': 13335},
                ]
         elif myenv == 'dev':
            redis_nodes=[
                 {'host':'221.122.127.41','port': 19990},
                 {'host':'221.122.127.41','port': 19991},
                 {'host':'221.122.127.127','port': 19990},
                 {'host':'221.122.127.127','port': 19991},
                 {'host':'221.122.127.128','port': 19990},
                 {'host':'221.122.127.128','port': 19991},
                 {'host':'221.122.127.204','port': 19990},
                 {'host':'221.122.127.204','port': 19991},
                 {'host':'221.122.127.205','port': 19990},
                 {'host':'221.122.127.205','port': 19991},
                ]
         rc =  RedisCluster(startup_nodes=redis_nodes,max_connections=30,decode_responses=True,skip_full_coverage_check=True)
         return render_template('shortJump.html',rcalue = rc.get(shortValue),shortValue=shortValue)
    return render_template('shortJump.html')

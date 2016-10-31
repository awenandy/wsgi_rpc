# -*- coding: utf-8 -*-
from __future__ import division 
import os 
import sys 
import subprocess
import socket
import platform 
import time
import copy
from jsonrpc2 import JsonRpcApplication
from wsgiref.simple_server import make_server  

from db import DataBase  
from scheduler import Scheduler  

data = {}
#
# add data to cache
#
def add_data_to_cache(key,value):
    if not data.has_key(key):
        data[key] = value
    else:
        return  False
    return  True
#
# delete data from cache
#
def delete_data_from_cache(key):
    if data.has_key(key):
        data.pop(key)
    else:
        return  False
    return  True 
#
# update data to cache
#
def update_data_to_cache(key,value):
    if data.has_key(key):
        data[key] = value
    else:
        return  False
    return  True 
#
# query data from cache
# 
def query_data_from_cache(key):
    if data.has_key(key):
        value = data.get(key)
        return  value 
    else:
        return  False
#
# query data from cache
# 
def query_all_data_from_cache():
    return  data 
#
# sync local data to database
#
def sync_database():
    DB = DataBase()
    DB.open()
    for key in data.keys():
        if not DB.getOne('key_table','key',key,'key'):
            DB.insertOne('key_table' ,key,data[key]) 
        elif DB.getOne('key_table','key',key,'key') != data[key]:
            DB.update('key_table' ,key,data[key])
            
    for array in DB.getAll('key_table'):
        if array[1] not in data.keys():
            DB.delete('key_table' ,array[1])
            
    # print DB.getAll('key_table')
    
    DB.close() 
#
# load data from database to local memory
#
def load_database():
    try:
        DB = DataBase()
        DB.open()
     
        for array in DB.getAll('key_table'):
            data[array[1]] = array[0]
        
        DB.close() 
    except Exception,e:
        print e
#
# init the database
#
def init():
    if not os.path.exists('cache.db'):
        open('cache.db','w').write('')
        
if __name__ == '__main__':
    init()
    load_database()
    
    scheduler = Scheduler(2, sync_database)
    scheduler.start()
    
    rpcs = dict()
    rpcs['add_data_to_cache'] = add_data_to_cache
    rpcs['delete_data_from_cache'] = delete_data_from_cache
    rpcs['update_data_to_cache'] = update_data_to_cache
    rpcs['query_data_from_cache'] = query_data_from_cache
    rpcs['query_all_data_from_cache'] = query_all_data_from_cache
    
    app = JsonRpcApplication(rpcs)
     
    httpd=make_server('localhost', 8282, app)
    httpd.serve_forever()



 
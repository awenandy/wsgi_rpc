#!/usr/bin/python
import httplib 
import json
import os
import sys
import pprint
#
# post interface
#
def oc_api(method,params):
    Content = {"jsonrpc":"2.0", "method":method,"id":"test",'params':params} 
    headers = {"Content-type":"application/json;"}

    conn =httplib.HTTPConnection("localhost:8282")
     
    conn.request("POST",'',json.dumps(Content), headers)
    response = conn.getresponse()
    ret = response.read()
    ret = json.loads(ret)

    conn.close()
    
    return ret
#
# add function
#
def add_function():
    if len(sys.argv) != 4:
        print 'add function need key and value params, please check your input'
    else:
        key = sys.argv[2]
        value = sys.argv[3]
        method = 'add_data_to_cache'
        params = {'key':key,'value':value}
        ret = oc_api(method,params)
        if 'result' in ret:
            if ret['result'] == True:
                print 'add key successfully!'
            else:
                print 'add key failed!'
        else:
            print ret['error']['message'] 
#
# delete function
#  
def delete_function():
    if len(sys.argv) != 3:
        print 'delete function only need key params, please check your input'
    else:
        key = sys.argv[2]
        method = 'delete_data_from_cache'
        params = {'key':key }
        ret = oc_api(method,params)
        if 'result' in ret:
            if ret['result'] == True:
                print 'delete key successfully!'
            else:
                print 'delete key failed!'
        else:
            print ret['error']['message']    
#
# update function
#
def update_function():
    if len(sys.argv) != 4:
        print 'update function need key and new value params, please check your input'
    else:
        key = sys.argv[2]
        value = sys.argv[3]
        method = 'update_data_to_cache'
        params = {'key':key,'value':value }
        ret = oc_api(method,params)
        if 'result' in ret:
            if ret['result'] == True:
                print 'update key successfully!'
            else:
                print 'update key failed!'
        else:
            print ret['error']['message']   
#
# query function
#
def query_function():
    if len(sys.argv) != 3:
        print 'query function only need key params, please check your input'
    else:
        key = sys.argv[2]
        method = 'query_data_from_cache'
        params = {'key':key }
        ret = oc_api(method,params)
        if 'result' in ret:
            if ret['result'] ==False :
                print 'no this query key!'
                sys.exit()
            print 'query key successfully!'
            print 'The result is : ',ret['result']
        else:
            print ret['error']['message'] 
#
# query all function
#
def query_all_function():
    if len(sys.argv) != 2:
        print 'query all function not need key params, please check your input'
    else:
        method = 'query_all_data_from_cache'
        params = { }
        ret = oc_api(method,params)
        if 'result' in ret:
            print 'The result is : '
            print ret['result']
        else:
            print ret['error']['message'] 

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'add':
            add_function()
        if sys.argv[1] == 'delete':
            delete_function()
        if sys.argv[1] == 'update':
            update_function()
        if sys.argv[1] == 'query':
            query_function()
        if sys.argv[1] == 'list':
            query_all_function()
    else:
        print 'oc tool need some params in the commad line, please check it!'
 



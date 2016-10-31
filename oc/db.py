# -*- coding: utf-8 -*-

import sqlite3 
import os 
import shutil
import time  
import hashlib  

class DataBase():
    def __init__(self):
        self.conn = None
        self.db = None
        self.cu = None
        self.DataBsePath = 'cache.db'
        
    def createDB(self):
        if not os.path.exists(self.DataBsePath):
            TmpRead = open(self.DataBsePath,'w')
            TmpRead.write('')
            TmpRead.close()
        
    def open(self):
        self.createDB()
        self.db = self.DataBsePath
        self.conn = self.GetConnection()
        self.cu = self.conn.cursor()
        
        table = 'key_table'
        keyDict = {'key':'varchar(30)','value':'varchar(30)'}
        self.createTable(table,keyDict)
 
    def GetConnection(self):
        """ If no connection, create one; otherwise retrun the exists one"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db, check_same_thread = False)
            self.conn.execute("PRAGMA synchronous  = OFF")
            self.conn.execute("PRAGMA temp_store   = MEMORY")
            self.conn.execute("PRAGMA page_size    = 4096")
            self.conn.execute("PRAGMA cache_size   = 16384")
            self.conn.execute("PRAGMA journal_mode = MEMORY")
            self.conn.row_factory = sqlite3.Row
        return self.conn
        
    def createTable(self,table,keyDict):
        key = Attributes =  ','.join( [one+' '+keyDict[one] for one in keyDict])  
        self.cu.execute('create table if not exists %s (%s) '%(table, key))
        
    def dropTable(self,table):
        self.cu.execute("drop table if exists %s  "%table)
        
    def getOne(self,table,primary_key,primary_value,searchkey):
        if type(primary_value) is str:
            self.cu.execute("select %s from %s where %s='%s' "%(searchkey,table,primary_key,str(primary_value)))
        else:
            self.cu.execute('select %s from %s where %s="%s" '%(searchkey,table,primary_key,str(primary_value)))
        ret = self.cu.fetchone()
        if ret:
            return ret[0]
        else:
            return ret
        
    def getMany(self,table,primary_key,primary_value,searchkey):
        if type(primary_value) is str:
            self.cu.execute("select %s from %s where %s='%s' "%(searchkey,table,primary_key,str(primary_value)))
        else:
            self.cu.execute("select %s from %s where %s=%s "%(searchkey,table,primary_key,str(primary_value)))
        return [x[0] for x in self.cu.fetchall()]
        
    def getAll(self,table):
        self.cu.execute("select * from %s"%(table)) 
        self.conn.commit()
        return self.cu.fetchall()
 
    def insertOne(self,table,key,value):
        cmd = ("insert into %s (key,value) values (%s,%s)"%(table ,repr(key),repr(value)))
        cmd = cmd.replace("u'","'")
        self.cu.execute(cmd)
        self.conn.commit()
 
    def update(self,table,key,value):
        if type(value) is str :
            self.cu.execute("update %s set value = '%s' where key='%s' "%(table,value,key))
        else:
            self.cu.execute("update %s set value = '%s' where key='%s' "%(table,value,key))
        self.conn.commit()
        
    def delete(self,table,key):
        self.cu.execute("delete from %s where key = '%s'"%(table,key))
        self.conn.commit()
        
    def close(self):
        self.cu.close()
        self.conn.commit()
        self.conn.close()
 
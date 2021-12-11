#!/usr/bin/python3
from bluepy import btle
from pymongo import MongoClient
import datetime

myDB = ""

def InitMyDB():
    global myDB
    cluster = "mongodb+srv://admin:1234@cluster0.fztpl.mongodb.net/MyData?retryWrites=true&w=majority"
    client = MongoClient(cluster)
    print(client.list_database_names())
    myDB = client.MyData
    print(myDB.list_collection_names())


def UploadDHT11(humi, temp):
    global myDB
    MyDHT11 = myDB["DHT11"]
    record = {
        "Humi": humi,
         "Temp": temp,
        "Date": datetime.datetime.now()
    }
    MyDHT11.insert_one(record)
    print("up to DB completed")


def GetDHT11():
    global myDB
    MyDHT11 = myDB["DHT11"]
    result = MyDHT11.find({"Temp":"23"})
    print(result)
    print(list(result))


def UploadCustomer(count, noMask):
    global myDB
    MyCustomer = myDB["CustomerCount"]
    
    MyCustomer.update_one(
      {"Date":"2021-12-11"},
      {"$set": {"Customer":count}}
    )
        
    MyCustomer.update_one(
      {"Date":"2021-12-11"},
      {"$set": {"NoMaskCustomer":noMask}}
    )
    print("up to DB completed")

def GetCustomer():
    global myDB
    MyCustomer = myDB["CustomerCount"]
    result = MyCustomer.find_one({"Date":"2021-12-11"})
    print(result)
    return result["Customer"]


def GetNoMaskCustomer():
    global myDB
    MyCustomer = myDB["CustomerCount"]
    result = MyCustomer.find_one({"Date":"2021-12-11"})
    print(result)
    return result["NoMaskCustomer"]

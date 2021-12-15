#!/usr/bin/python3
from bluepy import btle
from pymongo import MongoClient
import datetime
import time

myDB = ""

# init the mongoDB database for getting the data
def InitMyDB():
    global myDB
    cluster = "mongodb+srv://admin:1234@cluster0.fztpl.mongodb.net/MyData?retryWrites=true&w=majority"
    client = MongoClient(cluster)
    print(client.list_database_names())
    myDB = client.MyData
    # print the all collection name
    print(myDB.list_collection_names())

# upload the DHT11 data to the mongoDB database
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

# Dont working
def GetDHT11():
    global myDB
    MyDHT11 = myDB["DHT11"]
    result = MyDHT11.find({"Temp":"23"})
    print(result)
    print(list(result))

# upload the customer data to the mongoDB database
def UploadCustomer(count, noMask):
    global myDB
    MyCustomer = myDB["CustomerCount"]
    dateTime = time.strftime('%y-%m-%d')
    date = str(dateTime)

    # upload the customer count
    MyCustomer.update_one(
      {"Date":date},
      {"$set": {"Customer":count}}
    )
    
    # upload the no mask customer count
    MyCustomer.update_one(
      {"Date":date},
      {"$set": {"NoMaskCustomer":noMask}}
    )
    print("up to DB completed")

# get the customer count
def GetCustomer():
    global myDB
    MyCustomer = myDB["CustomerCount"]
    dateTime = time.strftime('%y-%m-%d')
    date = str(dateTime)

    result = MyCustomer.find_one({"Date":date})
    print(result)
    # return the data the main script
    return result["Customer"]

# get the no mask customer count
def GetNoMaskCustomer():
    global myDB
    MyCustomer = myDB["CustomerCount"]
    dateTime = time.strftime('%y-%m-%d')
    date = str(dateTime)

    result = MyCustomer.find_one({"Date":date})
    print(result)
    # return the data the main script
    return result["NoMaskCustomer"]

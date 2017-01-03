#coding: utf-8
import json


def insert_data(data, db):
    # Your code here. Insert the data into a collection 'arachnid'
    db.OPenStreet.insert(data)
    pass


if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient("mongodb://localhost:27017")
    db = client.Projeto_Final_DW

    data = []

    with open('D:\Talita\Pessoal\Udacity\Data_wran\Projeto Final\sao-paulo_brazil_sample.osm.json') as f:

      for line in f:
          insert_data(json.loads(line), db)


    print db.OpenStreet.find_one()



def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


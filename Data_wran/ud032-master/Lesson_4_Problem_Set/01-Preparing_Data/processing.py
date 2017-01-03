#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a dictionary of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
"""
import codecs
import csv
import json
import pprint
import re
import pymongo

from pymongo import MongoClient

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}


def process_file(filename, fields):

    process_fields = fields.keys()
    data = []
    dic = {}
    classif = {}
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            # YOUR CODE HERE
            # YOUR CODE HERE
            label = line["rdf-schema#label"].split(" ")
            dic[fields["URI"]] = check_null(line["URI"])
            dic[fields["rdf-schema#comment"]] = check_null(line["rdf-schema#comment"])

            if line["name"] == 'NULL':
                dic[fields["name"]] = label[0]
            elif re.match('^[\w-]+$', line["name"]) is not None:
                dic[fields["name"]] = label[0]
            else:
                dic[fields["name"]] = line["name"]

            if line["synonym"] == "NULL":
                dic[fields["synonym"]] = None
            else:
                synonym = line["synonym"].replace("{", "")
                synonym = synonym.replace("*", "")
                synonym = synonym.replace("}", "")
                synonym = synonym.split("|")
                dic[fields["synonym"]] = synonym

            classif[fields["family_label"]] = check_null(line["family_label"])
            classif[fields["class_label"]] = check_null(line["class_label"])
            classif[fields["phylum_label"]] = check_null(line["phylum_label"])
            classif[fields["order_label"]] = check_null(line["order_label"])
            classif[fields["kingdom_label"]] = check_null(line["kingdom_label"])
            classif[fields["genus_label"]] = check_null(line["genus"])

            dic["classification"] = classif
            dic[fields["rdf-schema#label"]] = check_null(label[0])
            # print dic
            # .arachnid.insert(dic)
            data.append(dic)

    return data

def check_null(field):

    if field == 'NULL':
        field = None
    else:
        field = field.strip()


    return field

def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    data = process_file(DATAFILE, FIELDS)

    pprint.pprint(data[0])
    """
    assert data[0] == {
                    "synonym": None,
                    "name": "Argiope",
                    "classification": {
                        "kingdom": "Animal",
                        "family": "Orb-weaver spider",
                        "order": "Spider",
                        "phylum": "Arthropod",
                        "genus": None,
                        "class": "Arachnid"
                    },
                    "uri": "http://dbpedia.org/resource/Argiope_(spider)",
                    "label": "Argiope",
                    "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
                }
    """

if __name__ == "__main__":
    test()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")vc tava
"""

osm_file = "D:\users\F65391A\Documents\example3.xml"

def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == "relation":
            users.add(element.attrib['user'])
        if element.tag == "way":
            users.add(element.attrib['user'])
        if element.tag == "node":
            users.add(element.attrib['user'])

    return users


def test():

    users = process_map(osm_file)
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":
    test()
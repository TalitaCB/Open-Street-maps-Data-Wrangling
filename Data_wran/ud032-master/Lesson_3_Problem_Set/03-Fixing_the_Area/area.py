#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the "areaLand" field,
you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it has to return a float
representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you like, but changes to process_file
will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = 'D:/Talita/Pessoal/Udacity/Data_wran/ud032-master/Lesson_3_Problem_Set/03-Fixing_the_Area/cities.csv'


def fix_area(area):

    print area
    # YOUR CODE HERE
    if area == 'NULL':
        area = None
    else:
        if area[:1] == "{":
            tamanho = len(area)
            fim = tamanho - 1
            area_sem_chave = area[1:fim]
            lista = area_sem_chave.split('|')

            num1 = lista[0].split('e')

            num2 = lista[1].split('e')
            if len(num1[0]) - 1 > len(num2[0]) - 1:
                area = float(lista[0])
            else:
               area = float(lista[0])

        else:
            area = float(area)

    print area
    return area



def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        print reader
        #skipping the extra matadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():

    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    assert data[8]["areaLand"] == 55166700.0
    assert data[3]["areaLand"] == None


if __name__ == "__main__":
   test()

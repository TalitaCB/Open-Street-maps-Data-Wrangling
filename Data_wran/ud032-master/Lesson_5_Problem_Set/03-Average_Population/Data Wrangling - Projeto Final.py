#coding: utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import xml.etree.cElementTree as ET # Use cElementTree or lxml if too slow
import pprint
import re
from collections import defaultdict
import codecs
import json

OSM_FILE = 'D:\Talita\Pessoal\Udacity\Data_wran\Projeto Final\sao-paulo_brazil.osm'  # Replace this with your osm file
SAMPLE_FILE = "D:\Talita\Pessoal\Udacity\Data_wran\Projeto Final\sao-paulo_brazil_sample.osm"

k = 2 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    print "entrou no get_element"
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def cria_sample(SAMPLE_FILE,OSM_FILE,k):

    with open(SAMPLE_FILE, 'wb') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')
        # Write every kth top level element
        for i, element in enumerate(get_element(OSM_FILE)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))
        output.write('</osm>')
        print "arquivo salvo"
    pass


def count_tags(filename):
    tags = {}
    i = 1
    # YOUR CODE HERE
    for event, elem in ET.iterparse(filename):
        if tags.has_key(elem.tag):
            i = tags[elem.tag]
            i = i + 1
            tags[elem.tag] = i
        else:
            tags[elem.tag] = 1

    return tags

#cria arquivo de amostras
#cria_sample(SAMPLE_FILE,OSM_FILE,k)

#contando quantidade de tags distintas
#tags = count_tags(SAMPLE_FILE)
#pprint.pprint(tags)

#procurando para ver se existem tagas com problemas de caracteres



#limpando nomes de ruas
street_type_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)

expected = ["Rua", "Avenida", "Alameda", "Acostamento", "Largo", "Viela", "Viaduto", "Via", "Estrada",
            "Rodovia", "Parque", "Travessa", "Praça", "Ladeira", "Marginal", "Passagem","Corredor", "Acesso", "Rodoanel"]

# UPDATE THIS VARIABLE
mapping = {"Acost": "Acostamento",
           "Al.": "Alameda",
           "Av.": "Avenida",
           "R.": "Rua",
           "Acost.": "Acostamento",
           "Alfonso": "Av. Prof. Alfonso",
           "Bueno": "Rua Bueno",
           "Coronel": "Rua Coronel",
           "Doutor": "Rua Doutor",
           "Dr.": "Rua Doutor Jesuino",
           "Manoel": "Rua Manoel",
           "O": "Rua",
           "Pateo": "Largo Pateo",
           "Pires": "Rua Pires",
           "antonio": "Rua",
           "armando": "Rua Armando",
           "Pra": "Praça",
           "Hermínio": "Rua Herminio",
           "Marquês": "Rua Marques",
           "Pça": "Praça",
           "Pça.": "Praça",
           "Av": "Avenida",
           "rua": "Rua",
           "R": "Rua",
           'RUA': "Rua",
           'RUa': "Rua",
           "r.": "Rua",
           "av.": "Avenida",
           "estrada": "Estrada",
           "avenida": "Avenida",
           "Rue": "Rua",
           "viela": "Viela",
           "praça": "Praça",
            "Av.Dn.Ana": "Avenida Dn Ana",
            "Azevedo": "Rua Azevedo",
            "Av.Antônio": 'Avenida Antonio',
            "Guarara": 'Rua Guarara',
            "Cantídio": 'Rua Cantidio',
            "sao": "Rua são",
            "antonio": "Rua antonio",
            "Oscar": "Rua Oscar",
            "Av.Francisco": "Avenida Francisco",
            "Garcia": "Rua Garcia",
            "Manoel": "Rua Manoel",
            "Marina": "Rua Marina",
            "Antonio": "Rua Antonio",
            "AvJacú": "Avenida Jacu",
            "Cajaíba":"Rua Cajaiba",
            "Marina": "Rua Marina",
            "R.Antônio": "Rua Antonio",
            "Av.das": "Avenida das",
            "CoronelMelo": "Rua Coronel Melo",
            "Alfonso": "Rua Alfosno",
            "Av.Agenor": "Avenida Agenor",
            "Tavares": "Rua Tavares",
            "Av.Presidente": "Avenida Presidente",
            "Nívia": "Rua Nivia",
            "José": "Rua José",
            "JOSÉ": "Rua José",
            "Ignacio": "Rua Ignacio",
            "Oito": "Rua Oito",
            "presidente": "Rua Presidente",
            "Escapatória": "Rua Escapatória",
            "Vale": "Rua Vale",
            "guainambe": "Rua Guainambe",
            "Ida": "Rua Ida",
            "Parati": "Rua Parati",
            "Quatro": "Rua Quatro",
            "Angelo": "Rua Angelo",
            "Paulo": "Rua Paulo",
            "Dr.": "Rua Doutor",
            "Conselheiro": "Rua Conselheiro",
            "Bueno": "Rua Bueno",
            "Pires": "Rua Pires",
            "Castro": "Rua Castro",
            "Maria": "Rua Maria",
            "Rocha": "Rua Rocha",
            "Conselheiro": "Rua Conselheiro",
            "Luiz": "Rua Luiz",
            "Barroco": "Rua Barroco",
            "armando": "Rua Armando",
            "Tupinambás": "Rua Tupinambás",
            "Fernando": "Rua Fernando"
            }

#converte dicinário para utf-8
mapping = {k: unicode(v).encode("utf8") for k,v in mapping.iteritems()}


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    m = street_type_re.search(name)
    street_type = m.group()
    street_type = unicode(street_type).encode("utf8")
    name = name.replace(street_type, mapping[street_type])

    return name


CREATED = ["version", "changeset", "timestamp", "user", "uid"]
cep_re = re.compile('d{5}-d{3}')


def verifica_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    resp = False
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            resp = True
        else:
            resp = False

    return resp

def retorna_street_type(street_types, street_name):

    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type in expected:
            return unicode(street_type).encode("utf8")
        else:
            pass


#formata arquivo json
def shape_element(element):
    node = {}

    if element.tag == "node" or element.tag == "way":
        pos = []
        node_refs = []
        # YOUR CODE HERE
        # print element.attrib
        node["id"] = element.attrib["id"]
        node["type"] = element.tag

        try:

            node["visible"] = element.attrib["visible"]
        except:

            pass


        node['created'] = {"version": element.attrib['version'],
                           'changeset': element.attrib['changeset'],
                           'timestamp': element.attrib['timestamp'],
                           'user': element.attrib['user'],
                           'uid': element.attrib['uid']}
        try:
            pos.append(float(element.attrib["lat"]))
            pos.append(float(element.attrib["lon"]))
            node["pos"] = pos
        except:
            pass
        endereco = {}
        street_types = defaultdict(set)
        for tag in element.iter("tag"):
            # print tag.attrib

            if tag.attrib['k'][0:4] == "addr":

                if is_street_name(tag):
                    #print tag.attrib['v']
                    if verifica_street_type(street_types, tag.attrib['v']):
                        try:
                            endereco[tag.attrib['k'][5:]] = update_name(tag.attrib['v'], mapping)
                            endereco['streettype'] = retorna_street_type(street_types, update_name(tag.attrib['v'], mapping))


                        except:
                            print tag.attrib['v']
                            endereco[tag.attrib['k'][5:]] = tag.attrib['v']

                    else:
                        endereco[tag.attrib['k'][5:]] = tag.attrib['v']
                        endereco['streettype'] = retorna_street_type(street_types, tag.attrib['v'])


                    node["address"] = endereco
                #print tag.attrib
                elif tag.attrib['k'].count(":") == 1:
                    # elif ":" in tag.attrib['k']:
                    # node["address"]['building'] = tag.attrib['v']
                    if tag.attrib['k'][5:] == 'postcode':

                        if len(tag.attrib['v']) == 8:
                            cep_d = tag.attrib['v'][:5]
                            cep_e = tag.attrib['v'][5:]
                            cep = cep_d + '-' + cep_e
                            endereco[tag.attrib['k'][5:]] = cep
                            node["address"] = endereco
                        elif len(tag.attrib['v']) != 9 and '.' in tag.attrib['v'] and '-' in tag.attrib['v']:
                             cep = tag.attrib['v'].replace('.','')
                             endereco[tag.attrib['k'][5:]] = cep
                             node["address"] = endereco
                        elif len(tag.attrib['v']) == 9 and '-' not in tag.attrib['v']:
                            if '.' in tag.attrib['v'] and tag.attrib['v'].index('.') == 5:
                                cep = tag.attrib['v'].replace('.','-')
                                endereco[tag.attrib['k'][5:]] = cep
                                node["address"] = endereco
                        else:
                            endereco[tag.attrib['k'][5:]] = tag.attrib['v']
                            node["address"] = endereco

                    else:
                        endereco[tag.attrib['k'][5:]] = tag.attrib['v']
                        node["address"] = endereco

            elif tag.attrib['k'] == 'amenity':
                node["amenity"] = tag.attrib['v']
            elif tag.attrib['k'] == 'cuisine':
                node["cuisine"] = tag.attrib['v']
            elif tag.attrib['k'] == 'name':
                node["name"] = tag.attrib['v']
            elif tag.attrib['k'] == 'phone':
                node["phone"] = tag.attrib['v']
            elif tag.attrib['k'] == 'emergency':
                node["emergency"] = tag.attrib['v']
            elif tag.attrib['k'] == 'shop':
                node["shop"] = tag.attrib['v']

        #print endereco["postcode"]
        # print element.attrib["id"]

        #print node["address"]
        if element.tag == "way":
            for nd in element.iter("nd"):
                node_refs.append(nd.attrib["ref"])
                node["node_refs"] = node_refs

        #print node
        return node
    else:
        return None

#processa arquivo Json

def process_map_json(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    print "Inicia leitura do arquivo"
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):

            el = shape_element(element)

            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")

            """""
            for ancestor in element.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
            """""
    return data




data = process_map_json(SAMPLE_FILE, False)





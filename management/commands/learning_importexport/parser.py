import xml.etree.ElementTree as ET
from xml.dom import minidom

def func3():
    root = ET.parse('ap.xml').getroot()
    print(root)



def func2():
    xmldoc = minidom.parse('ap2.xml')

    itemlist = xmldoc.getElementsByTagName('item')
    print(len(itemlist))
    print(itemlist[0].attributes['name'].value)
    for s in itemlist:
        print(s.attributes['name'].value)



def func1():
    tree = ET.parse('ap.xml')
    root = tree.getroot()
    print(root)
    print(root.tag)



def func4():
    import xml.etree.ElementTree as ET
    import xmltodict
    import json

    tree = ET.parse('ap.xml')
    xml_data = tree.getroot()

    xmlstr = ET.tostring(xml_data, encoding='utf8', method='xml')


    data_dict = dict(xmltodict.parse(xmlstr))

    print(data_dict['data']['country'])

    # with open('new_data_2.json', 'w+') as json_file:
    #     json.dump(data_dict, json_file, indent=4, sort_keys=True)


def func5():
    xmldoc = minidom.parse('xml3.xml')
    readbitlist = xmldoc.getElementsByTagName('readbit')
    values = []
    for s in readbitlist :
        x = s.attributes['bit'].value
        values.append(x)
    print(values)


def func6():
    import xmltodict, json
    # o = xmltodict.parse('<e> <a>text</a> <a>text</a> </e>')
    # with open('xml3.xml', 'r') as f:
    #     o = xmltodict.parse(f.read())
    o = xmltodict.parse(open('xml3.xml', 'r').read())
    x = json.dumps(o)
    x = json.loads(x) 
    # x = eval(x)

    d = x['data']['results'][0]
    # d = json.dumps(d, indent=4)
    print(d)



func6()

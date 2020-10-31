import xmltodict
import pprint
import json

my_xml = """
    <audience>
      <id what="attribute">123</id>
      <name>Shubham</name>
    </audience>
"""

pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(json.dumps(xmltodict.parse(my_xml)))


print(json.dumps(xmltodict.parse(my_xml)))


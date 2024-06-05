import xml.etree.ElementTree as etree
import json

class JSONConnector:
    """
    the class parses the JSON file and has a parsed data
    method that returns all data as a dictionary
    """
    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r', encoding='utf-8') as f:
            self.data = json.load(f)

    # the property decorator is used to make parsed_data()
    # appear as normal variable

    @property
    def parsed_data(self):
        return self.data   

    # XMLConnector class parses the XML file and has a parsed_data()
    # method that returns all data as a list of xml.etree.Element

class XMLConnector:
        def __init__(self, filepath):
            self.tree = etree.parse(filepath)

        @property
        def parsed_data(self):
            return self.tree

# the connection_factory() is a Factory Method
# it returns an instance of JSONConnector or XMLConnector
# depending on the extension of the input file path

def connection_factory(filepath):
    if filepath.endswith('json'):
        connector = JSONConnector
    elif filepath.endswith('xml'):
        connector = XMLConnector
    else:
        raise ValueError(f'Cannot connect to {filepath}')
    return connector(filepath)

# the connect_to() function is a wrapper of
# connection_factory(). It adds exception handling 
def connect_to(filepath):
    factory = None
    try:
        factory = connection_factory(filepath)
    except ValueError as ve:
        print(ve)
    return factory

def main():
    sqlite_factory = connect_to('/person.sq3')

    # working with XML files using the Factory Method
    xml_factory = connect_to('person.xml')
    xml_data = xml_factory.parsed_data
    liars = xml_data.findall("./{}[{}='{}']".format('person', 'lastName','Liar'))
    print('found: {} persons'.format(len(liars)))
    for liar in liars:
        print('first name:{}'.format(liar.find('firstName').text))
        print('last name: {}'.format(liar.find('lastName').text))
        [print('phone number ({}):'.format(p.attrib['type']), p.text) 
            for p in liar.find('phoneNumbers')]


    # working with JSON files using Factory Method
    json_factory = connect_to('donut.json')
    json_data = json_factory.parsed_data
    print('found: {} donuts'.format(len(json_data)))
    for donut in json_data:
        print('name: {}'.format(donut['name']))
        print('price: ${}'.format(donut['ppu']))
        [print('topping: {} {}'.format(t['id'], t['type'])) for t in donut['topping']]

if __name__ == '__main__':
    main()


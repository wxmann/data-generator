import xml.etree.ElementTree as ET
from core import config
from generators import dictionary

__author__ = 'tangz'

def parsexml(xmlfile):
    parser = XMLParser(xmlfile)
    return parser.parse_config()

class XMLParser:

    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        self.root = self._getxmlroot()

    def _getxmlroot(self):
        domtree = ET.parse(self.xmlfile)
        return domtree.getroot()

    def parse_config(self):
        columnnodes = self.root.findall('column')
        tabularconfig = config.TabularConfig()
        for columnnode in columnnodes:
            # parse column information
            columnname = columnnode.get('name')
            for child in columnnode:
                # parse function id
                func_id = child.tag
                func = dictionary.lookup(func_id)

                args = []
                kwargs = {}
                argnodes = child.findall('arg')

                for argnode in argnodes:
                    keyattr = argnode.get('key')
                    typeattr = argnode.get('type')

                    # handle list or single
                    if typeattr == 'list':
                        argtoadd = [item.text for item in argnode.findall('item')]
                    else:
                        argtoadd = argnode.text

                    # handle kwarg
                    if keyattr is None:
                        args.append(argtoadd)
                    else:
                        kwargs[keyattr] = argtoadd

                tabularconfig.set_funcsetting(columnname, func, *args, **kwargs)
        return tabularconfig
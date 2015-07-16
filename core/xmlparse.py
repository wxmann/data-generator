import xml.etree.ElementTree as ET
from core import config
from generators import dictionary

__author__ = 'tangz'

def parsexml(xmlfile):
    parser = XMLParser(xmlfile)
    return parser.parse_config()


class XMLFormatError(Exception):
    pass


class XMLParser:

    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        self.root = self._getxmlroot()

    def _getxmlroot(self):
        domtree = ET.parse(self.xmlfile)
        return domtree.getroot()

    def _getargwithtype(self, arg, datatype):
        return {
            'int': int,
            'float': float
            # 'date': arg  TODO: make this work
        }.get(datatype, lambda x: x)(arg)

    def parse_config(self):
        columnnodes = self.root.findall('column')
        tabularconfig = config.TabularConfig()
        for columnnode in columnnodes:
            # parse column information
            columnname = columnnode.get('name')
            funcnodes = columnnode.findall('function')
            if len(funcnodes) != 1:
                raise XMLFormatError('Excepted only one function element for column: {0}'.format(columnname))
            # parse function id
            funcnode = funcnodes[0]
            func_id = funcnode.get('id')
            func = dictionary.lookup(func_id)

            args = []
            kwargs = {}
            argnodes = funcnode.findall('arg')

            for argnode in argnodes:
                keyattr = argnode.get('key')
                typeattr = argnode.get('type')

                # handle list or single
                if typeattr == 'list':
                    argtoadd = [self._getargwithtype(item.text, typeattr) for item in argnode.findall('item')]
                else:
                    argtoadd = self._getargwithtype(argnode.text, typeattr)

                # handle kwarg
                if keyattr is None:
                    args.append(argtoadd)
                else:
                    kwargs[keyattr] = argtoadd

            tabularconfig.set_funcsetting(columnname, func, *args, **kwargs)
        return tabularconfig
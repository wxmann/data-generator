import unittest
from parse import xmlparse
import writer

__author__ = 'tangz'


class XMLParseTest(unittest.TestCase):

    def test_create_file(self):
        file_in = "../resources/Sample.xml"
        file_out = "../resources/Hope.csv"
        # config = xmlparse.parsexml(file)
        writer.write_csv_from_xml_config(file_out, file_in, 10)

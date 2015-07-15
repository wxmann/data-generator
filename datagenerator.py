from core import xmlparse, output

__author__ = 'tangz'

def main():
    xmlfile = "Sample.xml"
    config = xmlparse.parsexml(xmlfile)
    output.to_csv("Test1.csv", config, n=500)

if __name__ == "__main__":
    main()
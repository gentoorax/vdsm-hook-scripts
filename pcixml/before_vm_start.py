#!/usr/libexec/platform-python

import os
import sys
import argparse
import traceback
from xml.etree import ElementTree as ET
from xml.dom import minidom

devices_tag = 'devices'

def pcixml(domxml,pcixmlfilename):
    devices = domxml.find(devices_tag)
    if len(devices) > 0:
        sys.stderr.write('pcixml: found devices section')
        xmltoadd = getxmlblock(pcixmlfilename)
        attachblock(xmltoadd, devices)
    else:
        sys.stderr.write('pcixml: missing devices block aborted')
    return domxml

def getxmlblock(pcixmlfilename):
    xmltoadd = ET.parse(pcixmlfilename)
    return xmltoadd

def attachblock(xmltoadd,devices):
    root = xmltoadd.getroot()
    for child in root:
        devices.append(child)

def testfile():
    domxml = minidom.parse('./test.xml') #simulate hook read
    etxml = convertdomtoet(domxml)
    pcixmlfilename = "./xmltoadd.xml" #test block location
    etxml = pcixml(etxml,pcixmlfilename)
    domxml = convertettodom(etxml)
    print(domxml.toprettyxml())

def convertdomtoet(domxml):
    return ET.fromstring(domxml.toxml())

def convertettodom(etxml):
    etstr = ET.tostring(etxml)
    return minidom.parseString(etstr)

def hook():
    import hooking
    if os.environ.__contains__('pcixmlfile'):
        try:
            pcixmlfilename = os.environ['pcixmlfile']
            domxml = hooking.read_domxml()
            etxml = convertdomtoet(domxml)
            etxml = pcixml(etxml,pcixmlfilename)
            domxml = convertettodom(etxml)
            hooking.write_domxml(domxml)
        except:
            sys.stderr.write('pcixml: [unexpected error]: %s\n' % traceback.format_exc())
            sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description='VDSM Hook for attaching pci devices to the vm')
    parser.add_argument('--debug', action='store_true',
        help='Run this in debug mode for testing xml file and printing output')
    args = parser.parse_args()
    if args.debug:
        testfile()
    else:
        hook()

if __name__ == '__main__':
    main()
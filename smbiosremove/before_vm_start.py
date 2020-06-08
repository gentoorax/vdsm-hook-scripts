#!/usr/bin/python
import os
import sys
import argparse
import traceback

smbios_tag = 'smbios'

def smbiosremove(domxml):
    nodes = domxml.getElementsByTagName(smbios_tag)
    if len(nodes) > 0:
        for node in nodes:
            parent = node.parentNode
            parent.removeChild(node) 

    return domxml

def testfile():
    from xml.dom.minidom import parse
    domxml = parse('test.xml')
    domxml = smbiosremove(domxml)
    print(domxml.toprettyxml())

def hook():
    import hooking
    if hooking.tobool(os.environ.get('smbiosremove')):
        try:
            domxml = hooking.read_domxml()
            domxml = smbiosremove(domxml)
            hooking.write_domxml(domxml)
        except:
            sys.stderr.write('smbiosremove: [unexpected error]: %s\n' % traceback.format_exc())
            sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description='VDSM Hook for remove smbios from os section of the vm')
    parser.add_argument('--debug', action='store_true',
        help='Run this in debug mode for testing xml file and printing output')
    args = parser.parse_args()
    if args.debug:
        testfile()
    else:
        hook()

if __name__ == '__main__':
    main()
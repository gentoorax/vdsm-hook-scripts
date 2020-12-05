#!/usr/libexec/platform-python
import os
import sys
import argparse
import traceback

clock_tag = 'clock'

def clockoffset(domxml, clockoffsetmanual):
    clock = domxml.getElementsByTagName(clock_tag)
    if len(clock) > 0:
        set_clock_offset(clock[0], clockoffsetmanual)

    return domxml

def set_clock_offset(element, clockoffsetmanual):
    if element:
        if element.hasAttribute('offset'):
            element.setAttribute('offset', clockoffsetmanual)
        if element.hasAttribute('basis') > 0:
            element.removeAttribute('basis')
        if element.hasAttribute('adjustment') > 0:
            element.removeAttribute('adjustment')

def testfile():
    from xml.dom.minidom import parse
    clockoffsetmanual = 'localtime'
    domxml = parse('test.xml')
    domxml = clockoffset(domxml,clockoffsetmanual)
    print(domxml.toprettyxml())

def hook():
    import hooking
    if os.environ.__contains__('clockoffset'):
        try:
            clockoffsetmanual = os.environ.get('clockoffset')
            domxml = hooking.read_domxml()
            domxml = clockoffset(domxml,clockoffsetmanual)
            hooking.write_domxml(domxml)
        except:
            sys.stderr.write('clockoffset: [unexpected error]: %s\n' % traceback.format_exc())
            sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description='VDSM Hook for setting clock offset for the vm')
    parser.add_argument('--debug', action='store_true',
        help='Run this in debug mode for testing xml file and printing output')
    args = parser.parse_args()
    if args.debug:
        testfile()
    else:
        hook()

if __name__ == '__main__':
    main()
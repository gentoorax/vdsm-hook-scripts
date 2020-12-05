#!/usr/libexec/platform-python
import os
import sys
import argparse
import traceback

cpu_tag = 'cpu'

def cpuhostmodelcheckpartial(domxml):
    cpu = domxml.getElementsByTagName(cpu_tag)
    if len(cpu) > 0:
        set_cpu_model(cpu[0])

    return domxml

def set_cpu_model(element):
    if element:
        if element.hasAttribute('mode'):
            element.setAttribute('mode', 'host-model')
        if element.hasAttribute('check'):
            element.setAttribute('check', 'partial')
        if element.hasAttribute('match'):
            element.removeAttribute('match')

def testfile():
    from xml.dom.minidom import parse
    domxml = parse('test.xml')
    domxml = cpuhostmodelcheckpartial(domxml)
    print(domxml.toprettyxml())

def hook():
    import hooking
    if hooking.tobool(os.environ.get('cpuhostmodelcheckpartial')):
        try:
            domxml = hooking.read_domxml()
            domxml = cpuhostmodelcheckpartial(domxml)
            hooking.write_domxml(domxml)
        except:
            sys.stderr.write('cpuhostmodelcheckpartial: [unexpected error]: %s\n' % traceback.format_exc())
            sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description='VDSM Hook for setting cpu model to host-model and check to partial for the vm')
    parser.add_argument('--debug', action='store_true',
        help='Run this in debug mode for testing xml file and printing output')
    args = parser.parse_args()
    if args.debug:
        testfile()
    else:
        hook()

if __name__ == '__main__':
    main()
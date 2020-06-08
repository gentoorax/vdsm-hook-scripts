#!/usr/bin/python
import os
import sys
import argparse
import traceback

features_tag = 'features'
apic_tag = 'apic'

def apic_feature(domxml):
    features = domxml.getElementsByTagName(features_tag)
    if len(features) > 0:
        apic = features[0].getElementsByTagName(apic_tag)
        if len(apic) > 0:
            sys.stderr.write('apic-feature: apic tag already exists')
        else:
            sys.stderr.write('apic-feature: apic tag does not exist creating')
            create_append(features[0],domxml,[apic_tag],[])
    else:
        sys.stderr.write('apic-feature: features do not exist creating')
        create_append(domxml.firstChild,domxml,[apic_tag,features_tag],[create_append])

    return domxml

def create_append(element,domxml,tags,funcs):
    new_element = domxml.createElement(tags.pop())
    if funcs:
        funcs.pop()(new_element,domxml,tags,funcs)
    return element.appendChild(new_element)

def testfile():
    from xml.dom.minidom import parse
    domxml = parse('test.xml')
    domxml = apic_feature(domxml)
    print(domxml.toprettyxml())

def hook():
    import hooking
    if hooking.tobool(os.environ.get('apicfeature')):
        try:
            domxml = hooking.read_domxml()
            domxml = apic_feature(domxml)
            hooking.write_domxml(domxml)
        except:
            sys.stderr.write('apic-feature: [unexpected error]: %s\n' % traceback.format_exc())
            sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description='VDSM Hook for adding apic feature tag to the vm')
    parser.add_argument('--debug', action='store_true',
        help='Run this in debug mode for testing xml file and printing output')
    args = parser.parse_args()
    if args.debug:
        testfile()
    else:
        hook()

if __name__ == '__main__':
    main()
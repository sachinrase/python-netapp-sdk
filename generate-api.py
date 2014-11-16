#!/usr/bin/env python

import xmltodict
import time

api_file = 'system-api-list'

fd = open(api_file, 'r')
api_xml = fd.read()
fd.close()

hash = xmltodict.parse(api_xml)

api_list = hash.get('results').get('apis').get('system-api-info')

ws_size = ' '*4

header = '''############################################################################
# This module was auto-generated on %s
# by using the 'system-api-list' api call from NetApp SDK for python.  
# If you make changes to this module it will likely be broken the next time
# this file is auto-generated.  If you choose to update this file anyway,
# please ensure that you have also updated the generate-api.py script
# to include your new changes.
#
# Also worth mentioning that some of the api calls may not work properly
# and that is because there is no way to easily auto-determine what api
# calls require additional arguments.  If you find one that is broken,
# you may need to manually update this file but that is not recommended.
#
# The goal of this module is to make it easier to develop code since the
# original API requires you to know the exact API calls for interating
# with your NetApp appliance.  The other goal of this module is to ensure
# you can override it instaed of modifying it directly if you find problems.
############################################################################
''' %(time.ctime())
print(header)
print('')
print('import sys')
print('from NaElement import *')
print('from NaServer import *')
print('')

print('conn = None')
print('')
print('def connect(hostname, user, password, minor_version=1, major_version=21):')
print('%sglobal conn' %(ws_size))
print('%sconn = NaServer(hostname, minor_version, major_version)' %(ws_size))
print("%sconn.set_server_type('filer')" %(ws_size))
print("%sconn.set_transport_type('HTTPS')" %(ws_size))
print("%sconn.set_port(443)" %(ws_size))
print("%sconn.set_style('LOGIN')" %(ws_size))
print("%sconn.set_admin_user(user, password)" %(ws_size))
print("%sreturn conn" %(ws_size))
print('')

for api in api_list:
    api_call = api.get('name')
    api_function = api_call.replace('-','_')

    print('def %s():' %(api_function))
    print("%sapi_call = _invoke_api('%s')" %(ws_size, api_call))
    print('%sreturn api_call' %(ws_size))
    print('')

print('def _invoke_api(*args):')
print('%sapi = NaElement(*args)' %(ws_size))
print('%scall = conn.invoke_elem(api)' %(ws_size))
print('%sif call.results_errno() != 0:' %(ws_size))
print("%s%sraise IOError('Failed api call=%%s, errno=%%s, desc=%%s'" %(ws_size, ws_size))
print("%s%s%s%%(args, call.results_errno(), call.sprintf())" %(ws_size, ws_size, ws_size))
print("%s%s)" %(ws_size, ws_size))
print("%sreturn call" %(ws_size))

#!/usr/bin/env python

# SOURCE: https://github.com/zaproxy/zaproxy/wiki/ApiPython

import time
from pprint import pprint
from zapv2 import ZAPv2

target = 'http://0.0.0.1:8080'
apikey = 'eudq0kus3m0frtjm0plv9krbao' # Change to match the API key set in ZAP, or use None if the API key is disabled
# By default ZAP API client will connect to port 8080
# zap = ZAPv2(apikey=apikey)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
zap = ZAPv2(apikey=apikey, proxies={'http': '127.0.0.1:7576', 'https': '127.0.0.1:7576'})


print zap.pscan.scanners
print zap.ascan.scans
print zap.ascan.policies()


# do stuff
print 'Accessing target %s' % target
# try have a unique enough session...
zap.urlopen(target)
# Give the sites tree a chance to get updated
time.sleep(2)

zap.ascan.disable_all_scanners()
zap.ascan.remove_all_scans()
zap.ascan.enable_scanners(ids='40018')
zap.ascan.enable_scanners(ids='40012')

print 'policies'
for policy in  zap.ascan.policies():
    print policy

print 'scanners'
for scanner in zap.ascan.scanners():
    print scanner["name"]


print 'pscanners---'
for scanner in zap.pscan.scanners:
    print scanner["name"]

print "---"

print 'scans'
for scan in  zap.ascan.scans:
    print scan
print '---'

print 'spider'
for scan in zap.spider.scans:
    print scan
print '---'

print 'Spidering target %s' % target
scanid = zap.spider.scan(target)
# Give the Spider a chance to start
time.sleep(2)
while (int(zap.spider.status(scanid)) < 100):
    print 'Spider progress %: ' + zap.spider.status(scanid)
time.sleep(2)

print 'Spider completed'
# Give the passive scanner a chance to finish
# time.sleep(5)

pprint (zap.core.alerts())

"""
print 'Scanning target %s' % target
scanid = zap.ascan.scan(target)
while (int(zap.ascan.status(scanid)) < 100):
    print 'Scan progress %: ' + zap.ascan.status(scanid)
    time.sleep(5)

print 'Scan completed'

# Report the results

print 'type'
print type(zap.core.alerts())

print 'Hosts: ' + ', '.join(zap.core.hosts)
print 'Alerts: '

#pprint (zap.core.alerts())

print '---------------------------------------'

sql = False
xss = False

for alert in zap.core.alerts():
    if alert["pluginId"] == '40018':
        sql = True
        #print '---sql---'
        #print 'the website might be vulnerable:'
        #print alert['description']

        #print alert
    elif alert["pluginId"] == '40012':
        xss = True
        #print '---xss---'
        #print 'the website might be vulnerable:'
        #print alert['alert']
        #print alert

print 'Vulnerabilities:'
if sql == True:
    print 'SQL Injection'

if xss == True:
    print 'Cross Site Scripting'



print '1'
pprint (zap.core.alerts(1))

print '2'
pprint (zap.core.alerts(riskid=2))

print '79'
pprint (zap.core.alerts(riskid=79))

print 'sql'
pprint (zap.core.alert(pluginId=40018))
print 'xss reflected'
pprint (zap.core.alert(40012))
print '2'
pprint (zap.core.alert(2))
print '4'
pprint (zap.core.alert(4))
"""

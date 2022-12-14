'''
# SPDX-License-Identifier: LGPL-3.0-or-later
# MST - Mikhail Soloviev Tests
# Copyright 2022 <mikhail.soloviov@mail.ru>
# Network access functions used in MST
'''
from mstSettingsAndHelpers import *
from mstScapier import *

def mstOsiL2_BroadcastDiscovery():
    ''' OSI Level 2 operation: Broadcast Ethernet network; returns list of responded [IP, MAC] '''
    mstPrint(3, 'mstOsiL2_BroadcastDiscovery start ------')
    ret = []
    ipRange = mstDefaultIP + '/' + str(mstDefaultIPMask) # e.g. '192.168.1.4/30'
    discoveredIPsMacs = mstDiscoverIps(ipRange)
    if not discoveredIPsMacs:
        mstPrint(2, 'mstOsiL2_BroadcastDiscovery: Nothing discovered')
    else:
        discoveredIPsMacs.sort()
        ret = discoveredIPsMacs
        mstPrint(2, 'mstOsiL2BroadcastDiscovery result:', discoveredIPsMacs)
    mstPrint(3, 'mstOsiL2_BroadcastDiscovery end ------')
    return ret

def mstOsiL3_PingIp(host, text=''):
    ''' OSI Level 3 operation: Scan given port(s) on the host; returns list of responded [IP, port] '''
    executor = mstOsiL3_PingIp.__name__
    ret = None
    if not host:
        mstPrint(1, f'{executor} ERROR: No host provided')
    else:
        mstPrint(2, f'{executor} pinging: {host}')
        ret = mstIcmpPing(host, text)
        if ret:
            mstPrint(3, f'{executor} result: {host} returned {ret}')
    return ret

def mstOsiL4_ScanPorts(host, portRange):
    ''' OSI Level 4 operation: Scan given port(s) on the host; returns list of responded [IP, port] '''
    mstPrint(3, f'{mstOsiL4_ScanPorts.__name__} start ------')
    ret = []
    if not host or not portRange:
        mstPrint(1, f'{mstOsiL4_ScanPorts.__name__} ERROR: No parameter(s) provided')
    else:
        results = mstCheckIpPorts(host, portRange)
        if results:
            ret = results
            mstPrint(3, 'detected:', results)
    mstPrint(3, f'{mstOsiL4_ScanPorts.__name__} end ------')
    return ret

# Call examples; keep commented out:
#mstOsiL2_BroadcastDiscovery()
#mstOsiL4_ScanPorts('192.168.1.1', (80, 80))
#mstOsiL3_PingIp('192.168.1.1')
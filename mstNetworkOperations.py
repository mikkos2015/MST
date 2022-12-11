"""
# SPDX-License-Identifier: LGPL-3.0-or-later
# MST - Mikhail Soloviev Tests
# Copyright 2022 <mikhail.soloviov@mail.ru>
# OSI Level 2 access functions used in MST
"""
from mstSettingsAndHelpers import *
from mstScapier import *

"""
OSI Level2 operation: Broadcast Ethernet network collecting responded MACs and IPs
"""
def mstOsiLevel2BroadcastDiscovery():
    mstPrint(3, "mstOsiLevel2BroadcastDiscovery start ------")
    ret = []
    ipRange = mstDefaultIP + '/' + str(mstDefaultIPMask) # e.g. '192.168.1.4/30'
    discoveredIPsMacs = mstDiscoverIps(ipRange)
    if not discoveredIPsMacs:
        mstPrint(2, "mstOsiLeve2BroadcastDiscovery: Nothing discovered")
    else:
        discoveredIPsMacs.sort()
        ret = discoveredIPsMacs
        mstPrint(2, "mstOsiLeve2BroadcastDiscovery result:", discoveredIPsMacs)
    mstPrint(3, "mstOsiLeve2BroadcastDiscovery end ------")
    return ret

# Call examples; keep commented out:
#mstOsiLevel2BroadcastDiscovery()
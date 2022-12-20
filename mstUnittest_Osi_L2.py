'''
# SPDX-License-Identifier: LGPL-3.0-or-later
# MST - Mikhail Soloviev Tests
# Copyright 2022 <mikhail.soloviov@mail.ru>
# python unittest for LAN at OSI Level 2
'''
import unittest
from mstNetworkOperations import *

unittest.knownHosts = []
unittest.aliveHosts = []

class L2TestSute(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        unittest.knownHosts = mstReadHostDatabase()

    def testHostsAreAlive(self):
        unittest.aliveHosts = mstOsiL2_BroadcastDiscovery()
        self.assertTrue(unittest.aliveHosts)

    def testHostsAreKnown(self):
        res = []
        record = []
        for record in unittest.aliveHosts:
            res = mstFindLineInList(unittest.knownHosts, record)
        if not res:
            mstPrint(2, 'TEST ERROR: unexpected host', record)
        self.assertTrue(unittest.aliveHosts)

if __name__ == '__main__':
    unittest.main()
'''
# SPDX-License-Identifier: LGPL-3.0-or-later
# MST - Mikhail Soloviev Tests
# Copyright 2022 <mikhail.soloviov@mail.ru>
# pytest Suite enabled tests for TBA
'''
import pytest
from mstNetworkOperations import *

# Suite-wide global variables:
pytest.mstKnownHosts = []
pytest.mstAliveHosts = []
pytest.mstAllowedPorts = []
pytest.mstOpenPorts = []

#Place Fixtures in here; they called each time before running each test if reffed:
#@pytest.fixture
#def someInit(): return []

def test_SuiteIsClean(): # 1st
    ''' pytest.mstXXXX should exist but be None '''
    assert not pytest.mstKnownHosts
    assert not pytest.mstAliveHosts
    assert not pytest.mstAllowedPorts
    assert not pytest.mstOpenPorts

def test_LoadTestDatasets(): # 2nd
    ''' load test datasets an check they loaded '''
    pytest.mstKnownHosts = mstReadHostDatabase()
    assert pytest.mstKnownHosts
    pytest.mstAllowedPorts = mstReadPortDatabase()
    assert pytest.mstAllowedPorts

def test_L2_BroadcastDiscovery(): # 3rd
    ''' Broadcast should return any real results '''
    pytest.mstAliveHosts = mstOsiL2_BroadcastDiscovery()
    assert pytest.mstAliveHosts

def test_L2_BroadcastReturnsRecords():
    ''' Broadcast should return at least first record '''
    assert pytest.mstAliveHosts[0]

def test_L2_BroadcastReturnsOnlyKnownHosts():
    ''' Broadcast should return only already known records '''
    assert pytest.mstAliveHosts # sanity check
    for record in pytest.mstAliveHosts:
        res = mstFindLineInList(pytest.mstKnownHosts, record)
        if not res:
            mstPrint(2, 'TEST ERROR: unexpected host', record)
        assert res

def test_L4_FindOpenedPorts():
    ''' Find network ports that and listening for incoming connections should bring some '''
    assert pytest.mstAliveHosts # sanity check
    openPorts = []
    for host in pytest.mstAliveHosts:
        res = mstOsiL4_ScanPorts(host[0], (1, 1024))
        if res:
            for record in res:
                openPorts.append(record)
    assert openPorts
    pytest.mstOpenPorts = openPorts
    mstPrint(3, 'TEST DEBUG: Opened port list', pytest.mstOpenPorts)

def test_L4_OpenedPortsExist():
    ''' Any opened port exists in the network '''
    assert pytest.mstOpenPorts[0]

def test_L4_OpenedPortsAreAllAllowed():
    ''' Should not find unexpected new opened ports '''
    assert pytest.mstOpenPorts # sanity check
    for record in pytest.mstOpenPorts:
        res = mstFindLineInList(pytest.mstAllowedPorts, record)
        if not res:
            mstPrint(2, 'TEST ERROR: unexpected opened port', record)
        assert res

def Rest_FailingJustForDemonstration():
    ''' just an example that any test may fail one day '''
    assert 11 == 22

# Call examples; keep commented out:
#init: test_LoadTestDatasets(); test_L2_BroadcastDiscovery()
#test_L2_BroadcastReturnsOnlyKnownHosts()
#test_L4_FindOpenedPorts(); test_L4_OpenedPortsAreAllAllowed()

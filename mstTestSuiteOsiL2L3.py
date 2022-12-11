"""
# SPDX-License-Identifier: LGPL-3.0-or-later
# MST - Mikhail Soloviev Tests
# Copyright 2022 <mikhail.soloviov@mail.ru>
# pytest Suite enabled tests for TBA
"""
import pytest
from mstNetworkOperations import *

# Suite-wide global variables:
pytest.mstAliveHosts = []
pytest.mstKnownHosts = []

#Place Fixtures in here; they called each time before running each test if reffed:
#@pytest.fixture
#def someInit(): return []

def test_SuiteIsClean(): # 1st
    '''pytest.mstXXXX should exist but be None'''
    assert not pytest.mstAliveHosts
    assert not pytest.mstKnownHosts

def test_LoadHostDatabase(): # 2nd
    '''we loaded host database'''
    pytest.mstKnownHosts = mstReadHostDatabase()
    assert pytest.mstKnownHosts

def test_L2BroadcastDiscovery(): # 3rd
    '''Broadcast should return any real results'''
    pytest.mstAliveHosts = mstOsiLevel2BroadcastDiscovery()
    assert pytest.mstAliveHosts

def test_L2BroadcastReturnsRecords():
    '''Broadcast should return at least first record'''
    assert pytest.mstAliveHosts[0]

def test_L2BroadcastReturnsOnlyKnownHosts():
    '''Broadcast should return only already known records'''
    for record in pytest.mstAliveHosts:
        res = mstFindHostInList(pytest.mstKnownHosts, record)
        assert res

def trest_FailingJustForDemonstration():
    '''just an example that any test may fail one day'''
    assert 11 == 22

# Call examples; keep commented out:
#test_LoadHostDatabase(); test_L2BroadcastDiscovery()
#test_L2BroadcastReturnsOnlyKnownHosts()

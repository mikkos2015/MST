'''
# SPDX-License-Identifier: LGPL-3.0-or-later
# MST - Mikhail Soloviev Tests
# Copyright 2022 <mikhail.soloviov@mail.ru>
# default values and helpers needed for MST
'''
mstDefaultIP = '192.168.1.1'        # default network IP address
mstDefaultIPLast = '-20'            # limits a range by last address, e.g. 192.168.1.1-20 (20 addresses)
mstDefaultIPMask = 28               # masks a range around given one, e.g. 192.168.1.1/28 (16 addresses)
mstMACBroadcastAddress = 'ff:ff:ff:ff:ff:ff'    # Ethernet MAC broadcast mask
mstDefaultTimeout = 6.6             # seconds to wait for network reponses
mstDebugMaxLevel = 3                # debug messaging and logging maximum details level
mstDebugLevel = mstDebugMaxLevel    # debug messaging and logging level 0 to maximum

def mstPrint(level, line1, line2='', line3='', line4=''):
    ''' helper function: prints only when the requested details level is not worst than mstDebugLevel '''
    if level <= mstDebugLevel:
        print(line1, line2, line3, line4)

def mstSortHelperTBA(oneDimentionList):
    '''
    helper function: allows using built in sort() for 2-dimention lists by 2nd field in the inner list
    e.g. listXby2.sort(key=mstSortHelper2) makes [[3,1], [1,2], [2,3]]
    '''
    return oneDimentionList[1]

def mstFindLineInList(list, line):
    ''' helper function: Is given line [str1, str2] present in the list? '''
    mstPrint(3, 'start ------')
    ret = False
    if not list or not line:
        mstPrint(2, 'mstFindLineInList WARNING: empty parameter(s)!')
    else:
        for record in list:
            if (line == record):
                ret = True
    mstPrint(3, 'end ------')
    return ret

def mstMergeLists(oldList, addList):
    ''' helper function: Insert records from addList to oldList if they are not already in there '''
    ret = []
    if (not oldList or not addList):
        mstPrint(1, 'mstMergeLists: ERROR: wrong parameter(s)!')
    else:
        for pair in addList:
            if not mstFindLineInList(oldList, pair):
                oldList.append(pair)
                ret.append(pair)
                mstPrint(3, 'record was added to the list')
    return ret

def mstReadHostDatabase(filename='KnownHosts.txt'):
    '''
    returns a list of all expected [IP, MAC] that may be used as pre-defined Test Data Set
    TODO: implement read/save; currently the base is hardcoded; e.g. with open(filename) as f: lines = f.read().splitlines() etc.
    '''
    mstPrint(3, 'mstReadHostDatabase start ------')
    ret = [ ['192.168.1.1', 'f4:6d:04:7e:76:18'],
            ['192.168.1.3', '26:03:b4:4a:bb:10'],
            ['192.168.1.4', '24:92:0e:ab:72:4c'],
            ['192.168.1.5', 'ac:22:0b:a5:08:e5'],
            ['192.168.1.6', '26:a3:90:15:3f:3d'],
            ['192.168.1.8', '52:36:93:27:bb:3f'],
            ['192.168.1.11', '00:1c:b3:bc:6c:b6'],
            ['192.168.1.12', '70:4d:7b:62:58:76'],
            ['192.168.1.13', '00:13:e8:1d:8c:c1'] ]
    mstPrint(3, 'mstReadHostDatabase end ------')
    return ret

def mstReadPortDatabase(filename='KnownPorts.txt'):
    '''
    returns a list of allowed [IP, port] that may be used as pre-defined Test Data Set
    TODO: implement read/save; currently the base is hardcoded
    '''
    mstPrint(3, 'mstReadPortDatabase start ------')
    ret = [ ['192.168.1.1', 80], ['192.168.1.1', 515],
            ['192.168.1.11', 135], ['192.168.1.11', 139],
            ['192.168.1.11', 445],
            ['192.168.1.13', 139], ['192.168.1.13', 445],
            ['192.168.1.13', 554], ['192.168.1.13', 912],
            ['192.168.1.13', 135] ]
    mstPrint(3, 'mstReadPortDatabase end ------')
    return ret

# Call examples; keep commented out:
#list=[['aa', 'bb']]; addition=mstMergeLists(list, [['cc','dd'],['aa','bb'],['aa']])
#print('list=', list, 'addition=', addition)
#mstReadHostDatabase()
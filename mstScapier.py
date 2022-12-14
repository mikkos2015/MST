'''
# SPDX-License-Identifier: LGPL-3.0-or-later
# MST - Mikhail Soloviev Tests
# Copyright 2022 <mikhail.soloviov@mail.ru>
# wrapper around scapy API to network L2/L3/.../L7 access
'''
from mstSettingsAndHelpers import *
from scapy import config
config.Conf.load_layers.remove("x509")  # this is a trick to allow any debug
config.Conf.verb=mstDebugLevel          # scapy (default 2) messaging is prety the same to MST
from scapy.all import *

def mstDiscoverIps(ipAddr=mstDefaultIP):
    ''' discovers given address(es) using ARP (Address Resolve Protocol); returns list of [IP, MAC] '''
    mstPrint(3, 'mstDiscoverIps() started---')
    ret = []
    partReqEther = scapy.layers.l2.Ether(dst=mstMACBroadcastAddress)
    partReqARP = scapy.layers.l2.ARP(pdst=ipAddr)
    packBroadcastReq = partReqEther/partReqARP # broadcast packet
    # Send L2 ARP packets; unansered requests from [1] ignored:
    listBroadcastResps = scapy.sendrecv.srp(packBroadcastReq, timeout=mstDefaultTimeout)[0]

    for respRecord in listBroadcastResps:
        answer = respRecord[1]  # each response costans the original request [0] and the answer [1]
        mstPrint(3, 'broadcast brought:', answer.summary())
        answeredMAC=answer['Ether'].src
        answeredIP=answer['ARP'].psrc
        mstPrint(2, f'mstDiscoverIps(): IP {answeredIP} at MAC {answeredMAC}')
        ret.append([answeredIP, answeredMAC])
    mstPrint(3, 'mstDiscoverIps() ended---')
    return ret

def mstIcmpPing(ipAddr=mstDefaultIP, text='dummy'):
    ''' sends default Ping Echo Request using ICMP (Internet Control Message Protocol);
        returns response text or mstEmptyPingText or None '''
    mstPrint(3, f'{mstIcmpPing.__name__} started---')
    ret = None
    if isinstance(text, str):
        echoBinText = text.encode('utf-8')
    else:
        mstPrint(2, 'Wrong ping text provided, using default')
        echoBinText = mstDefaultPingText.encode('utf-8')
    partReqIp = scapy.layers.inet.IP(dst=ipAddr)
    partReqIcmp = scapy.layers.inet.ICMP(type=8)
    partRawReq = scapy.packet.Raw(load=echoBinText)
    packPingReq = partReqIp/partReqIcmp/partRawReq # broadcast packet
    # Send L2 ARP packets; unansered requests from [1] ignored:
    listPingResps = scapy.sendrecv.sr(packPingReq, timeout=mstDefaultTimeout, retry=0)[0]

    if listPingResps:
        answer = listPingResps[0][1] # 0 - correct resps, 1 - answer
        mstPrint(3, 'Ping response:', answer.summary())
        ret = mstEmptyPingText
        rawLayer = answer.getlayer(Raw)
        if rawLayer:
            rawData = rawLayer.load
            if isinstance(rawData, bytes):
                ret = rawData.decode('utf-8')
    mstPrint(3, f'{mstIcmpPing.__name__} ended---')
    return ret

def mstNameResolveWithSnmp(ipAddr=mstDefaultIP):
    ''' TODO: DRAFT and needed rework as SNMP has issues '''
    mstPrint(3, 'mstNameResolveWithSnmp() started---')
    ret = ''
    p1 = scapy.layers.inet.IP(dst=ipAddr)
    p2 = scapy.layers.inet.UDP(sport=161)
    p3 = scapy.layers.snmp.SNMP(community='public',
        PDU=scapy.layers.snmp.SNMPget(
            varbindlist=[scapy.layers.snmp.SNMPvarbind(oid=ASN1_OID("1.3.6.1.2.1.1.5.0"))]))
    p = p1/p2/p3
    r = sr1(p)
    mstPrint(2, 'Summary:', r.summary())
    # TODO: implement result parsing; ATM I do not have plenty SNMP aware devices to implement details
    mstPrint(3, 'mstNameResolveWithSnmp() ended---')
    return ret

def mstCheckIpPorts(ipAddr, ports):
    ''' scans for port(s) opened on the address using TCP; returns positive responses [IP, port] '''
    mstPrint(3, 'mstCheckIpPorts() started---')
    ret = []
    # partReqEther = scapy.layers.l2.Ether(dst=mac, src='00:1c:b3:bc:6c:b6', type='IPv4')
    partReqIP = scapy.layers.inet.IP(dst=ipAddr)
    partReqTCP = scapy.layers.inet.TCP(dport=ports, flags="S")
    packPortReq = partReqIP/partReqTCP # TCP port open packet
    # Send L4 TCP packet(s); TODO: consider using L2 to avoid MAC resolving by scapy:
    listPortResps = scapy.sendrecv.sr(packPortReq, timeout=mstDefaultTimeout, retry=0)[0]
    if not listPortResps:
        mstPrint(2, f'mstCheckIpPorts(): no response from {ipAddr}')
        ret = None
    else:
        for respRecord in listPortResps:
            answer = respRecord[1]  # each response costans the original request [0] and the answer [1]
            status = str(answer['TCP'].flags)
            if 'S' in status: # expect SYN bit among flags like 'SA'
                mstPrint(1, 'RAW response:', answer.summary())
                remoteIP = answer['IP'].src
                remotePortNumber = answer['TCP'].sport
                mstPrint(2, f'mstCheckIpPorts(): got response from {remoteIP}:{remotePortNumber}')
                ret.append([remoteIP, remotePortNumber])
    mstPrint(3, 'mstCheckIpPorts() ended---')
    return ret

# Call examples; keep commented out:
#mstDiscoverIps('192.168.1.1/30')
#mstGetSnmpNameIPs('192.168.1.4')
#
#mstDiscoverIps('192.168.1.1')
#mstCheckIpPorts('192.168.1.1', 80) # 'f4:6d:04:7e:76:18' '24:92:0e:ab:72:4c')
#
#mstCheckIpPorts('192.168.1.1', (80, 90))
#mstIcmpPing('192.168.1.1','abc')
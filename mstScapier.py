"""
# SPDX-License-Identifier: LGPL-3.0-or-later
# MST - Mikhail Soloviev Tests
# Copyright 2022 <mikhail.soloviov@mail.ru>
# wrapper around scapy (enables network L2/L3/.../L7 access)
"""
from mstSettingsAndHelpers import *
from scapy import config
config.Conf.load_layers.remove("x509")  # to allow any debug
config.Conf.verb=mstDebugLevel          # scapy (default 2) messaging is prety the same to MST
from scapy.all import *

def mstDiscoverIps(ipAddr=mstDefaultIP):
    mstPrint(3, 'mstDiscoverIps() started---')
    ret = []
    partReqEther = scapy.layers.l2.Ether(dst=mstMACBroadcastAddress)
    partReqARP = scapy.layers.l2.ARP(pdst=ipAddr)
    packBroadcastReq = partReqEther/partReqARP # Address Resolve Protocol broadcast packet
    # Send L2 ARP packets; ignore unansered requests from [1]:
    listBroadcastResps = scapy.sendrecv.srp(packBroadcastReq, timeout=mstDefaultTimeout)[0]

    for respRecord in listBroadcastResps:
        answer = respRecord[1]  # each response costans the original request [0] and the answer [1]
        mstPrint(2, 'broadcast brought:', answer.summary())
        answeredMAC=answer['Ether'].src
        answeredIP=answer['ARP'].psrc
        mstPrint(1, f'mstDiscoverIps(): IP {answeredIP} at MAC {answeredMAC}')
        ret.append([answeredIP, answeredMAC])
    mstPrint(3, 'mstDiscoverIps() ended---')
    return ret

def mstNameResolveWithSnmp(ipAddr=mstDefaultIP):
    mstPrint(3, 'mstNameResolveWithSnmp() started---')
    ret = ''
    p1 = scapy.layers.inet.IP(dst="192.168.1.4")
    p2 = scapy.layers.inet.UDP(sport=161)
    p3 = scapy.layers.snmp.SNMP(community="public",
        PDU=scapy.layers.snmp.SNMPget(
            varbindlist=[scapy.layers.snmp.SNMPvarbind(oid=ASN1_OID("1.3.6.1.2.1.1.5.0"))]))
    p = p1/p2/p3
    r = sr1(p)
    mstPrint(2, 'Summary:', r.summary())
    # TODO: implement result parsing; ATM I do not have SNMP aware devices to implement details
    mstPrint(3, 'mstNameResolveWithSnmp() ended---')
    return ret

def mstCheckIpPorts(ipAddr, ports):
    mstPrint(3, 'mstCheckIpPorts() started---')
    ret = []
    # partReqEther = scapy.layers.l2.Ether(dst=mac, src='00:1c:b3:bc:6c:b6', type='IPv4')
    partReqIP = scapy.all.IP(dst=ipAddr)
    partReqTCP = scapy.all.TCP(dport=ports, flags="S")
    packPortReq = partReqIP/partReqTCP # TCP port open packet
    # Send L4 TCP packet(s); use L2 send to avoid MAC resolving:
    listPortResps = scapy.sendrecv.sr(packPortReq, timeout=mstDefaultTimeout, retry=0)[0]
    if not listPortResps:
        mstPrint(1, f'mstCheckIpPorts(): no response from {ipAddr}')
        ret = None
    else:
        for respRecord in listPortResps:
            answer = respRecord[1]  # each response costans the original request [0] and the answer [1]
            status = str(answer['TCP'].flags)
            if 'S' in status: # expect SYN bit among flags like 'SA'
                mstPrint(2, 'RAW response:', answer.summary())
                remoteIP = answer['IP'].src
                remotePortNumber = answer['TCP'].sport
                mstPrint(1, f'mstCheckIpPorts(): got response from {remoteIP}:{remotePortNumber}')
                ret.append([remoteIP, remotePortNumber])
    mstPrint(3, 'mstCheckIpPorts() ended---')
    return ret

# Call examples; keep commented out:
#mstDiscoverIps('192.168.1.1/30')
#mstGetSnmpNameIPs('192.168.1.4')
#mstCheckIpPorts('192.168.1.4', 21) # 'f4:6d:04:7e:76:18' '24:92:0e:ab:72:4c')
#mstCheckIpPorts('192.168.1.12', (1, 1023))
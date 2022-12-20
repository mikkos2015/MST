# MST - Mikhail Soloviev Tests for Network OSI Levels 2/3/.../7

SPDX-License-Identifier: LGPL-3.0-or-later<br>
Copyright 2022 Mikhail Soloviev <mikhail.soloviov@mail.ru>

**Installation**:
- clone this repository:
> `https://github.com/mikkos2015/MST`
- Install Python v3.7 or higher.
- - On linux you may need to allow Pyton network blocking read access:
> `sudo setcap cap_net_raw=eip \$(readlink -f \$(which python3))`
- - On Windows you need to install npcap-1.71.exe to work with WiFi; after restart you may need
> `net start npcap` or `net start npcap_wifi2`
- Install these Python packages with pip:
- - scapy[basic] - Network access library
- - pytest - one may want to switch onto unitest
- - pytest-json-report - [OPIONAL] Stores test results in JSON format

**Typical execution command would be like below**:
- `pytest -v mstPytest_Osi_L2L3L4.py`
- `pytest --json-report --json-report-file=PytestRunReport.json -v mstPytest_Osi_L2L3L4.py`
- `python mstUnittest_Osi_L2.py`

# MST - Mikhail Soloviev Tests for Network OSI Levels 2/3/.../7

SPDX-License-Identifier: LGPL-3.0-or-later
<br>
Copyright 2022 Mikhail Soloviev <mikhail.soloviov@mail.ru>

Installation:
- clone this repository:
> https://github.com/mikkos2015/MST
- Install Python v3.7 or higher
> On linux you may need to allow Pyton network blocking read access:
<br> "sudo setcap cap_net_raw=eip $(readlink -f $(which python3))"
- Install these Python packages with pip:
> scapy - Network access library
<br> pytest - one may want to switch onto unitest
<br> pytest-json-report - [OPIONAL] Stores test results in JSON format

Typical execution command would be like below:
> pytest -v mstTestSuiteOsiL2L3.py
<br> pytest --json-report --json-report-file=TestRunReport.json -v mstTestSuiteOsiL2L3.py
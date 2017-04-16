OOCRAN: Open Orchestrator Cloud Radio Access Network 
====================================================

What is OOCRAN?
===============
OOCRAN is an implementation of the NFV MANO standard architecture, designed for wireless communications and provided by the NLnet foundation, that introduces the management of the radio spectrum. An OpenStack running cluster is necessary (tested on Mitaka release).

Features
========
* Computational resources and Radio Spectrum Sharing.
* Interference avoidance.
* NVFI management for service providers.
* Easy Infrastructure management for infratustructe providers.
* Multi VIM and multi hypervisor support.
* LTE transmission use case.
* VNF Descriptor APIs.
* Graphical User Interface for the NVFI orchestrator.
* OSS/BBS implementation.

Requeriments
============
* Influxdb

Installation
============
Please refer to the OOCRAN Installation guide for a thorough walkthrough [wiki](https://github.com/oocran/oocran/wiki/Installation).

Get Started
===========
As of now, OOCRAN can only be deployed on top of OpenStack environments but OOCRAN will support local hypervisors (Docker, KVM, VirtualBox and VMWare) in subsequent releases. To get started with some examples, please refer to the examples guide.

Creating NFs
============
The Network Functions developing tool kit will provide all the necessary tools to start, manage and monitor your own NFs.

News and Website
================
Information about OOCRAN can be found in the [website](http://oocran.dynu.com/)

Issue tracker
=============
Issues and bug reports should be posted to the GitHub Issue Tracker of this project.

License
=======

This software is licensed under the `AGPL License`. See the ``LICENSE``
file in the top distribution directory for the full license text.

Supported by
============
<img src="https://www.nlnet.nl/image/logo.gif" width="150"/>


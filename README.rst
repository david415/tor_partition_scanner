
tor network partition/clique scanner
====================================

This project has the singular goal of scanning the Tor network
for partitions. However this code originated from bwscanner
which can be found here: https://github.com/TheTorProject/bwscanner

(the original git history is not preserved in this repository)


scan method
===========

It's simple. Make two hop Tor circuits, for each circuit
build we record:

- success
- fail
- timeout
- time duration to failure
- time duration to success

Care is take to not make rapid sequential Tor circuit
builds through the same relays. Said another way: we use the
Fisher Yates shuffle algorithm to shuffle our circuit permutations.


special features
================

- partition scheme allows the scanner to run on multiple
  processes or machines so that different slices of circuit
  permutations can be scanned in parallel

- resume feature allows continuing the scan from that last known
  item in the scan partition


contributors
============

Special thanks to the following excellent humans
who have contributed code:

* Aaron Gibson
* cfcs of https://github.com/cfcs
* Donncha O' Cearbhaill <donncha@donncha.is>
* Leif Ryge
* Meejah <meejah@meejah.ca>


license
=======

GPL3 - see LICENSE file for details

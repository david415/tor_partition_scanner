#!/usr/bin/env python

import sys
from stem.descriptor import parse_file, DocumentHandler

with open(sys.argv[1], 'rb') as consensus_file:
  # Processes the routers as we read them in. The routers refer to a document
  # with an unset 'routers' attribute.

  routers = []
  for router in parse_file(consensus_file, 'network-status-consensus-3 1.0', document_handler = DocumentHandler.ENTRIES):
    if u'Fast' in router.flags and u'Stable' in router.flags and u'Valid' in router.flags:
      router_tuple = (router.bandwidth, router.fingerprint)
      routers.append(router_tuple)

  count = 100
  for router in sorted(routers, key=lambda x: x[0], reverse=True):
    #print "%s %s" % (router[0], router[1])
    print "%s" % router[1]
    count -= 1
    if count == 0:
      break

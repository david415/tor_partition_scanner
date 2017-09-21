#!/usr/bin/env python

import click
import json

from orscanner.probedb import get_probedb


@click.command()
@click.option('--dbfile', default=None, type=str, help="db file name")
@click.option('--probefile', '-p', multiple=True, default=None, type=str, help="")
def main(dbfile, probefile):
    assert dbfile is not None
    probedb = get_probedb(dbfile)

    for path in probefile:
        with open(path, 'r') as probefile:
            results = json.load(probefile)
            for val in results:
                fields = val[u"path"].split(" -> ")
                assert len(fields) == 2
                probedb.add_probe_entry(fields[0], fields[1], val[u"status"], val[u"time_start"], val[u"time_end"])

        
if __name__ == '__main__':
    main()

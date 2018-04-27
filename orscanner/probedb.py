
import os, sys
import base64
import time
import sqlite3
from sqlite3 import IntegrityError

# hidden service directory probe db schema version 1
SCHEMA_v1 = """
CREATE TABLE version
(
 version INTEGER
);

CREATE TABLE scan_log
(
 first_hop               VARCHAR(44),
 second_hop              VARCHAR(44),
 status                  VARCHAR(10),
 reason                  VARCHAR(100),
 start_time              NUMBER,
 end_time                NUMBER
);
"""

def get_db(dbfile, stderr=sys.stderr,
           create_version=(None, None), updaters={}, just_create=False, dbname="db",
           journal_mode=None, synchronous=None):
    """Open or create the given db file. The parent directory must exist.
    create_version=(SCHEMA, VERNUM), and SCHEMA must have a 'version' table.
    Updaters is a {newver: commands} mapping, where e.g. updaters[2] is used
    to get from ver=1 to ver=2. Returns a (sqlite3,db) tuple, or raises
    DBError.
    """
    must_create = not os.path.exists(dbfile)
    try:
        db = sqlite3.connect(dbfile)
    except (EnvironmentError, sqlite3.OperationalError), e:
        raise DBError("Unable to create/open %s file %s: %s" % (dbname, dbfile, e))

    schema, target_version = create_version
    c = db.cursor()

    # Enabling foreign keys allows stricter integrity checking.
    # The default is unspecified according to <http://www.sqlite.org/foreignkeys.html#fk_enable>.
    c.execute("PRAGMA foreign_keys = ON;")

    if journal_mode is not None:
        c.execute("PRAGMA journal_mode = %s;" % (journal_mode,))

    if synchronous is not None:
        c.execute("PRAGMA synchronous = %s;" % (synchronous,))

    if must_create:
        c.executescript(schema)
        c.execute("INSERT INTO version (version) VALUES (?)", (target_version,))
        db.commit()

    try:
        c.execute("SELECT version FROM version")
        version = c.fetchone()[0]
    except sqlite3.DatabaseError, e:
        # this indicates that the file is not a compatible database format.
        # Perhaps it was created with an old version, or it might be junk.
        raise DBError("%s file is unusable: %s" % (dbname, e))

    if just_create: # for tests
        return (sqlite3, db)

    while version < target_version and version+1 in updaters:
        c.executescript(updaters[version+1])
        db.commit()
        version = version+1
    if version != target_version:
        raise DBError("Unable to handle %s version %s" % (dbname, version))

    return (sqlite3, db)

def get_probedb(dbfile, stderr=sys.stderr,
                      create_version=(SCHEMA_v1, 1), just_create=False):
    try:
        (sqlite3, db) = get_db(dbfile, stderr, create_version,
                               just_create=just_create, dbname="probedb")
        if create_version[1] in (1, 2):
            return ProbeDB(sqlite3, db)
        else:
            print >>stderr, "invalid probedb schema version specified"
            return None
    except DBError, e:
        print >>stderr, e
        return None

class ProbeDB(object):
    VERSION = 1

    def __init__(self, sqlite_module, connection):
        self.sqlite_module = sqlite_module
        self.connection = connection
        self.cursor = connection.cursor()

    def add_probe_entry(self, first_hop, second_hop, status, start_time, end_time, reason):
        self.cursor.execute("INSERT INTO scan_log VALUES (?,?,?,?,?,?)",
                            (first_hop, second_hop, status, reason, start_time, end_time))
        self.connection.commit()


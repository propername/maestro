import os.path
import maestro.lib.manage_db

if not os.path.isfile('../db/testing.db'):
    db = manage_db.Database_Connection('testing')
    db.create_tables()
    db.insert_acts('A',0,'action A')
    db.insert_acts('B',1,'action B')

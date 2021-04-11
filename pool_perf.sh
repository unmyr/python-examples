#!/bin/bash
/usr/bin/time -v python database/sqlalchemy-postgresql/src/sqlalchemy_pool_NullPool.py postgresql+pg8000
/usr/bin/time -v python database/sqlalchemy-postgresql/src/sqlalchemy_pool_NullPool.py postgresql+psycopg2
/usr/bin/time -v python database/sqlalchemy-postgresql/src/sqlalchemy_pool_QueuePool.py postgresql+pg8000
/usr/bin/time -v python database/sqlalchemy-postgresql/src/sqlalchemy_pool_QueuePool.py postgresql+psycopg2

# -*- coding: utf-8 -*-
"""Example of postgresql+pg8000."""
import json
import os
import traceback
from logging import getLogger, StreamHandler, DEBUG, Formatter

import sqlalchemy
from sqlalchemy import text


logger = getLogger(__name__)
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False
stream_handler.setFormatter(
    Formatter('[%(asctime)s] %(levelname)s: %(message)s')
)


def main(engine):
    """Run main."""
    result = {
        'statusCode': 500,
        'body': 'Internal Server Error.'
    }
    try:
        query_results = []
        logger.info('engine.connect()')
        with engine.connect() as connection:
            logger.info('connection.execute()')
            rows = connection.execute(
                text("SELECT * FROM FruitsMenu")
            )
            for row in rows:
                query_results.append({'name': row['name'], 'price': row['price']})
                # print(f"name={row['name']} price={row['price']}")
        return {
            'statusCode': 200,
            'body': json.dumps(query_results)
        }

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)
        result = {
            'statusCode': 500,
            'body': json.dumps(traceback.format_exc())
        }

    return result


if __name__ == '__main__':
    engine_pg8000 = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            'postgresql+pg8000',
            host=os.environ.get('PGHOST'),
            port=os.environ.get('PGPORT'),
            database=os.environ.get('PGDATABASE'),
            username=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        )
    )
    print(main(engine_pg8000))

# EOF

import json
import psycopg2
from configparser import ConfigParser
import redis

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    print('database configged')
    print(db)
    return db

def build():
    print('build...')
    try:
        # connect to database 
        conn = connect()
        cur = conn.cursor()
        sqlCommand = """
            create function slow_version() RETURNS text AS
            $$
              select pg_sleep(5);
              select version();
            $$
            LANGUAGE SQL;
        """
        cur.execute(sqlCommand)
        print('Closing connection to build database...')
        cur.close() 
        conn.close()
    
        return 0
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def fetch(sql):
    print('fetch...')
    ttl = 10 # Time to live in seconds
    try:
        params = config(section='redis')
        print('cache?...')
        cache = redis.Redis.from_url(params['redis_url'])
        result = cache.get(sql)
        print('cache found')

        if result:
            print('cache match ')
            return result
        else:
            # connect to database listed in database.ini
            conn = connect()
            cur = conn.cursor()
            cur.execute(sql)
            # fetch one row
            result = cur.fetchone()
            print('Closing connection to database...')
            cur.close() 
            conn.close()

        # cache result
        cache.setex(sql, ttl, ''.join(result))
        return result
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def connect():
    # """ Connect to the PostgreSQL database server and return a cursor """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print('Connected!')
		
        # return a conn
        return conn
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def lambda_handler(event, context):
    
    # build()
    retval = ''
    sql = 'SELECT slow_version();'
    db_result = fetch(sql)
    print('db_result:',db_result)
    
    retval = 'DB Version = ' + ''.join(db_result)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": retval,
            # "location": ip.text.replace("\n", "")
        }),
    }

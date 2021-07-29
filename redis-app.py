import json
import psycopg2
import redis
import os

def config():
    
    print("dbhost = " + os.environ['DB_Host'])

    # get section, default to postgresql
    db = {}
    db['host'] = os.environ['DB_Host']
    db['database'] = os.environ['DB_Type']
    db['user'] = os.environ['DB_Username']
    db['password'] = os.environ['DB_Password']
    db['port'] = os.environ['DB_Port']

    print('database configged')
    print(db)
    return db

def fetch(sql):
    print('fetch...')
    ttl = 10 # Time to live in seconds
    try:
        print('cache?...')
        cache = redis.Redis.from_url('redis://' + os.environ['REDIS_URL'] +':6379')
        result = cache.get(sql)
        print('cache found')

        if result:
            print('cache match ')
            return result.decode('utf-8')
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
        cache.set(sql, ("".join(result)).encode('utf_8'), ex=ttl)
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
    
    sql = 'SELECT slow_version();'
    db_result = fetch(sql)
    print('db_result:',db_result)
    
    retval = 'DB Version = ' 
    if db_result:
        retval = retval + ''.join(db_result)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": retval,
        }),
    }

import psycopg2
import os
import cfnresponse

def connect():
    # """ Connect to the PostgreSQL database server and return a cursor """
    conn = None
    try:
        # read connection parameters
        params = {}
        params['host'] = os.environ['DB_Host']
        params['database'] = os.environ['DB_Type']
        params['user'] = os.environ['DB_Username']
        params['password'] = os.environ['DB_Password']
        params['port'] = os.environ['DB_Port']

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print('Connected!')
		
        # return a conn
        return conn
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def build():
    print('build...')
    try:
        sqlCommand = """;
            create or replace function slow_version() RETURNS text AS
            $$
              select pg_sleep(5);
              select version();
            $$
            LANGUAGE SQL;
        """
        # connect to database 
        conn = connect()
        cur = conn.cursor()
        cur.execute(sqlCommand)
        print('Closing connection to build database...')
        cur.close() 
        conn.close()
    
        return 0
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def lambda_handler(event, context):
    try:
        print('lambda_handler started...')
        db_result = build()
        print('... build complete!')
    
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except (Exception) as error:
        print(error)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})

import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
import sys
import psycopg2.extras as extras
import os

class DB:    
    def __init__(self):
        self.connection = self.get_connection()
    
    def get_connection(self):
        #this would generally be stored in a config file in the container.. 
        #or using e.g. AWS secrets manager
        params =  {
            "host"      : "shelltest.czfeljkgnxtd.eu-west-2.rds.amazonaws.com",              
            "port"      : "5432",
            "database"  : "mktdata",
            "user"      : "postgres",
            "password"  : "1EsIfsze2Ki1CPmD2qFM",
        }            
        conn = None        
        try: 
            conn = psycopg2.connect(**params)
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            sys.exit(1) 
        return conn

    def get_df_from_sql(self, conn, sql):
        df =  pd.DataFrame(columns=["a","b"])  
        try:
            df = sqlio.read_sql_query(sql, conn)        
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            return 1
        return df

    def execute_mogrify(self, df, table):
        """
        Using cursor.mogrify() to build the bulk insert query
        then cursor.execute() to execute the query
        """
        success = False
        #get the connection
        if self.connection.closed > 0:
            self.connection = self.get_connection()
        conn = self.connection

        # Create a list of tupples from the dataframe values
        tuples = [tuple(x) for x in df.to_numpy()]
        # Comma-separated dataframe columns
        cols = ','.join(list(df.columns))
        # SQL quert to execute
        cursor = conn.cursor()
        values = [cursor.mogrify("(%s,%s,%s)", tup).decode('utf8') for tup in tuples]
        query  = "INSERT INTO %s(%s) VALUES " % (table, cols) + ",".join(values)
        query  = query.replace(r'%',r'%%')
        
        try:
            cursor.execute(query, tuples)
            conn.commit()
            success = True
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
        cursor.close()
        return success

    def execute_batch(self, df, table, page_size=1000):
        """
        Using psycopg2.extras.execute_batch() to insert the dataframe
        """
        success = False
        #get the connection
        if self.connection.closed > 0:
            self.connection = self.get_connection()
        conn = self.connection
        # Create a list of tupples from the dataframe values
        tuples = [tuple(x) for x in df.to_numpy()]
        # Comma-separated dataframe columns
        cols = ','.join(list(df.columns))
        # SQL quert to execute
        query = f"INSERT INTO {table}({cols}) VALUES("
        for _ in df.columns:
            query += '%s,'
        query = query.rstrip(',')
        query += ')'

        cursor = conn.cursor()
        try:
            extras.execute_batch(cursor, query, tuples, page_size)
            conn.commit()
            success = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            conn.rollback()
        cursor.close()
        return success

    def execute_sql(self, sql):
        if self.connection.closed > 0:
            self.connection = self.get_connection()
        conn = self.connection
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()    
        
    def fetch_one(self, sql):
        if self.connection.closed > 0:
            self.connection = self.get_connection()
        conn = self.connection
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        return result
        cur.close()    
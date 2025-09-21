import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="irrigacao",
            user="julio",
            password="886317",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()

    def execute_ddl_false(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        
    def execute_ddl_true(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def close(self):
        self.cursor.close()
        self.conn.close()
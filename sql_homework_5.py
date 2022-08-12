from sqlite3 import OperationalError
import psycopg2

# conn = psycopg2.connect(database="contacts_db", user = "postgres",password = "230575")
# # with conn.cursor() as cur:
    

# conn.close()
def create_connection( db_name,db_user,db_password):
    connection = None
    try:
        conn = psycopg2.connect(
          database = db_name,
          user = db_user,
          password = db_password
        )
        print ("Connection to PostgreSQL DB successful")
    except OperationalError as e:
         print(f"The error '{e}' occurred")
    return connection 

def create_tables(conn):
    with conn.cursor() as cur:
        cur.executemany("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40),
            last_name VARCHAR(40),
            email VARCHAR(40) UNIQUE
        );
        CREATE TABLE IF NOT EXISTS phone (
             id SERIAL PRIMARY KEY,
             client_id INTEGER  NOT NULL REFERENCES client(id),
             number INTEGER UNIQUE
        );
        """)
def add_client(conn,n_ame,lastname,email,phone=None):
    with conn.cursor() as cur:
        cur.executemany("""
        INSERT INTO client(name,last_name,email)
        VALUES (n_ame,lastname,email);
        INSERT INTO phone(number, client_id)
        VALUES (phone, (select id from client where e-mail = email));
        """)
    
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""   
        INSERT INTO phone(number, client_id)
        VALUES (phone, client_id);
        """)         




if __name__ == '__main__':

     create_connection("contacts_db", "postgres", "230575" )

     conn.close()


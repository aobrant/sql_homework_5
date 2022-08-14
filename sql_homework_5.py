import psycopg2


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40),
            last_name VARCHAR(40),
            email VARCHAR(40) UNIQUE
            );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone (
             id SERIAL PRIMARY KEY,
             client_id INTEGER  NOT NULL REFERENCES client(id),
             number INTEGER UNIQUE
        );
        """)
        conn.commit()
    return

def add_client(conn,name,last_name,email,number=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(name,last_name,email)
        VALUES (%s,%s,%s);
        """,(name,last_name,email))
        if number is not None:
            cur.execute("""
            SELECT id FROM client WHERE name = %s;
            """,(email))
            client_id = cur.fetchone()
            cur.execute("""   
            INSERT INTO phone(number, client_id)
            VALUES (%s, %s);
            """,(number, client_id))    
            conn.commit()

    return
    

def add_phone(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""   
        INSERT INTO phone(number, client_id)
        VALUES (%s, %s);
        """,(number, client_id))    
        conn.commit()
    return


def chg_client(conn,client_id, name=None,last_name=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""   
        UPDATE client
        SET name = %s 
        WHERE (%s <> None) AND client_id = %s;
        """,(name, name, client_id))
        cur.execute("""   
        UPDATE client
        SET last_name = %s 
        WHERE (%s <> None) AND client_id = %s;
        """,(last_name, last_name, client_id))
        cur.execute("""   
        UPDATE client
        SET email = %s 
        WHERE (%s <> None) AND client_id = %s;
        """,(email, email, client_id))

        conn.commit() 
    return 


def phone_remove(conn, client_id,phone):
    with conn.cursor() as cur:
        cur.execute("""   
        DELETE FROM phone WHERE phone = %s AND client_id = %s
        VALUES (%s, %s);
        """,(phone, client_id))    
        conn.commit()
    return


def client_remove(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""   
        DELETE FROM phone WHERE client_id = %s
        VALUES (%s);
        """,(client_id,))    
        cur.execute("""   
        DELETE FROM client WHERE client_id = %s
        VALUES (%s);
        """,(client_id,))    
        conn.commit()
    return


def find_client(conn, name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        if name is not None :
            cur.execute("""
            SELECT id FROM client WHERE name = %s;
            """,(name))
            return(cur.fetchone())
        
        if last_name is not None :
            cur.execute("""
            SELECT id FROM client WHERE last_name = %s;
            """,(last_name))
            return(cur.fetchone())
        
        if email is not None :
            cur.execute("""
            SELECT id FROM client WHERE email = %s;
            """,(email))
            return(cur.fetchone())
        
        if number is not None :
            cur.execute("""
            SELECT client_id FROM phone WHERE number = %s;
            """,(number))
            return(cur.fetchone())
   


if __name__ == '__main__':
  
     with psycopg2.connect(database="contacts_db", user="postgres", password="230575") as conn:
     
         create_tables(conn)
         add_client(conn,name = 'Alex',last_name = 'Petrov',email = 'asd@mail.ru',number = 91723598494)
         add_client(conn,name = 'John',last_name = 'Sidorov',email = 'sid@mail.ru',number = 9152330567)
         id = find_client(conn,name='Alex')
         add_phone(conn,client_id = id, number = 9163456789)
         chg_client(conn,id,name='Don')
         id2 = find_client(conn,last_name='Sidorov')
         phone_remove(conn, client_id = id2) 
         client_remove(conn, client_id = id2)

     


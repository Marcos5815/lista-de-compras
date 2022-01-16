import mysql.connector

def conexao():

    try:
        con = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Sua senha",
            database = "mylist"
            
        )
        
    except:
        print("Error connecting to database")
        
    return con
        
def dql(query):
    
    try:
        
        vcon = conexao()
        c = vcon.cursor()
        c.execute(query)
        res = c.fetchall()
        vcon.close()
        return res
    
    except:
        print("error querying the data in the database")
    
    
def dml(query):
    
    try:
        vcon = conexao()
        c = vcon.cursor()
        c.execute(query)
        vcon.commit()
        vcon.close()
    
    except:
        print("Error when updating the data in the database")
import mariadb
import dbcreds
import random, string
#this just has the imports for mariadb and dbcreds it also has the run_procedures that has some excepts to check for some errors
def run_procedures(sql, args):
    try:
        results = None
        conn = mariadb.connect(**dbcreds.conn_params)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        results = cursor.fetchall()
    except mariadb.IntegrityError:
        print("Sorry, what you entered doesn't exist")
    except mariadb.OperationalError:
        print('there is an error in the data base')
    except mariadb.ProgrammingError:
        print('Error in the sql syntax or query execution')
    except Exception as error:
        print('Error:', error)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
        return results
#i made the endpoint here the same as on the slides, should this be changed? maybe try to make sure nothing happens with the data that could affect everything
def check_endpoint_info(sent_data, expected_data):
    for data in expected_data:
        if(sent_data.get(data) == None):
            return f"The {data} paramter is required!"

#this is my token its just something easy to read and check
def generate_token(length=16):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
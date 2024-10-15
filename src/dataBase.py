import sqlite3

def generate_next_id(database, table):
    """
    The function will take the current database and the table that is being accessed and will return the next valid userID.
    This function will work for multiple different tables at a single time as it checks the last userID that was registered in
    the table.
    """
    rows = database.read_all_data_from_table(table)
    if len(rows) == 0:
        last_id_str = "S000"
    else:
        last_id_str = rows[-1][0]
    formatted_id_int = int(last_id_str[1:])
    next_id_int = formatted_id_int + 1
    next_id = "S" + ((3 - len(str(next_id_int))) * "0") + str(next_id_int)
    return next_id

def generate_password_hash(password):
    """
    This feature was not implemented due to time constrainsts.
    """
    # to implement
    return password

def validate_sign_up(current_menu):
    """
    The function will check that every field has valid data entered as well as if the user has entered the same password twice.
    It does not check the actual passwords, instead it check the two password hashes.
    """
    fields = [field.text for field in current_menu.button_ls]
    if (fields[1] != "Full Name") and (generate_password_hash(fields[2]) == generate_password_hash(fields[3])) \
        and (fields[4] in ["A", "B", "C", "D"]) and (fields[5] in ["12", "13"]):
        return True
    else:
        return False

class DataBase:
    """
    This class defines the structure and functionality for how the SQL database it accessed and modified.
    """
    def __init__(self):
        """
        This constructor method has no parameters and therefore will not require any arguments to be passed when a new object is 
        instantiated.
        """
        self.connection = sqlite3.connect("database.db", 5.0)
        self.cursor = self.connection.cursor()
        self.init_database()

    def init_database(self):
        """
        This method will create the required tables if they do not already exist.
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS students (StudentID, firstName, surName, classID, passwordHash)")
        print("Database is open")

    def close_connection(self):
        """
        This method will ensure that all of the data that has been changed is saved/commited to the database. Once this is successful
        it will print a message to show that the database is now closed.
        """
        self.connection.commit()
        print("Database is closed")

    def add_data(self, table, data):
        """
        This method will allow for a new record to be added to a specific table in the database.
        """
        rows = self.read_all_data_from_table(table)
        first_items = [row[0] for row in rows]

        if len(data) == 5 and data[0] not in first_items:
            self.cursor.execute(f"INSERT INTO {table} VALUES(?, ?, ?, ?, ?)", data)

    def remove_data(self, table, primary_key):
        """
        This method will delete a certain record from a given table in the database. This record is referenced by its primary key
        (this will be the userID).
        """
        self.cursor.execute(f"DELETE FROM {table} WHERE StudentID = '{primary_key}'")

    def read_all_data_from_table(self, table):
        """
        This method will return a list containing all of the records in the database in the order that they appear.
        """
        self.cursor.execute(f"SELECT * FROM {table}")
        rows = self.cursor.fetchall()

        return rows



# conn Class for Sqlite

import sqlite3
from prettytable import PrettyTable
from rich import print
from random import randint
class SQLiteCrud:
    """"
    SQLiteCrud Class
    
    This class is used to create a connection to a SQLite database.
    It also contains methods to create, read, update, and delete data
    from the database.

    Attributes:
        conn (sqlite3.Connection): Connection to the database.
        cursor (sqlite3.Cursor): Cursor for the database.
    """

    def __init__(self, db_path, table_name=None, csv=None):
        """Initialize database connection and cursor."""
        self.columns_init = ["id INTEGER PRIMARY KEY", "pid INTEGER","Permissions TEXT","Owner TEXT","_Group TEXT", "Size REAL","Type TEXT", "Created_date TEXT",
                    "Modified_date TEXT","Filename TEXT", "Hidden BOOL" ]
        self.columns = ["id", "pid","Permissions","Owner","_Group", "Size","Type", "Created_date", "Modified_date","Filename", "Hidden"]
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        
        self.cursor = self.conn.cursor()
        self.table_name = table_name

        self.drop_table(self.table_name)
        self.load_csv(csv)
        self.current_directory = 0
        self.current_directory_name = "~"

    def load_csv(self, csv):
        """Loads csv file into database"""
        self.create_table(self.table_name, self.columns_init)

        with open(csv) as f:
            data = f.readlines()
            for row in data:
                row = row.strip().split(",")
            #   row.append(random.randint(500,1000000))
                #
                self.insert_data(self.table_name, tuple(row), tuple(self.columns))   
    
    def __raw_results(self, results):
        """Converts raw results to a list of table names."""
        table = []
        for row in results:
            table.append(row[0])
        return table
    
    def __formatted_results(self, results):
        """Formats results into a PrettyTable."""
        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(results)
        return table

    def get_columns(self, table_name):
        """
            Get the columns of a table.

            Args:
                table_name (str): Name of the table to get columns from.
        """
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        results = self.cursor.fetchall()
        columns = []

        for column_info in results:
            column_name = column_info[1]
            columns.append(column_name)
        self.columns = columns
        return columns
    
    def insert_data(self, table_name, data, columns=None):
        """
            Inserts data in a table.

            Args:
                table_name (str): Name of the table to insert data into.
                data (tuple): Tuple of values to insert into the table.
                columns (tuple): Tuple of columns to insert data into.
        """
        if not columns:
            columns = tuple(self.columns)
        try:
            # Retrieve all data from the table
            #placeholders = ", ".join(["?"] * len(data))
            insert_query = f"INSERT INTO {table_name} {columns} VALUES {data};"
            self.cursor.execute(insert_query)
            self.conn.commit()
            # print(f"Inserted data into table '{table_name}'.")
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")
 
    def close_connection(self):
        """Close the connection to the database."""
        self.conn.close()
        #print("Database connection closed.")

    def formmated_print(self, table_name):
        """
            Print the contents of a table in a formatted way.
        
            Args:
                table_name (str): Name of the table to print.
        """
        self.cursor.execute(f"SELECT * FROM {table_name};")
        table_info = self.cursor.fetchall()

        table_info_list = []

        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(table_info)
        return table
    
    def table_exists(self, table_name, db_path = None):
        """
            Checks if a table exists in the database.

            Args:
                table_name (str): Name of the table to check.
                db_path (str): Path to the database.
        """
        different_conn = False
        if not db_path:
            db_path = self.db_path
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
        else:
            different_conn = True
            conn = self.conn
            cursor = self.cursor()

        try:
            # Query the sqlite_master table to check if the table exits
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            result = cursor.fetchone()

            # If result is not None, the table exists
            return result is not None
        
        except sqlite3.Error as e:
            print(f"Error checking if table exists: {e}")
            return False
        finally:
            if different_conn:
                conn.close()
                print("Database connection closed.")
 
    def create_table(self, table_name, columns):
        """
            Creats a table in the database.

            Params:
                table_name (str): Name of the table to create.
                columns (list): List of columns to create in the table.
                   
            Args:
                table_name (str): Name of the table to create.
                columns (list): List of columns to create in the table.
        """
        try:
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
            self.cursor.execute(create_table_query)
            self.conn.commit()
            # print(f"Table '{table_name}' created.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
    
    def get_perms(self,table_name,filename):
        """
        Gets the permission associated with a given filename from a table.

        Args:
            table_name (str): Name of the table to query.
            filename (str): The filename to look for.

        Returns:
            int: The permissions as a string associated with the given filename.
        """
        try:
            select_query = f"SELECT Permissions FROM {table_name} WHERE Filename = ?;"
            self.cursor.execute(select_query, (filename,))
            result = self.cursor.fetchone()

            if result:
                return result[0]  # Extract the first (and only) value from the result
            else:
                return None  # Return None if the filename was not found
        except sqlite3.Error as e:
            print(f"Error retrieving Permissions: {e}")
  
    def get_pid(self, table_name, filename):
        """
        Gets the PID value associated with a given filename from a table.

        Args:
            table_name (str): Name of the table to query.
            filename (str): The filename to look for.

        Returns:
            int: The PID value associated with the given filename.
        """
        try:
            select_query = f"SELECT pid FROM {table_name} WHERE Filename = ?;"
            self.cursor.execute(select_query, (filename,))
            result = self.cursor.fetchone()

            if result:
                return result[0]  # Extract the first (and only) value from the result
            else:
                return None  # Return None if the filename was not found
        except sqlite3.Error as e:
            print(f"Error retrieving PID: {e}")

    def read_data(self, table_name, condition_column=None, condition_value=None, order_by=None, order="ASC"):
        """
            Reads data from a table.

            Args:
                table_name (str): Name of the table to read data from.
        """
        try:
            if order_by:
                order = f"ORDER BY {order_by} {order}"
            else:
                order = ""
            
            if condition_column and condition_value:
                # Retrieve all data from the table
                select_query = f"SELECT * FROM {table_name} WHERE {condition_column} = '{condition_value}' {order};"
                self.cursor.execute(select_query)
                results = self.cursor.fetchall()
                #print(f"Retrieved data from table '{table_name}'.")
                output = []
                for row in results:
                    output.append(dict(zip(self.columns, row)))
                return output
            else:
                # Retrieve all data from the table
                select_query = f"SELECT * FROM {table_name} {order};"
                self.cursor.execute(select_query)
                results = self.cursor.fetchall()
                #print(f"Retrieved data from table '{table_name}'.")
                output = []
                for row in results:
                    output.append(dict(zip(self.columns, row)))
                return output
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")

    def update_data(self, table_name, column, new_value, condition_column, condition_value):
        """
            Updates data in a table based on a condition.

            Args:
                table_name (str): Name of the table to update data in.
                column (str): Name of the column to update.
                new_value (str): New value to update the column with.
                condition_column (str): Name of the column to use in the condition.
                condition_value (str): Value to use in the condition.
        """
        try:
            # Update the data in the table based on the condition
            update_query = f"UPDATE {table_name} SET {column} = '{new_value}' WHERE {condition_column} = '{condition_value}';" 
            self.cursor.execute(update_query)
            self.conn.commit()
            #print(f"Updated data in table '{table_name}'.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")

    def delete_data(self, table_name, condition_column, condition_value):
        """
            Deletes data in a table based on a condition.

            Args:
                table_name (str): Name of the table to delete data from.
                condition_column (str): Name of the column to use in the WHERE clause.
                condition_value (str): Value to use in the WHERE clause.
        """

        try:
            # Delete the data from the table based on the condition
            delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = '{condition_value}';"
            self.cursor.execute(delete_query)
            self.conn.commit()
            # print(f"Deleted data from table '{table_name}'.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")

    def drop_table(self, table_name):
        """
            Drops a table from the database.

            Params:
                table_name (str): Name of the table to drop.
                columns (list): List of columns to create in the table.
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    created TXT,
                    modified TXT
                    size REAL
                    type TEXT,
                    owner TEXT,
                    owner_group TEXT,
                    permissions TEXT

            Args:
                table_name (str): Name of the table to drop.
        """
        try:
            # Create a table with the given columns
            create_table_query = f"DROP TABLE IF EXISTS {table_name};"
            self.cursor.execute(create_table_query)
            self.conn.commit()
            # print(f"Dropped table '{table_name}' successfully.")
        except sqlite3.Error as e:
            print(f"Error dropping table: {e}")

    def show_tables(self, raw=True):
        """"
            Show all tables in the database.

            Args:
                raw (bool): If True, returns a list of table names.
                    If False, returns a PrettyTable of the results.
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        results = self.cursor.fetchall()

        if not raw:
            return self.__formatted_results(results)
        else:
            return self.__raw_results(results)
        
    def describe_table(self,table_name, raw=False):
        """
            Describes the structure of a table

            Args:
                table_name (str): Name of the table to describe.
                raw (bool): If True, returns a list of table names.
                    If False, returns a PrettyTable of the results.   
        """
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        results = self.cursor.fetchall()
        table = None

        if not raw:
            return self.__formatted_results(results)
        else:
            table = []
            for column_info in results:
                column_name = column_info[1]
                data_type = column_info[2]
                if_nullable = "NULL" if column_info[3] == 0 else "NOT NULL"
                table.append({f"Column Name: {column_name}, Data Type: {data_type}, Nullable: {if_nullable}"})
        return table
    
if __name__ == "__main__":
    db_name = "filesystem.sqlite"
    table = "filesystem"
    csv = "filesysdata.csv"
    conn = SQLiteCrud(db_name, table, csv)

    hidden = 'GROUP BY Type'
    print(conn.read_data(table, "pid", str(0)+"' GROUP BY 'Type "))
    

    # Get Columns
    # print("Columns: ")
    # print(conn.columns)

    # for file in conn.read_data(table):
    #     conn.update_data(table, "file_size", randint(0, 300000), "filename", file["filename"])

    # # Define table schema
    # table_name = "students"
    # columns = ["id TEXT", "name TEXT", "age INTEGER"] 

    # # Create table
    # conn.create_table(table_name, columns)

    # # Insert data
    # data = ("1", "Alice", 25)
    # conn.insert_data(table_name, data)
    

    # data = ("2", "Bob", 22)
    # conn.insert_data(table_name, data)

    # data = ("3", "Charlie", 20)
    # conn.insert_data(table_name, data)

    # # Read Data
    # conn.read_data(table_name)

    # # Update data
    # conn.update_data(table_name, "age", 26, "name", "Alice")

    # # Display table
    # print(conn.formmated_print(table_name))

    # # Delete data
    # conn.delete_data(table_name, "name", "Charlie")

    # # Display table
    # print(conn.formmated_print(table_name))

    # # Drop table
    # conn.drop_table(table_name)

    # # Display tables
    # print(conn.show_tables())

    # Close connection
    conn.close_connection()
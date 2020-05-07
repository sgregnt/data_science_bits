import sqlite3
import pandas as pd

def header():
    """Separator of different code sinppets"""

    global index
    print('*' * 50)
    print('*** (' + str(index) + ')')
    print('*' * 50)
    index = index + 1

def caption(string):
    """Wrappert to print out captions"""

    print('*** (' + string + ') ')


def print_as_table(connection, sql_command):
    print(pd.read_sql_query(sql_command, connection))

def generate_new_table(GENERATE_NEW_TABLE, connection, crsr, sql_command):
    if GENERATE_NEW_TABLE:
        crsr.execute(sql_command)

index = 1

if __name__ == '__main__':

    connection = sqlite3.connect("myTable.db")
    crsr = connection.cursor()

    # run once to create a new table and add values
    GENERATE_NEW_TABLE = False
    ADD_DATA = False

    # run once to create a new table and add values
    GENERATE_NEW_TABLE2 = False
    ADD_DATA2 = False

    sql_command = """CREATE TABLE Users 
                     (id INTEGER PRIMARY KEY, 
                      name VARCHAR(20), 
                      gender CHAR(1));"""

    generate_new_table(GENERATE_NEW_TABLE, connection, crsr, sql_command)

    sql_command = """CREATE TABLE Rides 
                         (id INTEGER PRIMARY KEY, 
                          user_id VARCHAR(20), 
                          distance INTEGER);"""

    generate_new_table(GENERATE_NEW_TABLE, connection, crsr, sql_command)

    if ADD_DATA:
        sql_command = """INSERT INTO 
                          Users (id, name, gender) 
                         VALUES 
                                (1, "Alice", "f"), 
                                (2, "Bob", "m"),
                                (3, "Alex", "m"),
                                (4, "Donald", "m"),
                                (7, "Lee", "f"),
                                (13, "Jonathan", "m"),
                                (19, "Elvis", "m");"""
        crsr.execute(sql_command)

        sql_command = """INSERT INTO 
                          Rides (id, user_id, distance) 
                         VALUES 
                                (1, 1, 120), 
                                (2, 2, 317),
                                (3, 3, 222),
                                (4, 7, 100),
                                (5, 13, 312),
                                (6, 19, 50),
                                (7, 7, 120),
                                (8, 19, 400),
                                (9, 7, 230);"""
        crsr.execute(sql_command)

        connection.commit()

    #=========================================
    # Join on column where left table insures a unique value
    # but the other table might have multiple values
    # how then are the rows aligned?
    #=========================================

    header()

    sql_command = """SELECT
                            *
                     FROM 
                            Users u 
                            LEFT JOIN 
                            Rides r 
                            ON 
                            u.id = r.user_id
                   """

    crsr.execute(sql_command)
    print_as_table(connection, sql_command)

    #=========================================
    # Distance traveled by each user
    #=========================================

    header()

    sql_command = """SELECT
                            u.name AS name, IFNULL(SUM(distance), 0) AS travelled_distance
                     FROM 
                            Users u 
                            LEFT JOIN 
                            Rides r 
                            ON 
                            u.id = r.user_id
                     GROUP BY
                            u.id 
                     ORDER BY
                           travelled_distance DESC, u.name
                   """

    crsr.execute(sql_command)
    print_as_table(connection, sql_command)

    #-------------------------------------------------
    # Adding rows manually
    #-------------------------------------------------

    header()

    sql_command = """CREATE TABLE Sessions 
                     (Sessions_id INTEGER PRIMARY KEY, 
                      duration int);"""

    generate_new_table(GENERATE_NEW_TABLE2, connection, crsr, sql_command)

    if ADD_DATA2:
        sql_command = """INSERT INTO 
                          Sessions (Sessions_id, duration) 
                         VALUES 
                                (1, 30), 
                                (2, 199),
                                (3, 299),
                                (4, 580),
                                (7, 1000);"""

        crsr.execute(sql_command)

    sql_command = """WITH cte AS (
                     SELECT duration/60 AS mins
                     FROM sessions)
            
                     SELECT '[0-5>' AS bin,
                           SUM(CASE WHEN mins<5 THEN 1 ELSE 0 END) AS total
                     FROM cte
                     UNION ALL
                     SELECT '[5-10>' AS bin,
                           SUM(CASE WHEN mins>=5 AND mins<10 THEN 1 ELSE 0 END) AS total
                     FROM cte
                     UNION ALL
                     SELECT '[10-15>' AS bin,
                           SUM(CASE WHEN mins>=10 AND mins<15 THEN 1 ELSE 0 END) AS total
                     FROM cte
                     UNION ALL
                     SELECT '15 or more' AS bin,
                           SUM(CASE WHEN mins>=15 THEN 1 ELSE 0 END) AS total
                     FROM cte;"""
    crsr.execute(sql_command)
    print_as_table(connection, sql_command)


    #-------------------------------------------------
    # Functions in select operate on groups (such as AVG)
    # on the other hand some functions return a column like ABS()
    #-------------------------------------------------

    header()

    sql_command = """SELECT AVG(id=user_id) FROM Rides"""
    crsr.execute(sql_command)
    print_as_table(connection, sql_command)

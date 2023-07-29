import sqlite3

class database:
    def __init__(self):
        self.conn = sqlite3.connect('movies.db')
        self.create_database()
        self.populate_database()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_database(self):
        self.create_table_users()
        self.create_table_movies()
        self.create_table_booking()

    def populate_database(self):
        self.insert_movies()

    def create_table_users(self):
        query = """
                CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT
                );
                """
        self.conn.execute(query)

    def create_table_movies(self):
        query = """DROP TABLE IF EXISTS Movies"""
        self.conn.execute(query)
        query = """
                CREATE TABLE IF NOT EXISTS Movies (
                movie_name TEXT ,
                theatre_name TEXT,
                location TEXT,
                screen TEXT,
                showtime TEXT,
                available_seats text,
                id INTEGER PRIMARY KEY AUTOINCREMENT
                );
                """
        self.conn.execute(query)

    def create_table_booking(self):
        query = """
                CREATE TABLE IF NOT EXISTS booking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                movie_name TEXT,
                theatre_name TEXT,
                location_name TEXT,
                showtime TEXT,
                screen TEXT,
                seat_number TEXT
                );
                """
        self.conn.execute(query)

    def insert_movies(self):
        query = """
                INSERT INTO Movies (movie_name,theatre_name,location,screen, showtime,available_seats)
                VALUES 
                ('Viduthalai', 'Surya Cinemas', 'Villupuram', 'A', '10:00', '1,2,3,4,5,6,7,8,9,10'),
                ('Vikram', 'Surya Cinemas', 'Villupuram', 'A', '13:00', '1,2,3,4,5,6,7,8,9,10'),
                ('PS-2', 'Surya Cinemas', 'Villupuram', 'A', '16:00', '1,2,3,4,5,6,7,8,9,10'),
                ('Soorarai Potru', 'Surya Cinemas', 'Villupuram', 'A', '19:00', '1,2,3,4,5,6,7,8,9,10'),
                ('PS-2', 'Surya Cinemas', 'Villupuram', 'A', '22:00', '1,2,3,4,5,6,7,8,9,10'),                
                ('Viduthalai', 'Surya Cinemas', 'Villupuram', 'B', '10:00', '1,2,3,4,5'),
                ('Vikram', 'Surya Cinemas', 'Villupuram', 'B', '13:00', '1,2,3,4,5'),
                ('PS-2', 'Surya Cinemas', 'Villupuram', 'B', '16:00', '1,2,3,4,5'),
                ('Soorai Potru', 'Surya Cinemas', 'Villupuram', 'B', '19:00', '1,2,3,4,5'),
                ('PS-2', 'Surya Cinemas', 'Villupuram', 'B', '22:00', '1,2,3,4,5'),
                ('Viduthalai', 'Surya Cinemas', 'Pondicherry', 'A', '11:00', '1,2,3,4,5,6,7,8,9,10'),
                ('Vikram', 'Surya Cinemas', 'Pondicherry', 'A', '14:00', '1,2,3,4,5,6,7,8,9,10'),
                ('PS-2', 'Surya Cinemas', 'Pondicherry', 'A', '17:00', '1,2,3,4,5,6,7,8,9,10'),
                ('Soorarai Potru', 'Surya Cinemas', 'Pondicherry', 'A', '20:00', '1,2,3,4,5,6,7,8,9,10'),
                ('PS-2', 'Surya Cinemas', 'Pondicherry', 'A', '23:00', '1,2,3,4,5,6,7,8,9,10');
        
                """
        self.conn.execute(query)

class request:

    def __init__(self):
        self.conn = sqlite3.connect("movies.db")
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def getMovieByLocation(self, location):
        query = "select movie_name, theatre_name, location,showtime, screen, available_seats from Movies where " \
                f"location = '{location}';"

        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result

    def getTheatreByMovies(self, movie_name):
        query = "select movie_name, theatre_name, location, showtime, screen, available_seats" \
                " from Movies where " \
                f"movie_name = '{movie_name}';"
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result

    def createUser(self, username, password):
        query = f'insert into user ' \
                f'(username, password) ' \
                f'values ("{username}","{password}")'
        self.conn.execute(query)

    def validateUser(self, username, password):
        query = "select * from user where " \
                f"username = '{username}' and password = '{password}';"
        result_set = self.conn.execute(query).fetchall()
        if len(result_set) == 0:
            return False
        return True

    def createEntry(self, location, movie_name, theatre, screen, seat, showtime, logged_in_user):
        query = "INSERT INTO booking (user_name, movie_name, " \
                "theatre_name, location_name, showtime, screen, seat_number)" \
                " VALUES " \
                f"('{logged_in_user}', '{movie_name}', '{theatre}', " \
                f"'{location}', '{showtime}', '{screen}', '{seat}') ;"
        self.conn.execute(query)

    def updateMovies(self, location, movie_name, theatre, screen, seat, showtime):
        query = "update Movies " \
                f"set  available_seats = '{seat}' where " \
                f"location = '{location}' " \
                f"and movie_name = '{movie_name}' " \
                f"and theatre_name = '{theatre}' " \
                f"and screen = '{screen}' " \
                f"and showtime = '{showtime}' ;"

        self.conn.execute(query)

    def bookTicket(self, location, movie_name, theatre, screen, seat, showtime, logged_in_user):
        query = "select movie_name, theatre_name, location, showtime, screen, available_seats" \
                " from Movies where " \
                f"location = '{location}' " \
                f"and movie_name = '{movie_name}' " \
                f"and theatre_name = '{theatre}' " \
                f"and screen = '{screen}' "\
                f"and showtime = '{showtime}' ;"

        result_set = self.conn.execute(query).fetchall()
        if len(result_set) != 1:
            return False
        s = result_set[0]["available_seats"]
        li = s.split(",")
        if seat not in li:
            return False
        self.createEntry(location, movie_name, theatre, screen, seat, showtime, logged_in_user)
        li.remove(seat)
        s = ','.join(li)
        self.updateMovies(location, movie_name, theatre, screen, s, showtime)
        return True
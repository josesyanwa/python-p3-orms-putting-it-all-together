import sqlite3

CONN = sqlite3.connect("lib/dogs.db") 
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        if self.id is None:
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            sql = "UPDATE dogs SET name=?, breed=? WHERE id=?"
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        return cls(row[1], row[2], row[0])

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        result = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in result]

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name=? LIMIT 1"
        result = CURSOR.execute(sql, (name,)).fetchone()
        if result:
            return cls.new_from_db(result)
        return None

    @classmethod
    def find_by_id(cls, dog_id):
        sql = "SELECT * FROM dogs WHERE id=? LIMIT 1"
        result = CURSOR.execute(sql, (dog_id,)).fetchone()
        if result:
            return cls.new_from_db(result)
        return None


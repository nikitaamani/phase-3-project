
from db import cursor, conn

class Buses:

    TABLE_BUSES = "buses"

    def __init__(self, name, location_from, location_to,  passengers,price):
        self.id = None
        self.name = name
        self.location_from = location_from
        self.location_to = location_to
        self.passengers = passengers
        self.price = price

    def save(self):
        sql = f"""
        INSERT INTO {self.TABLE_BUSES} (name,location_from,location_to,passengers,price)
        VALUES  (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.name, self.location_from,
                             self.location_to, self.passengers, self.price))
        conn.commit()
        self.id = cursor.lastrowid

        return self

    def decrement_seat(self):
        if self.passengers <= 0:
            raise ValueError("No available seats")
        
        sql = f"""
        UPDATE {self.TABLE_BUSES} SET passengers = passengers - 1 WHERE id = ?
        """
        cursor.execute(sql, (self.id,))
        conn.commit()
        self.passengers -= 1

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location_from": self.location_from,
            "location_to": self.location_to,
            "passengers": self.passengers,
            "price": self.price
        }
    
    @classmethod
    def find_one(cls, id):
        sql = """
            SELECT buses.* FROM buses
            WHERE buses.id = ?
        """
        row = cursor.execute(sql, (id,)).fetchone()
        return cls.row_to_instance(row)
    
    @classmethod
    def find_all_buses(cls):
        sql = """
        SELECT buses.* FROM buses
        """
        rows = cursor.execute(sql).fetchall()

        return [
            cls.row_to_instance(row).to_dict() for row in rows
        ]

    @classmethod
    def row_to_instance(cls, row):
        if row is None:
            return None

        bus = cls(row[1], row[2], row[3], row[4], row[5])
        bus.id = row[0]

        return bus

    @classmethod
    def create_table(cls):
        sql = f"""
          CREATE TABLE IF NOT EXISTS {cls.TABLE_BUSES} (
              id  INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              location_from TEXT NOT NULL,
              location_to VARCHAR NOT NULL,
              passengers INTEGER NOT NULL,
              price INTEGER NOT NULL
          )
          """
        cursor.execute(sql)
        conn.commit()
        print("Buses table created")

Buses.create_table()


#Hard coded the buses into the database
# easycoach = Buses("EasyCoach", "Nairobi", "Nakuru", 67, 1200)
# easycoach.save()
# mashpoa = Buses("MashPoa", "Nakuru", "Kisii", 70, 1000)
# mashpoa.save()
# greenline = Buses("Greenline", "Nairobi", "Mombasa", 68,2200)
# greenline.save()
# climaxcoach = Buses("Climax coach", "Nairobi", "Kisumu", 53, 1500)
# climaxcoach.save()
# enacoach = Buses("Ena Coach", "Nairobi", "Eldoret", 58, 1900)
# enacoach.save()
# supermetro = Buses("Super Metro", "Kericho", "Nairobi", 69, 1300)
# supermetro.save()
# metrotrans = Buses("Metro Trans", "Bungoma", "Uganda", 67, 1900)
# metrotrans.save()
# nairobibus = Buses("Nairobi bus", "Kirinyaga", "Embu", 67, 2000)
# nairobibus.save()
# moderncoast = Buses("Modern Coast", "Nairobi", "Nakuru", 60, 1200)
# moderncoast.save()
# transline = Buses("Transline", "Machakos", "Kikuyu", 69, 1400)
# transline.save()
# honestmax = Buses("Honest Max", "Lodwar", "Nairobi", 67, 1900)
# honestmax.save()
# decenttravel = Buses("Decent Travel", "Baringo", "Kilifi", 65, 1600)
# decenttravel.save()
# prestigeshuttle = Buses("Prestige Shuttle", "Nairobi", "Bomet", 67, 1700)
# prestigeshuttle.save()

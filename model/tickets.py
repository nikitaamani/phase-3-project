
from db import conn, cursor
from models.bus import Buses


class Ticket:

    TABLE_NAME = "tickets"

    def __init__(self, location_from,location_to,  bus_id):
        self.id = None
        self.location_from = location_from
        self.location_to = location_to
        self.bus_id = bus_id

    def save(self):
        

        bus = Buses.find_one(self.bus_id)
        if not bus:
            raise ValueError("Bus not found")
        
        if bus.passengers <= 0:
            raise ValueError("No available seats on the bus")

        sql = f"""
              INSERT INTO {self.TABLE_NAME} (location_from, location_to,  bus_id)
              VALUES (?, ?, ?)
        """
        cursor.execute(sql, (self.location_from, self.location_to, self.bus_id,))
        conn.commit()
        self.id = cursor.lastrowid

        # Decrease the available seats on the bus
        bus.decrement_seat()
        
        return self

    @classmethod
    def create_table(cls):
        sql = f"""
          CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          location_from TEXT NOT NULL,
          location_to TEXT NOT NULL,
          bus_id INTEGER NOT NULL REFERENCES buses(id)
        )
        """
        cursor.execute(sql)
        conn.commit()
        print("Tickets table created successfully")





Ticket.create_table()

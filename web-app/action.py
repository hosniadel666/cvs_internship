from time import sleep
import threading
import sqlite3
import control
import os


class action_worker():
    def __init__(self):
        self.control = control.control()

    def start(self):
        myThread = threading.Thread(target=self.act)
        myThread.daemon = True
        myThread.start()

    def act(self):
        while True:
            self.conn = sqlite3.connect(os.getenv('PATH_2_DB'))
            self.cursor = self.conn.cursor()

            self.cursor.execute("select * from actuator")
            rows = self.cursor.fetchall()
            if len(rows) >= 1:
                for row in rows:
                    self.handle(row[0], row[5], row[6])

            self.conn.commit()
            self.conn.close()

    def handle(self, id, value, type):
        if id == 1:
            if type == "UPDATE":
                self.control.change_brightness(value, id)
            elif type == "OFF":
                self.control.change_brightness(0, id)
            elif type == "ON":
                self.control.change_brightness(100, id)

        elif id == 2:
            if type == "UPDATE":
                self.control.change_brightness(value, id)
            elif type == "OFF":
                self.control.change_brightness(0, id)
            elif type == "ON":
                self.control.change_brightness(value, id)

        elif id == 3:
            if type == "UPDATE":
                self.control.change_brightness(value, id)
            elif type == "OFF":
                self.control.change_brightness(0, id)
            elif type == "ON":
                self.control.change_brightness(value, id)

        elif id == 4:
            if type == "UPDATE":
                self.control.change_servo_angle(value)
            elif type == "OFF":
                self.control.change_servo_angle(2)
            elif type == "ON":
                self.control.change_servo_angle(90)

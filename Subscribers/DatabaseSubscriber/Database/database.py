import os
import datetime
import psycopg2
from Subscribers.DatabaseSubscriber.compartmentPickModel import CompartmentPickModel
from dotenv import load_dotenv
load_dotenv()

CREATE_COMPARTMENT_PICKS_TABLE = """CREATE TABLE IF NOT EXISTS "CompartmentPicks" (
    "Id" SERIAL PRIMARY KEY,
    "PortId" INTEGER,
    "BinType" INTEGER,
    "CompartmentId" INTEGER,
    "CreationTimestamp" TIMESTAMP
);"""
INSERT_COMPARTMENT_PICK = """INSERT INTO "CompartmentPicks" ("PortId", "BinType", "CompartmentId", "CreationTimestamp") VALUES (%s, %s, %s, now())"""
SELECT_ALL_COMPARTMENT_PICKS = """SELECT * FROM "CompartmentPicks";"""
SELECT_COMPARTMENT_PICKS_BY_PORT_ID = """SELECT * FROM "CompartmentPicks" WHERE "PortId"=%s;"""

class Database:
    def __init__(self):
        conn_string = "host="+ os.environ.get("PG_HOST") +" port="+ os.environ.get("PG_PORT") +" dbname="+ os.environ.get("PG_DATABASE") +" user=" + os.environ.get("PG_USER")  +" password="+ os.environ.get("PG_PASSWORD") 
        self.connection = psycopg2.connect(conn_string)
        self.create_tables()
    def create_tables(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(CREATE_COMPARTMENT_PICKS_TABLE)
    def add_pick(self, portId, binType, compartmentId):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(INSERT_COMPARTMENT_PICK, (portId, binType, compartmentId))
    def get_picks(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(SELECT_ALL_COMPARTMENT_PICKS)
                picks = cursor.fetchall()
                return [CompartmentPickModel(*x) for x in picks]
    def get_picks_by_port_id(self, portId):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(SELECT_COMPARTMENT_PICKS_BY_PORT_ID, [portId])
                picks = cursor.fetchall()
                return [CompartmentPickModel(*x) for x in picks]
                
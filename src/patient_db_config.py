"""All sqlalchemy related config goes here, including the database schema definition."""

import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData

DB_FILE_PATH = "patient.db"

CONN = sqlite3.connect(DB_FILE_PATH)
ENGINE = create_engine("sqlite:///" + DB_FILE_PATH, echo=True)
METADATA = MetaData()

PATIENTS_TABLE_NAME = "patients"
PATIENT_ID_COLUMN = "patient_id"
PATIENT_NAME_COLUMN = "patient_name"
PATIENT_AGE_COLUMN = "patient_age"
PATIENT_GENDER_COLUMN = "patient_gender"
PATIENT_CHECKIN_COLUMN = "patient_checkin"
PATIENT_CHECKOUT_COLUMN = "patient_checkout"
PATIENT_WARD_COLUMN = "patient_ward"
PATIENT_ROOM_COLUMN = "patient_room"

PATIENT_COLUMN_NAMES = [
    PATIENT_ID_COLUMN,
    PATIENT_NAME_COLUMN,
    PATIENT_AGE_COLUMN,
    PATIENT_GENDER_COLUMN,
    PATIENT_ROOM_COLUMN,
    PATIENT_WARD_COLUMN,
    PATIENT_CHECKOUT_COLUMN,
    PATIENT_CHECKIN_COLUMN,
]

PATIENTS_TABLE = Table(
    PATIENTS_TABLE_NAME,
    METADATA,
    Column(PATIENT_ID_COLUMN, String, primary_key=True),
    Column(PATIENT_NAME_COLUMN, String),
    Column(PATIENT_AGE_COLUMN, Integer),
    Column(PATIENT_GENDER_COLUMN, String),
    Column(PATIENT_CHECKIN_COLUMN, String),
    Column(PATIENT_CHECKOUT_COLUMN, String),
    Column(PATIENT_WARD_COLUMN, Integer),
    Column(PATIENT_ROOM_COLUMN, Integer),
)

METADATA.create_all(ENGINE)

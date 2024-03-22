import uuid
import datetime
import requests
from config import WARD_NUMBERS, ROOM_NUMBERS, GENDERS, API_CONTROLLER_URL

from patient_db_config import PATIENT_ID_COLUMN
from patient_db_config import PATIENT_NAME_COLUMN
from patient_db_config import PATIENT_AGE_COLUMN
from patient_db_config import PATIENT_GENDER_COLUMN
from patient_db_config import PATIENT_CHECKIN_COLUMN
from patient_db_config import PATIENT_CHECKOUT_COLUMN
from patient_db_config import PATIENT_WARD_COLUMN
from patient_db_config import PATIENT_ROOM_COLUMN


class Patient:
    def __init__(self, name, gender, age):
        self._name = name
        self._gender = gender
        self._age = age
        self._id = self.get_patient_id()
        self._checkin_time = self.generate_current_time()
        self._checkout_time = None
        self._ward_number = None
        self._room_number = None

    def generate_current_time(self):
        return datetime.datetime.now()

    def get_patient_id(self):
        return int(uuid.uuid4())

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_gender(self):
        return self._gender

    def get_age(self):
        return self._age

    def set_checkin_time(self, date_time, now=True):
        if now:
            self._checkin_time = self.generate_current_time()
        else:
            self._checkin_time = date_time

    def set_checkout_time(self, time, now=True):
        if now:
            self._checkout_time = self.generate_current_time()
        else:
            self._checkout_time = time

    def set_ward(self, ward):
        if ward not in WARD_NUMBERS:
            raise ValueError("WARD NUMBER NOT AVAILABLE")
        self._ward_number = ward

    def get_ward(self):
        return self._ward_number

    def validate_room_number(self, room_number):
        conditions = [
            len(str(room_number)) != 2,
            str(room_number)[0] not in WARD_NUMBERS,
        ]
        if any(conditions):
            error = f"Room number {room_number} is invalid"
            raise ValueError(error)
        return True

    def set_room(self, room_number):
        if self.validate_room_number(room_number):
            if self._ward_number is not None:
                if room_number in ROOM_NUMBERS[self._ward_number]:
                    self._room_number = room_number
                else:
                    error = f"Room Number {room_number} is not allocated in the ward {self._ward_number}"
                    raise ValueError(error)
            else:
                self._ward_number = room_number[0]
                self._room_number = room_number

    def get_room(self):
        return self._room_number

    # Compliant with the keys of db
    def get_payload(self):
        return {
            PATIENT_ID_COLUMN: int(self._id),
            PATIENT_NAME_COLUMN: str(self._name),
            PATIENT_AGE_COLUMN: int(self._age),
            PATIENT_GENDER_COLUMN: str(self._gender),
            PATIENT_CHECKIN_COLUMN: str(self._checkin_time),
            PATIENT_CHECKOUT_COLUMN: str(self._checkout_time),
            PATIENT_WARD_COLUMN: int(self._ward_number),
            PATIENT_ROOM_COLUMN: int(self._room_number),
        }

    def commit(self):
        # Commit to the database using requests
        url = f"{API_CONTROLLER_URL}/patients"
        requests.post(url, json=self.get_payload())

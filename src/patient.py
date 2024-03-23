"""Patient Model"""

import uuid
import datetime
import requests
from config import WARD_NUMBERS, ROOM_NUMBERS, API_CONTROLLER_URL

from patient_db_config import PATIENT_ID_COLUMN
from patient_db_config import PATIENT_NAME_COLUMN
from patient_db_config import PATIENT_AGE_COLUMN
from patient_db_config import PATIENT_GENDER_COLUMN
from patient_db_config import PATIENT_CHECKIN_COLUMN
from patient_db_config import PATIENT_CHECKOUT_COLUMN
from patient_db_config import PATIENT_WARD_COLUMN
from patient_db_config import PATIENT_ROOM_COLUMN


class Patient:
    """
    Represents a patient in the hospital.

    Attributes:
        _name (str): The name of the patient.
        _gender (str): The gender of the patient.
        _age (int): The age of the patient.
        _id (int): The unique ID of the patient.
        _checkin_time (datetime): The check-in time of the patient.
        _checkout_time (datetime): The check-out time of the patient.
        _ward_number (int): The ward number where the patient is allocated.
        _room_number (int): The room number where the patient is allocated.
    """

    def __init__(self, name, gender, age):
        """
        Initializes a new instance of the Patient class.

        Args:
            name (str): The name of the patient.
            gender (str): The gender of the patient.
            age (int): The age of the patient.
        """
        self._name = name
        self._gender = gender
        self._age = age
        self._id = self.get_patient_id()
        self._checkin_time = self.generate_current_time()
        self._checkout_time = None
        self._ward_number = None
        self._room_number = None

    def generate_current_time(self):
        """
        Generates the current date and time.

        Returns:
            datetime: The current date and time.
        """
        return datetime.datetime.now()

    def get_patient_id(self):
        """
        Generates a unique ID for the patient.

        Returns:
            int: The unique ID of the patient.
        """
        return int(uuid.uuid4())

    def get_id(self):
        """
        Gets the ID of the patient.

        Returns:
            int: The ID of the patient.
        """
        return self._id

    def get_name(self):
        """
        Gets the name of the patient.

        Returns:
            str: The name of the patient.
        """
        return self._name

    def get_gender(self):
        """
        Gets the gender of the patient.

        Returns:
            str: The gender of the patient.
        """
        return self._gender

    def get_age(self):
        """
        Gets the age of the patient.

        Returns:
            int: The age of the patient.
        """
        return self._age

    def set_checkin_time(self, date_time="", now=True):
        """
        Sets the check-in time of the patient.

        Args:
            date_time (str, optional): The check-in time to set. Defaults to "".
            now (bool, optional): Indicates whether to set the current time. Defaults to True.
        """
        if now:
            self._checkin_time = self.generate_current_time()
        else:
            self._checkin_time = date_time

    def set_checkout_time(self, time="", now=True):
        """
        Sets the check-out time of the patient.

        Args:
            time (str, optional): The check-out time to set. Defaults to "".
            now (bool, optional): Indicates whether to set the current time. Defaults to True.
        """
        if now:
            self._checkout_time = self.generate_current_time()
        else:
            self._checkout_time = time

    def set_ward(self, ward):
        """
        Sets the ward number where the patient is allocated.

        Args:
            ward (int): The ward number to set.

        Raises:
            ValueError: If the ward number is not available.
        """
        if ward not in WARD_NUMBERS:
            raise ValueError("WARD NUMBER NOT AVAILABLE")
        self._ward_number = ward

    def get_ward(self):
        """
        Gets the ward number where the patient is allocated.

        Returns:
            int: The ward number where the patient is allocated.
        """
        return self._ward_number

    def validate_room_number(self, room_number):
        """
        Validates the room number.

        Args:
            room_number (int): The room number to validate.

        Returns:
            bool: True if the room number is valid, False otherwise.

        Raises:
            ValueError: If the room number is invalid.
        """
        conditions = [
            len(str(room_number)) != 2,
            int(str(room_number)[0]) not in WARD_NUMBERS,
        ]
        if any(conditions):
            error = f"Room number {room_number} is invalid"
            raise ValueError(error)
        return True

    def set_room(self, room_number):
        """
        Sets the room number where the patient is allocated.

        Args:
            room_number (int): The room number to set.

        Raises:
            ValueError: If the room number is invalid or not allocated in the ward.
        """
        if self.validate_room_number(room_number):
            if self._ward_number is not None:
                if room_number in ROOM_NUMBERS[self._ward_number]:
                    self._room_number = int(room_number)
                else:
                    error = f"Room Number {room_number} is not allocated in the ward {self._ward_number}"
                    raise ValueError(error)
            else:
                self._ward_number = int(str(room_number)[0])
                self._room_number = int(room_number)

    def get_room(self):
        """
        Gets the room number where the patient is allocated.

        Returns:
            int: The room number where the patient is allocated.
        """
        return self._room_number

    def create_patient_payload(self):
        """
        Creates a payload for the patient to be sent to the database.

        Returns:
            dict: The patient payload.
        """
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
        """
        Commits the patient data to the database.
        """
        url = f"{API_CONTROLLER_URL}/patients"
        requests.post(url, json=self.create_patient_payload(), timeout=10)

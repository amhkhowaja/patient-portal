from patient_db_config import PATIENTS_TABLE, ENGINE, METADATA
from patient import Patient
from sqlalchemy.exc import SQLAlchemyError

class PatientDB():
    def __init__(self):
        pass

    def insert_patient(self, request_body):
        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.insert().values(**request_body)
            result = conn.execute(stmt)
            return result.inserted_primary_key
        except SQLAlchemyError as e:
            print("Error occurred while inserting the patient", e)
            return None
        finally:
            conn.close()
    
    def select_all_patients(self):
        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.select()
            result = conn.execute(stmt)
            return result.fetchall()
        except SQLAlchemyError as e:
            print("Error occurred while selecting all patients", e)
            return None
        finally:
            conn.close()
    
    def select_patient(self, patient_id):
        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.select().where(PATIENTS_TABLE.c.patient_id == patient_id)
            result = conn.execute(stmt)
            return result.fetchone()
        except SQLAlchemyError as e:
            print("Error occurred while selecting the patient", e)
            return None
        finally:
            conn.close()
    
    def update_patient(self, patient_id, update_dict):
        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.update().where(PATIENTS_TABLE.c.patient_id == patient_id).values(**update_dict)
            result = conn.execute(stmt)
            return result.rowcount
        except SQLAlchemyError as e:
            print("Error occurred while updating the patient", e)
            return None
        finally:
            conn.close()
    
    def delete_patient(self, patient_id):
        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.delete().where(PATIENTS_TABLE.c.patient_id == patient_id)
            result = conn.execute(stmt)
            return result.rowcount
        except SQLAlchemyError as e:
            print("Error occurred while deleting the patient", e)
            return None
        finally:
            conn.close()

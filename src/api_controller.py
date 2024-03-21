from flask import Flask, request, jsonify
from patient_db import PatientDB
from patient_db_config import PATIENT_COLUMN_NAMES
from patient_db_config import PATIENT_ID_COLUMN

class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):
        self.app.route('/patients', methods=['GET'])(self.get_patients)
        self.app.route('/patients/<patient_id>', methods=['GET'])(self.get_patient)
        self.app.route('/patients', methods=['POST'])(self.create_patient)
        self.app.route('/patient/<patient_id>', methods=['PUT'])(self.update_patient)
        self.app.route('/patient/<patient_id>', methods=['DELETE'])(self.delete_patient)
    
    def validate_patient_request_body(self, request_body):
        required_fields = PATIENT_COLUMN_NAMES
        if not all(field in request_body for field in required_fields):
            return False
        # I will add more validation here
        return True
    
    def create_patient(self):
        request_body = request.get_json()
        patient_id = request_body.get(PATIENT_ID_COLUMN)
        if not self.validate_patient_request_body(request_body):
            return jsonify({'result': 'failure', 'reason': 'Invalid patient data'}), 400
        result = self.patient_db.insert_patient(request_body)
        if result is None:
            return jsonify({'result': 'failure', 'reason': 'Failed to insert the database'}), 400
        return jsonify({PATIENT_ID_COLUMN: result}), 201


    def get_patients(self):
        result = self.patient_db.select_all_patients()
        if result is None:
            return jsonify({'result': 'failure', 'reason': 'Failed to select the database'}), 400
        return jsonify(result), 200

    def get_patient(self, patient_id):
        result = self.patient_db.select_patient(patient_id)
        if result is None:
            return jsonify({'result': 'failure', 'reason': 'Failed to select the database'}), 400
        return jsonify(result), 200

    def update_patient(self, patient_id):
        update_dict = request.get_json()
        result = self.patient_db.update_patient(patient_id, update_dict)
        if result is None:
            return jsonify({'result': 'failure', 'reason': 'Failed to update the database'}), 400
        return jsonify({'result': 'success updating'}), 200

    def delete_patient(self, patient_id):
        result = self.patient_db.delete_patient(patient_id)
        if result is None:
            return jsonify({'result': 'failure', 'reason': 'Failed to delete the database'}), 400
        return jsonify({'result': 'success deleting'}), 200
        
    def run(self):
        self.app.run()

PatientAPIController()
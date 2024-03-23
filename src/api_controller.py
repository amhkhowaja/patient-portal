"""Patient API Controller"""

from flask import Flask, request, jsonify
from patient_db import PatientDB
from patient_db_config import PATIENT_COLUMN_NAMES
from patient_db_config import PATIENT_ID_COLUMN


class PatientAPIController:
    """
    This class represents the API controller for managing patient data.

    Attributes:
        app (Flask): The Flask application instance.
        patient_db (PatientDB): The patient database instance.

    Methods:
        setup_routes(): Sets up the routes for the API endpoints.
        validate_patient_request_body(request_body): Validates the request body for
        creating a patient.
        row_to_dict(row_values): Converts a row of patient data to a dictionary.
        create_patient(): Creates a new patient.
        get_patients(): Retrieves all patients.
        get_patient(patient_id): Retrieves a specific patient.
        update_patient(patient_id): Updates a specific patient.
        delete_patient(patient_id): Deletes a specific patient.
        run(): Runs the Flask application.
    """

    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):
        """
        Sets up the routes for the API endpoints.
        """
        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)

    def validate_patient_request_body(self, request_body):
        """
        Validates the request body for creating a patient.

        Args:
            request_body (dict): The request body containing patient data.

        Returns:
            bool: True if the request body is valid, False otherwise.
        """
        required_fields = PATIENT_COLUMN_NAMES
        if not all(field in request_body for field in required_fields):
            return False
        # I will add more validation here
        return True

    def row_to_dict(self, row_values):
        """
        Converts a row of patient data to a dictionary.

        Args:
            row_values (tuple): The row values representing a patient.

        Returns:
            dict: The patient data as a dictionary.
        """
        return dict(zip(PATIENT_COLUMN_NAMES, row_values))

    def create_patient(self):
        """
        Creates a new patient.

        Returns:
            tuple: A tuple containing the response data and status code.
        """
        request_body = request.get_json()
        if not self.validate_patient_request_body(request_body):
            return jsonify({"result": "failure", "reason": "Invalid patient data"}), 400
        result = self.patient_db.insert_patient(request_body)[0]
        if result is None:
            return (
                jsonify(
                    {"result": "failure", "reason": "Failed to insert the database"}
                ),
                400,
            )
        return jsonify({PATIENT_ID_COLUMN: result}), 201

    def get_patients(self):
        """
        Retrieves all patients.

        Returns:
            tuple: A tuple containing the response data and status code.
        """
        result = self.patient_db.select_all_patients()
        if result is None:
            return (
                jsonify(
                    {"result": "failure", "reason": "Failed to select the database"}
                ),
                400,
            )
        return jsonify(result), 200

    def get_patient(self, patient_id):
        """
        Retrieves a specific patient.

        Args:
            patient_id (str): The ID of the patient to retrieve.

        Returns:
            tuple: A tuple containing the response data and status code.
        """
        result = self.patient_db.select_patient(patient_id)
        if result is None:
            return (
                jsonify(
                    {"result": "failure", "reason": "Failed to select the database"}
                ),
                400,
            )
        return jsonify(result), 200

    def update_patient(self, patient_id):
        """
        Updates a specific patient.

        Args:
            patient_id (str): The ID of the patient to update.

        Returns:
            tuple: A tuple containing the response data and status code.
        """
        update_dict = request.get_json()
        result = self.patient_db.update_patient(patient_id, update_dict)
        if result is None:
            return (
                jsonify(
                    {"result": "failure", "reason": "Failed to update the database"}
                ),
                400,
            )
        return jsonify({"result": "success updating"}), 200

    def delete_patient(self, patient_id):
        """
        Deletes a specific patient.

        Args:
            patient_id (str): The ID of the patient to delete.

        Returns:
            tuple: A tuple containing the response data and status code.
        """
        result = self.patient_db.delete_patient(patient_id)
        if result is None:
            return (
                jsonify(
                    {"result": "failure", "reason": "Failed to delete the database"}
                ),
                400,
            )
        return jsonify({"result": "success deleting"}), 200

    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run()


PatientAPIController()

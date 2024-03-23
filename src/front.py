"""StreamLit front-end for the patient management system"""

import streamlit as st
import requests
import pandas as pd
from patient import Patient

PATIENTS_API_URL = "http://localhost:5000/patients"
PATIENT_API_URL = "http://localhost:5000/patient"


class Tab:
    """Base class for all the tabs in the app"""

    def __init__(self, name: str):
        self.name = name

    def write(self):
        """Write the contents of the page"""
        st.header(self.name)


class ListPatientsTab(Tab):
    """Tab for listing all patients"""

    def write(self):
        super().write()
        self.view_patients()

    def view_patients(self):
        """
        Fetches patient data from the API and displays it in a table.

        Returns:
            None
        """
        response = requests.get(PATIENTS_API_URL, timeout=5)
        if response.status_code == 200:
            # create a table to show the data
            patients = pd.DataFrame.from_records(response.json(), index="patient_id")
            st.table(patients)
        else:
            st.write("Failed to fetch data")


class InsertPatientTab(Tab):
    """
    Represents a tab for inserting a new patient in the patients portal.

    Attributes:
        None

    Methods:
        write(): Renders the UI elements for inserting a new patient
        and handles the insertion process.
        create_patient(patient_name, patient_gender, patient_age, patient_room):
        Creates a new Patient object with the given details.
        insert_patient(patient_data): Inserts the patient data into the patients API.

    """

    def __init__(self, name: str):
        super().__init__(name)
        self.patient = None
        self.patient_data = None

    def write(self):
        super().write()

        patient_name = st.text_input("Patient name:")
        patient_age = st.text_input("Patient age:")
        patient_gender = st.radio("Pick one:", ["Male", "Female"])
        patient_room = st.text_input("Patient room:")

        if st.button("Insert New Patient"):
            self.patient = self.create_patient(
                patient_name, patient_gender, patient_age, patient_room
            )
            self.patient_data = self.patient.create_patient_payload()
            self.insert_patient(self.patient_data)

    def create_patient(self, patient_name, patient_gender, patient_age, patient_room):
        """
        Creates a new Patient object with the given details.

        Args:
            patient_name (str): The name of the patient.
            patient_gender (str): The gender of the patient.
            patient_age (str): The age of the patient.
            patient_room (str): The room number of the patient.

        Returns:
            patient (Patient): The created Patient object.

        """
        patient = Patient(patient_name, patient_gender, patient_age)
        if patient_room == "":
            patient_room = None
        patient.set_room(patient_room)
        patient.set_checkin_time()

        patient.commit()
        return patient

    def insert_patient(self, patient_data):
        """
        Inserts the patient data into the patients API.

        Args:
            patient_data (dict): The patient data to be inserted.

        Returns:
            None

        """
        response = requests.post(PATIENTS_API_URL, json=patient_data, timeout=5)
        if response.status_code == 201:
            st.write("Patient inserted successfully")
        else:
            st.write("Failed to insert the patient")


class Portal:
    """Main Portal class for the patients portal application."""
    def __init__(self):
        self.patient_tab, self.insert_tab, self.update_tab, self.remove_tab = st.tabs(
            [
                "Patients List",
                "Insert Patient",
                "Update patient",
                "Remove Patient",
            ]
        )

    def run(self):
        """
        Runs the patients portal application.

        This method is responsible for running the patients portal application.
        It selects the page to display using the sidebar,
        and then runs the selected page.

        Args:
            None

        Returns:
            None
        """
        # Use the sidebar to select the page

        # tab_name = st.sidebar.selectbox("Tabs", tuple(self.tabs.keys()))

        # Run the selected page
        # self.tabs[tab_name].write()
        with self.patient_tab:
            ListPatientsTab("Patients List").write()

        with self.insert_tab:
            InsertPatientTab("Insert Patient").write()


# Create an instance of the app and run it
Portal().run()

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
            try:
                patients = pd.DataFrame.from_records(response.json(), index="patient_id")
                st.table(patients)
            except KeyError:
                st.write("No patients found")
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

        response = patient.commit()
        if response.status_code == 201:
            st.write("Patient inserted successfully")
        else:
            st.write("Failed to insert the patient")
        return patient

class UpdatePatientTab(Tab):
    """Patients data can be updated here"""
    def write(self):
        super().write()
        self.search_patient()

    def edited_columns(self, original_df, edited_df):
        """Will show the edited columns in the data editor"""
        # Check which data has been edited
        if not edited_df.equals(original_df):
            st.write('Dataframe has been edited.')

            # Find the rows where the dataframes differ
            diff_df = edited_df != original_df
            edited_cols = diff_df.any()

            # Display the edited data
            st.write('Edited columns:')
            st.write(edited_cols[edited_cols].index.tolist())
        else:
            st.write('Dataframe has not been edited.')

    def edited_rows(self, original_df, edited_df):
        """Will show the edited rows in the data editor"""
        # Check which data has been edited
        if not edited_df.equals(original_df):
            st.write('Dataframe has been edited.')

            # Find the rows where the dataframes differ
            diff_df = edited_df != original_df
            edited_rows = diff_df.any(axis=1)
            edited_data = edited_df[edited_rows]

            # Display the edited data
            st.write('Edited data:')
            st.write(edited_data)
        else:
            st.write('Dataframe has not been edited.')

    def search_patient(self):
        """Search patients with the search bar"""
        search_term = st.text_input("Search Patient By Name")
        if search_term:
            response = requests.get(PATIENTS_API_URL + "?search_name=" + search_term, timeout=5)
            if response.status_code == 200:
                patient_data = response.json()
                try:
                    patients = pd.DataFrame.from_records(patient_data, index="patient_id")
                    new_order = [col for col in patients.columns if col != "patient_name"]
                    new_order.insert(0, "patient_name")
                    patients = patients[new_order]
                    original_data = patients.copy()
                    editable_data = st.data_editor(patients)
                    self.edited_rows(original_data, editable_data)
                    self.edited_columns(original_data, editable_data)
                except KeyError:
                    st.write("No patients found")
            else:
                st.write("Failed to fetch the Patients")
        else:
            response = requests.get(PATIENTS_API_URL, timeout=5)
            if response.status_code == 200:
                patient_data = response.json()
                try:
                    patients = pd.DataFrame.from_records(patient_data, index="patient_id")
                    new_order = [col for col in patients.columns if col != "patient_name"]
                    new_order.insert(0, "patient_name")
                    patients = patients[new_order]
                    st.data_editor(patients)
                except KeyError:
                    st.write("No patients found")
            else:
                st.write("Failed to fetch the Patients")

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

        with self.patient_tab:
            ListPatientsTab("Patients List").write()

        with self.insert_tab:
            InsertPatientTab("Insert Patient").write()

        with self.update_tab:
            UpdatePatientTab("Update Patient").write()


# Create an instance of the app and run it
Portal().run()

# Patients Portal

## Introduction

This project is a simple patient management system implemented in Python. It provides a RESTful API to create, read, update, and delete patient records. The patient data includes fields such as name, age, gender, check-in and check-out dates, ward number, and room number.

The project is structured as follows:

- `src/`: This directory contains the main source code for the project. It includes the API controller (`api_controller.py`), the patient database (`patient_db.py`), and the patient model (`patient.py`).
- `testing-api-templates/`: This directory contains shell scripts for testing the API endpoints. It also includes JSON payloads for creating and updating patients.
- `requirements.txt`: This file lists the Python packages required to run the project.

## Prerequisites

- Install **Python** (recommended version >= 3.10)
- Install **Gitbash** (Optional)

## Installation Steps

Follow these steps to install the repository requirements:

1. **Clone the Repository:**

```bash
git clone https://github.com/amhkhowaja/patient-portal.git
```

2. **Navigate to the Repository:**
```bash
cd patient-portal
```

3. **Create a virtual environment**
```bash
python -m venv venv
```

4. **Activate the virtual environment**

*In linux*

```bash
source venv/bin/activate
```

*In windows*
```bash
source venv/Scripts/activate
```

5. **Install python packages to run the application**
```bash
python -m pip install -r requirements.txt
```

6. **For Running Flask**
```bash
python src/api_controller.py
```

7. **For Running Streamlit**
```bash
streamlit run .\src\front.py
```
## Patient API Features

The Patient API provides the following features:

- **Create Patient:** This feature allows you to create a new patient record. The API endpoint for this feature is `/patients` and the HTTP method is `POST`. You can test it out in (`testing-api-templates/create_patient.sh`).

In Terminal :

First Run the flask server by running the API_CONTROLLER (`src/api_controller.py`) directly or using linux command:
```bash
python src/api_controller.py
```
Once the Flask server is running, open a new terminal and keep the server running in the first one.

Then,
```bash
cd testing-api-templates
```

Then,
```bash
bash create_patient.sh
```

If it returns the patient_id in the response then meaning that Patient has been created successfully and added to the database.

- **Read Patient:** This feature allows you to retrieve the details of a specific patient. The API endpoint for this feature is `/patients/{id}` and the HTTP method is `GET`.


- **Update Patient:** This feature allows you to update the details of a specific patient. The API endpoint for this feature is `/patients/{id}` and the HTTP method is `PUT`.

- **Delete Patient:** This feature allows you to delete a specific patient record. The API endpoint for this feature is `/patients/{id}` and the HTTP method is `DELETE`.

- **List Patients:** This feature allows you to retrieve the list of all patients. The API endpoint for this feature is `/patients` and the HTTP method is `GET`.
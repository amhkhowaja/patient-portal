# Patients Portal

## Introduction

This project is a simple patient management system implemented in Python. It provides a RESTful API to create, read, update, and delete patient records. The patient data includes fields such as name, age, gender, check-in and check-out dates, ward number, and room number.

The project is structured as follows:

- `src/`: This directory contains the main source code for the project. It includes the API controller (`api_controller.py`), the patient database (`patient_db.py`), and the patient model (`patient.py`).
- `testing-api-templates/`: This directory contains shell scripts for testing the API endpoints. It also includes JSON payloads for creating and updating patients.
- `requirements.txt`: This file lists the Python packages required to run the project.

## Prerequisites

Install **Python** (recommended version >= 3.10)
Install **Gitbash** (Optional)

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

5. **For Running Flask**
```bash
python src/api_controller.py
```
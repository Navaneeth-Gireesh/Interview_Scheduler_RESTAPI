# Interview_Scheduler_RESTAPI


This project provides a REST API for scheduling and managing interview time slots. It allows users (e.g.,
 Interviewer and candidates) to register their availability and HR can view the schedulable time slots.

## Requirements

Before running the project, ensure the following are installed:

- Python 3.x 
- Django 5.1.3
- Any other dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Interview_Scheduler_RESTAPI.git

2. **Navigate to the project directory**:
   ```bash
    cd Interview_Scheduler_RESTAPI

3. **Create a virtual environment**:
   ```bash
    python -m venv venv
    
4. **Activate the virtual environment**:
    ```json
    # On Windows
    .\venv\Scripts\activate 

    # On MAC/Linux
    source venv/bin/activate 
    ```

5. **Install the required libraries**:
   ```bash
    pip install -r requirements.txt

## Running the Project

1. **Apply migrations**:
   ```bash
    python manage.py migrate

2. **Run the development server**:
   ```bash
    python manage.py runserver

### This will start the Django development server at http://127.0.0.1:8000/

## API Endpoints

### 1. Account Registration
- **Endpoint:**  `http://127.0.0.1:8000/account_registration`
- **Description:** This endpoint allows users to register a new account.
  
#### Request Body:
```json
{
    "username": "yourusername",
    "email": "your_email",
    "password": "yourpassword"
}
```

### 2.Accout Login:
- **Endpoint:**  `http://127.0.0.1:8000/api-auth/login/?next=/account_registration`
- **Description:** This endpoint allows users to Login to their account.
  

### 3.Availability Slot Registration:
- **Endpoint:**  `http://127.0.0.1:8000/Register_Slots/`
- **Description:** This endpoint allows users to book the slots.
  

### 4.Schedulable_Slots:
- **Endpoint:**  `http://127.0.0.1:8000/Schedulable_Slots`
- **Description:** This endpoint allows HR to view the interview schedulable time slots.

#### Request Body:
```json
{
        "candidate_id" : 4,
        "interviewer_id" : 2
}

```





## Users and Passwords

### HR
```json
username : HRADMIN
password : hradmin@1234
```
### Interviewers

```json
username : Interviewer1
password : admin@1234
```

```json
username : Interviewer2
password : admin@1234
```

### Candidates
```json
username : Candidate1
password : admin@1234
```

```json
username : Candidate2
password : admin@1234
```
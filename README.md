# Team Placeholder Big Group Project

## Team members
The members of the team are:
 - Jasmin Bedi
 - Manav Sukheja
 - Khuslen Bambar
 - Aman Hayer
 - Joshua Hodes
 - Arif Uddin
 - Chuhao (Akalay) Weng
 - Sanika Gadgil


## Project structure
This project is called Interactive Polling System. It currently consists of a single app 'polls'.

## Deployed version of the application
The deployed version of the application can be found at [enter url here].

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment. From the root of the project:

Clone the repository to your local machine:
```bash
git clone https://github.com/Arif1025/Placeholder
```

Navigate into the project directory:
```bash
cd Placeholder
```

Set up a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
- On Windows:
    ```bash
    venv\Scripts\activate
    ```
- On Mac/Linux:
    ```bash
    source venv/bin/activate
    ```


Install all required packages:
```bash
pip install -r requirements.txt
```

Migrate the database:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Seed the development database with:
```bash
python3 manage.py seeder
```

Create 2 superusers (one as a teacher, one as a student) to access the django admin interface:
```bash
python3 manage.py createsuperuser --username student_admin --email admin@example.com
python3 manage.py createsuperuser --username teacher_admin --email teacher@example.com

python3 manage.py shell
```
In the python shell, assign the 2 superusers as student or teacher
```python
from polls.models import CustomUser

# Get the superuser you just created
student_superuser = CustomUser.objects.get(username="student_admin")

# Set their role to 'student'
student_superuser.role = "student"
student_superuser.save()

print(f"Superuser {student_superuser.username} updated with role: {student_superuser.role}")

teacher_superuser = CustomUser.objects.get(username="teacher_admin")

# Set their role to 'teacher'
teacher_superuser.role = "teacher"
teacher_superuser.save()

print(f"Superuser {teacher_superuser.username} updated with role: {teacher_superuser.role}")
```

Run all tests with:
```bash
python3 manage.py test
```

Open your browser and navigate to 'http://127.0.0.1:8000' to view the project

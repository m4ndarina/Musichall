# Musichall
Musichall is a LMS (Learning Management System) designed to enhance music education through course management and interactive features, including a metronome, a guitar tuner and an interactive chord learning tool. It was built using Django (Python), HTML, CSS and JavaScript.

## How to run this program?  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/m4ndarina/Musichall.git

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt

3. Configure the database:  
   ```bash  
   python manage.py migrate 

4. Run the server:  
   ```bash  
   python manage.py runserver

5. Log in:
   Go to http://127.0.0.1:8000/login/

## Accounts:

The system supports role-based access (using Django authentication) for tutors and students, enabling course creation and assignment distribution. For testing, there are two pre-configured accounts available, one from each role. You can copy and paste it from here.

| Role    | Username     | Password         |  
|---------|--------------|------------------|  
| Tutor   | `Tutor`      | `prueba123`  |  
| Student | `Estudiante` | `prueba123`  |  

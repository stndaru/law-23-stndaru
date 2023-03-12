# Audio Central v1
#### Layanan Aplikasi & Web Project by Stefanus Ndaru W - 2006526812

## List of Functions

### [Flagship Feature] Song Randomizer

### [Flagship Feature] Song Recognizer

### Top Tracks by Region

## Application/Web Service Development Difficulties & Complexity

## Application/Web Service Usability/Urgency

## Application/Web Service Uniqueness

---

## How to run
Credit to Adrian Ardizza (Meta501)
### Locally
#### Requirements
- Python 3.10
- pipenv (install using python -m pip install pipenv)
#### Installation
- Run `pipenv install` on the project directory
- Create a new `.env` file based on `.env.example`
- Run `pipenv shell`
- Run `python manage.py runserver`
### Docker (For deployment on GCP)
#### Requirements
- Latest version of Docker
#### Installation
- Run `docker-compose up` on the project directory
- Application will deploy all necessary dependencies automatically
- If an error occurs during migration, rerun `docker-compose up`

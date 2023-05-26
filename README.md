# Car owners API

## How to run locally
- create a virtual environment based on requirements.txt file.
You can run `pip install -r requirements.txt` command at terminal
- Copy the following SECRET_KEY : 
`"django-insecure-=ok6&fsow=(^4(&&$k=45eda5%d37*!s6xf78jx9wz&&g#6h6-"` 
and paste it at `prod_settings.py` (or `dev_settings.py`) instead of 
`config("SECRET_KEY")`
- By analogy, copy the following DB_PASSWORD : `"uzRRPett4YE67WC6Bn9C"`
and paste it at `prod_settings.py` (or `dev_settings.py`) instead of 
`config("DB_PASSWORD"),`
- If you want to use development settings, go to `manage.py` file and change 
`prod_settings` to `dev_settings` at
`os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_owners.prod_settings")`
- At terminal go to Car_owners directory and run `python manage.py runserver`

## API

1. Open Swagger view with all possible endpoints and theirs descriptions:
`http://localhost:8000/`

or

2. Open API Root view based on django-rest-framework:
`http://localhost:8000/app/`

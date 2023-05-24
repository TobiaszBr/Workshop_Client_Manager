# Car owners API

## How to run locally
- create a virtual environment based on requirements.txt file
- Copy the following SECRET_KEY : 
`"django-insecure-=ok6&fsow=(^4(&&$k=45eda5%d37*!s6xf78jx9wz&&g#6h6-"` 
and paste it at settings.py instead of `config("SECRET_KEY")`
- At terminal go to Car_owners directory and run `python3 manage.py runserver`

## API

1. Open Swagger view with all possible endpoints and theirs descriptions:
`http://localhost:8000/`

or

2. Open API Root view based on django-rest-framework:
`http://localhost:8000/app/`

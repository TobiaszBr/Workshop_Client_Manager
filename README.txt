Working URLs with short description:

1. http://localhost:8000/                                    -> root screen
2. http://localhost:8000/owners/                             -> list of all owners
3. http://localhost:8000/owners/1/                           -> view of owner's details
4. http://localhost:8000/owners/search/                      -> lack of search parameters prompt view
5. http://localhost:8000/owners/search/?name=Name            -> list of all owners with name 'Name' - manage letters' size error (could be Name, name, nAmE etc)
6. http://localhost:8000/owners/search/?surname=Surname      ->  list of all owners with surname 'Surname' - manage letters' size error (could be Surname, surname,  SuRnAmE etc)
7. http://localhost:8000/owners/search/?phone=+KKYYYYYYYYY   -> one owner as a result if exists, else no owner prompt
8. http://localhost:8000/owners/search
/?phone=+KKYYYYYYYYY&surname=Surname&name=Name               -> possibility of useing all search parameters configurations -> phone&name&surname; name&surname etc...
9. http://localhost:8000/owners/name/alphabetic              ->  list of owners in name alphabetic order
10. http://localhost:8000/owners/surname/alphabetic/         ->  list of owners in surname alphabetic order

11. http://localhost:8000/cars/                              -> list of all cars
12. http://localhost:8000/cars/1/                            -> view of car's details
13. http://localhost:8000/cars/search/                       -> lack of search parameters prompt view
14. http://localhost:8000/cars/search/?brand=Brand           -> list of all cars with brand 'Brand' - manage letters' size error (could be Brand, brand, bRanD etc).
                                                                If brand contains more than one word, just use spacebar
15. http://localhost:8000/cars/search/?model=Model           -> list of all cars with model 'Model' - manage letters' size error (could be Model, model, mOdeL etc).
                                                                If model contains more than one word, just use spacebar
16. http://localhost:8000/cars/search
/?production_date=YYYY-MM-DD                                 -> list of all cars with production date YYYY-MM-DD' - manage wrong format error.
17. http://localhost:8000/owners/search
/?brand=Brand&model=Model&production_date=YYYY-MM-DD         -> possibility of useing all search parameters configurations



18. http://localhost:8000/cars/brand/alphabetic   ->  list of cars in brand alphabetic order
19. http://localhost:8000/cars/model/alphabetic/   ->  list of cars in model alphabetic order
20. http://localhost:8000/cars/production_date/ascending  ->  list of cars in production date ascending order
21. http://localhost:8000/cars/production_date/descending  ->  list of cars in production date descending order

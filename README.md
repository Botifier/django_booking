## How to start
To setup the backend you need python3 and pip and then run the following: 
<br/>
``` pip install -r requirements.txt ```
<br/>
Create the db:
<br/>
``` python manage.py migrate ```
<br/>Run the server: <br/>
``` python manage.py runserver ```
<br/>The app will run on http://localhost:8000 <br/>

## API endpoints

List bookings of a certain user:
/api/users/USER_ID/bookings <br/>

List bookings of a certain property:
/api/properties/PROPERTY_ID/bookings <br/>

## Testing
To Run the backend tests:<br/>
``` python manage.py test ```
<br/>

## TODO
- [ ] Add docker-compose for an easier setup/reusability. 
- [ ] Make a seperate app for the frontend using node .
- [ ] Seperate config for production and development for the django backend.
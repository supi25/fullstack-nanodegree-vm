from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from puppies import Base, Shelter, Puppy, Adopter, Profile

import datetime


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()



#This function will check a puppy into a Shelter
def PuppyCheckin(_name, _gender, _dateOfBirth, _picture, _shelterID, _wieght):
	shelter_capacity = session.query(Shelter.maximum_capacity).filter(Shelter.id == _shelterID).one()
	shelter_occupancy = session.query(Shelter.current_occupancy).filter(Shelter.id == _shelterID).one()
	shelter_state = session.query(Shelter.state).filter(Shelter.id == _shelterID).one()[0]
	shelter_city = session.query(Shelter.city).filter(Shelter.id == _shelterID).one()[0]
	print (shelter_state == "California")
	print shelter_city
	print (shelter_occupancy < shelter_capacity)

	if (shelter_occupancy < shelter_capacity):
		new_puppy = Puppy(name = _name, gender = _gender, date_of_birth = _dateOfBirth, picture = _picture, shelter_id = _shelterID, weight = _wieght)
		session.add(new_puppy)
		session.commit()
	else:
		close_shelter = session.query(Shelter.id).filter(Shelter.state == shelter_state).first()[0]
		print close_shelter
		
		if close_shelter:
			new_puppy = Puppy(name = _name, gender = _gender, date_of_birth = _dateOfBirth, picture = _picture, shelter_id = close_shelter, weight = _wieght)
			session.add(new_puppy)
			session.commit()
			print "Transfered to close shelter"
		else:
			print "Shelter at capacity and no close shelters"


PuppyCheckin("Ztbaa", "Male", datetime.date(2015, 11, 15), "http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct", 4, 21.1)
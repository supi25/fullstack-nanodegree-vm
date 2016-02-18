from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from puppies import Base, Shelter, Puppy, Adopter, Profile

import datetime

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

PUPsession = sessionmaker(bind=engine)

session = PUPsession()

today = datetime.date.today()
max_age = datetime.timedelta(days = 180)
min_dob = today - datetime.timedelta(days = 180)

#print today
#print max_age
#print min_dob
#print (today > min_dob)
#print (datetime.date(2015, 12, 01))

#print session.query(Puppy.name, Puppy.date_of_birth).filter(Puppy.date_of_birth > min_dob).order_by(Puppy.date_of_birth.desc()).all()
#print session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc()).all()
#print session.query(Puppy.name, Puppy.shelter_id).order_by(Puppy.shelter_id.asc()).all()
#print session.query(Puppy.name, Puppy.shelter_id).group_by(Puppy.shelter_id).all()
#print session.query(Puppy.name, Puppy.id, Puppy.shelter_id).order_by(Puppy.shelter_id.asc()).all()
print session.query(Adopter.name, Adopter.id).order_by(Adopter.name.asc()).all()

#print session.query(Shelter.name, Shelter.id, Shelter.address, Shelter.city, Shelter.state, Shelter.zip_code, Shelter.maximum_capacity, Shelter.current_occupancy).all()
#print session.query(Shelter.name, Shelter.id, Shelter.maximum_capacity, Shelter.current_occupancy).order_by(Shelter.id.asc()).all()
#print session.query(Puppy.name, Puppy.id, Puppy.adopter_id).filter(Puppy.id == 20).order_by(Puppy.name.asc()).all()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from puppies import Base, Shelter, Puppy, Adopter, Profile

import datetime


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()



#This function will check a puppy into a Shelter
def PuppyAdopt(_puppyID, _adopterIDs = []):

	#Find the occupancy of the shelter that the puppy is in
	puppy_shelter_id = session.query(Puppy.shelter_id).filter(Puppy.id == _puppyID).one()[0]
	puppy_shelter_obj = session.query(Shelter).filter(Shelter.id == puppy_shelter_id).one()

	#Reduce the current shelter occupancy by 1
	puppy_shelter_obj.current_occupancy = puppy_shelter_obj.current_occupancy-1


	adopted_puppy = session.query(Puppy).filter(Puppy.id == _puppyID).one()
	for ad_ID in _adopterIDs:
		puppy_adopter = session.query(Adopter).filter(Adopter.id == ad_ID).one()
		adopted_puppy.adopter_id.append(puppy_adopter)


	session.commit()

PuppyAdopt(20,[4,5,8])
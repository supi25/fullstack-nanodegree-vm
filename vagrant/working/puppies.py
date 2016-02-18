import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric

from sqlalchemy import Table

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()




class Shelter(Base):
	__tablename__ = 'shelter'
	name = Column(String(80), nullable = False)
	address = Column(String(250))
	city = Column(String(80), nullable = False)
	state = Column(String(80), nullable = False)
	zip_code = Column(String(80))
	website = Column(String(250))
	maximum_capacity = Column(Integer)
	current_occupancy = Column(Integer)
	id = Column(Integer, primary_key = True)



puppy_adopter = Table('puppy_association', Base.metadata, 
	Column('puppy.id', Integer, ForeignKey('puppy.id')),
	Column('adopter.id', Integer, ForeignKey('adopter.id'))
)



class Puppy(Base):
	__tablename__ = 'puppy'
	name = Column(String(80), nullable = False)
	date_of_birth = Column(Date)
	picture = Column(String)
	gender = Column(String(16))
	weight = Column(Numeric(10))
	id = Column(Integer, primary_key = True)
	adopter_id = relationship("Adopter", secondary=puppy_adopter, backref="adopter")
	profile_id = relationship("Profile", uselist=False, backref="puppy")
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)



class Profile(Base):
	__tablename__ = 'profile'
	id = Column(Integer, primary_key = True)
	url = Column(String(250))
	description = Column(String(250))
	considerations = Column(String(250))
	puppy_id = Column(Integer, ForeignKey('puppy.id'))


class Adopter(Base):
	__tablename__ = 'adopter'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)



engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
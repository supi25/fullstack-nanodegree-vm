from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

RESsession = sessionmaker(bind=engine)

session = RESsession()

restaurant_list = session.query(Restaurant.name).order_by(Restaurant.name.asc()).all()

for restaurant_data in restaurant_list:
	print restaurant_data[0]

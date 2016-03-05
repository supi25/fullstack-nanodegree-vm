from flask import Flask, render_template, url_for, request, redirect, jsonify
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
RESsession = sessionmaker(bind=engine)
session = RESsession()




#Fake Restaurants
#restaurant = {'name': 'Sandras Tea Parlor', 'id': '1'}

#restaurants = [{'name': 'Sandras Tea Parlor', 'id': '1'}, {'name': 'Ryans specialty pesto', 'id': '2'}, {'name': 'The waffle cart', 'id': '3'}]
#restaurants = []

#items = [{'name':'Earl grey', 'description':'not grey, but good', 'price':'$2.99', 'course':'Side', 'id':'1'}, {'name':'Pepermint', 'description':'Ryans favorite', 'price':'$2.50', 'course':'Side', 'id':'2'}, {'name':'Basil Pesto', 'description':'standard pesto', 'price':'$4.99', 'course':'Side', 'id':'3'}, {'name':'Cashew Pesto', 'description':'nutty', 'price':'$5.99', 'course':'Side', 'id':'4'}, {'name':'Belgian Waffle', 'description':'With real maple syrup', 'price':'$3.50', 'course':'Entree', 'id':'5'}, {'name':'Chocolate Waffle', 'description':'Covered in delicious chocolate', 'price':'$4.50', 'course':'Entree', 'id':'6'}]
#items = []

#item = {'name':'Earl grey', 'description':'not grey, but good', 'price':'$2.99', 'course':'Side', 'id':'1'}

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant)
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/JSON/')
def showRestaurantsJSON():
	restaurants = session.query(Restaurant)
	return jsonify(Restaurant =[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		newRest = Restaurant(name = request.form['name'])
		session.add(newRest)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_select>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_select):
	editRest = session.query(Restaurant).filter_by(id = restaurant_select).one()
	if request.method == 'POST':
		editRest.name = request.form['name']
		session.add(editRest)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant = editRest)

@app.route('/restaurant/<int:restaurant_select>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_select):
	deleteRest = session.query(Restaurant).filter_by(id = restaurant_select).one()
	if request.method == 'POST':
		session.delete(deleteRest)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant = deleteRest)

@app.route('/restaurant/<int:restaurant_select>/')
@app.route('/restaurant/<int:restaurant_select>/menu/')
def showMenu(restaurant_select):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_select).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_select)
	return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurant_select>/menu/JSON/')
def showMenuJSON(restaurant_select):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_select).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_select).all()
	return jsonify(MenuItems =[item.serialize for item in items])

@app.route('/restaurant/<int:restaurant_select>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_select):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_select).one()
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], course = request.form['course'], description = request.form['description'], price = request.form['price'], restaurant_id = restaurant_select)
		session.add(newItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_select = restaurant_select))
	else:
		return render_template('newMenuItem.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_select>/menu/<int:menu_select>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_select, menu_select):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_select).one()
	item = session.query(MenuItem).filter_by(restaurant_id = restaurant_select).filter_by(id = menu_select).first()
	if request.method == 'POST':
		if request.form['name']:
			item.name = request.form['name']
		if request.form['description']:
			item.description = request.form['description']
		if request.form['price']:
			item.price = request.form['price']
		if request.form['course']:
			item.course = request.form['course']
		session.add(item)
		session.commit()
		return redirect(url_for('showMenu', restaurant_select = restaurant_select))
	else:
		return render_template('editMenuItem.html', restaurant = restaurant, item = item)

@app.route('/restaurant/<int:restaurant_select>/menu/<int:menu_select>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_select, menu_select):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_select).one()
	item = session.query(MenuItem).filter_by(restaurant_id = restaurant_select).filter_by(id = menu_select).first()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		return redirect(url_for('showMenu', restaurant_select = restaurant_select))
	else:
		return render_template('deleteMenuItem.html', restaurant = restaurant, item = item)

@app.route('/restaurant/<int:restaurant_select>/menu/<int:menu_select>/JSON')
def deleteMenuItemJSON(restaurant_select, menu_select):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_select).one()
	item = session.query(MenuItem).filter_by(restaurant_id = restaurant_select).filter_by(id = menu_select).first()
	return jsonify(MenuItem =item.serialize)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
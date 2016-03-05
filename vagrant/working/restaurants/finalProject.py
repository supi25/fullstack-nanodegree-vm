from flask import Flask, render_template
app = Flask(__name__)


#Fake Restaurants
restaurant = {'name': 'Sandras Tea Parlor', 'id': '1'}

restaurants = [{'name': 'Sandras Tea Parlor', 'id': '1'}, {'name': 'Ryans specialty pesto', 'id': '2'}, {'name': 'The waffle cart', 'id': '3'}]
#restaurants = []

items = [{'name':'Earl grey', 'description':'not grey, but good', 'price':'$2.99', 'course':'Side', 'id':'1'}, {'name':'Pepermint', 'description':'Ryans favorite', 'price':'$2.50', 'course':'Side', 'id':'2'}, {'name':'Basil Pesto', 'description':'standard pesto', 'price':'$4.99', 'course':'Side', 'id':'3'}, {'name':'Cashew Pesto', 'description':'nutty', 'price':'$5.99', 'course':'Side', 'id':'4'}, {'name':'Belgian Waffle', 'description':'With real maple syrup', 'price':'$3.50', 'course':'Entree', 'id':'5'}, {'name':'Chocolate Waffle', 'description':'Covered in delicious chocolate', 'price':'$4.50', 'course':'Entree', 'id':'6'}]
#items = []

item = {'name':'Earl grey', 'description':'not grey, but good', 'price':'$2.99', 'course':'Side', 'id':'1'}

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/')
def newRestaurant():
	return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_select>/edit/')
def editRestaurant(restaurant_select):
	return render_template('editRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_select>/delete/')
def deleteRestaurant(restaurant_select):
	return render_template('deleteRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_select>/')
@app.route('/restaurant/<int:restaurant_select>/menu/')
def showMenu(restaurant_select):
	return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurant_select>/menu/new')
def newMenuItem(restaurant_select):
	return render_template('newMenuItem.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_select>/menu/<int:menu_select>/edit')
def editMenuItem(restaurant_select, menu_select):
	return render_template('editMenuItem.html', restaurant = restaurant, item = item)

@app.route('/restaurant/<int:restaurant_select>/menu/<int:menu_select>/delete')
def deleteMenuItem(restaurant_select, menu_select):
	return render_template('deleteMenuItem.html', restaurant = restaurant, item = item)



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
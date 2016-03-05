from flask import Flask
app = Flask(__name__)



@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	return "This page will show all my restaurants"

@app.route('/restaurant/new/')
def newRestaurant():
	return "This page will be for making a new restaurant"

@app.route('/restaurant/<int:restaurant_select>/edit/')
def editRestaurant(restaurant_select):
	return "This page will be for editing restaurant %s" % restaurant_select

@app.route('/restaurant/<int:restaurant_select>/delete/')
def deleteRestaurant(restaurant_select):
	return "This page will be for deleting restaurant %s" % restaurant_select

@app.route('/restaurant/<int:restaurant_select>/')
@app.route('/restaurant/<int:restaurant_select>/menu/')
def showMenu(restaurant_select):
	return "This page is the menu for restaurant %s" % restaurant_select

@app.route('/restaurant/<int:restaurant_select>/menu/new')
def newMenuItem(restaurant_select):
	return "This page is for making a new menu item for restaurant %s" % restaurant_select

@app.route('/restaurant/<int:restaurant_select>/menu/<int:menu_select>/edit')
def editMenuItem(restaurant_select, menu_select):
	return "This page is for editing menu item %s" % menu_select

@app.route('/restaurant/<int:restaurant_select>/menu/<int:menu_select>/delete')
def deleteMenuItem(restaurant_select, menu_select):
	return "This page is for deleting menu item %s" % menu_select



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
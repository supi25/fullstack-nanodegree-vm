from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
RESsession = sessionmaker(bind=engine)
session = RESsession()

#Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_select>/menu/JSON')
def restaurantMenuJSON(restaurant_select):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_select).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_select).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_select>/menu/<int:menu_select>/JSON/')
def restaurantMenuItemJSON(restaurant_select, menu_select):
	menu_item = session.query(MenuItem).filter_by(restaurant_id = restaurant_select).filter_by(id = menu_select).one()
	return jsonify(MenuItem=menu_item.serialize)

@app.route('/')
@app.route('/restaurants/<int:restaurant_select>/')
def restaurantMenu(restaurant_select):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_select).one()
	menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return render_template('menu.html', restaurant = restaurant, items = menu_items)

@app.route('/restaurants/<int:restaurant_select>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_select):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'],restaurant_id = restaurant_select)
		session.add(newItem)
		session.commit()
		flash("New menu item created!")
		return redirect(url_for('restaurantMenu', restaurant_select = restaurant_select))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_select)

@app.route('/restaurants/<int:restaurant_select>/<int:menu_select>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_select, menu_select):
	editItem = session.query(MenuItem).filter_by(id = menu_select).one()
	if request.method == 'POST':
		if request.form['name']:
			editItem.name = request.form['name']
		session.add(editItem)
		session.commit()
		flash("Menu item edited!")
		return redirect(url_for('restaurantMenu', restaurant_select = restaurant_select))
	else:
		return render_template('editmenuitem.html', restaurant_id = restaurant_select, menu_id = menu_select, edited_item = editItem)

@app.route('/restaurants/<int:restaurant_select>/<int:menu_select>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_select, menu_select):
	deleteItem = session.query(MenuItem).filter_by(id = menu_select).one()
	if request.method == 'POST':
		session.delete(deleteItem)
		session.commit()
		flash("Menu item deleted!")
		return redirect(url_for('restaurantMenu', restaurant_select = restaurant_select))
	else:
		return render_template('deletemenuitem.html', restaurant_id = restaurant_select, menu_id = menu_select, deleted_item = deleteItem)
	return "page to delete a new menu item. Task 3 complete!"

if __name__ == '__main__':
	app.secret_key = 'super_secret_key_25'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
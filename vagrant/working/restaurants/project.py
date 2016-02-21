from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
RESsession = sessionmaker(bind=engine)
session = RESsession()


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
		return redirect(url_for('restaurantMenu', restaurant_select = restaurant_select))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_select)

@app.route('/restaurants/<int:restaurant_select>/<int:menu_select>/edit/')
def editMenuItem(restaurant_select, menu_select):
	return "page to edit a new menu item. Task 2 complete!"

@app.route('/restaurants/<int:restaurant_select>/<int:menu_select>/delete/')
def deleteMenuItem(restaurant_select, menu_select):
	return "page to delete a new menu item. Task 3 complete!"

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
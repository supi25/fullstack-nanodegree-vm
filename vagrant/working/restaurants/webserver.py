from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
RESsession = sessionmaker(bind=engine)
session = RESsession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?<h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
				output += "</body></html>"

				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "&#161Hola!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?<h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
				output += "<a href = '/hello' > Back to Hello </a></body></html>"

				self.wfile.write(output)
				print output
				return


			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurant_list = session.query(Restaurant).order_by(Restaurant.name.asc()).all()

				output = ""
				output += "<html><body>"

				for restaurant_data in restaurant_list:
					output += restaurant_data.name
					output += "<br>"
					output += "<a href = '/%s/edit'> Edit </a>" % restaurant_data.id
					output += "<br>"
					output += "<a href = '/%s/delete'> Delete </a>" % restaurant_data.id
					output += "<br><br>"

				output += "<a href = '/add'> Add New Restaurant </a>"

				output += "</body></html>"

				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/add"):

				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='/add'><h2>Enter name of new restaurant<h2><input name='new_restaurant' type='text' ><input type='submit' value='Create'> </form>"
				output += "<br><br>"
				output += "<a href = '/restaurants' > Cancel </a></body></html>"
				output += "</body></html>"

				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/edit"):
				edit_id = self.path.rpartition("/")[0].partition("/")[2]
				edit_name = session.query(Restaurant.name).filter(Restaurant.id == edit_id).first()

				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='/%s/edit'><h2>%s<h2><input name='edited_restaurant' type='text' ><input type='submit' value='Edit'> </form>" % (edit_id, edit_name[0])
				output += "<br><br>"
				output += "<a href = '/restaurants' > Cancel </a></body></html>"
				output += "</body></html>"

				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/delete"):
				delete_id = self.path.rpartition("/")[0].partition("/")[2]
				delete_name = session.query(Restaurant.name).filter(Restaurant.id == delete_id).first()

				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='/%s/delete'><h2>Are you sure you want to delete %s?<h2><input name='delete_restaurant' type='submit' value='Delete'> </form>" % (delete_id, delete_name[0])
				output += "<br><br>"
				output += "<a href = '/restaurants' > Cancel </a></body></html>"
				output += "</body></html>"

				self.wfile.write(output)
				print output
				return

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				print fields

				if fields.get('message'):
					print "message"
					messagecontent = fields.get('message')

					output = ""
					output += "<html><body>"
					output += " <h2> Okay, how about this: </h2>"
					output += "<h1> %s </h1>" % messagecontent[0]

					output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?<h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
					output += "</body></html>"

					self.wfile.write(output)
					print output
					return

				if fields.get('new_restaurant'):
					print 'new_restaurant'
					inputcontent = fields.get('new_restaurant')

					new_restaurant_object = Restaurant(name = inputcontent[0])

					session.add(new_restaurant_object)
					session.commit()

					output = ""
					output += "<html><body>"
					output += "<h2> Restaurant added </h2>"
					output += "<br><br>"
					output += "<a href = '/restaurants' > Return to list </a>"
					output += "</body></html>"

					self.wfile.write(output)
					print output
					return

				if fields.get('edited_restaurant'):
					print 'edited_restaurant'
					inputcontent = fields.get('edited_restaurant')

					edit_id = self.path.rpartition("/")[0].partition("/")[2]

					editing_restaurant = session.query(Restaurant).filter(Restaurant.id == edit_id).first()
					editing_restaurant.name = inputcontent[0]

					session.commit()

					output = ""
					output += "<html><body>"
					output += "<h2> Restaurant name updated </h2>"
					output += "<br><br>"
					output += "<a href = '/restaurants' > Return to list </a>"
					output += "</body></html>"

					self.wfile.write(output)
					print output
					return

				if fields.get('delete_restaurant'):
					print 'delete_restaurant'

					delete_id = self.path.rpartition("/")[0].partition("/")[2]

					deleting_restaurant = session.query(Restaurant).filter(Restaurant.id == delete_id).first()

					session.delete(deleting_restaurant)
					session.commit()

					output = ""
					output += "<html><body>"
					output += "<h2> Restaurant deleted </h2>"
					output += "<br><br>"
					output += "<a href = '/restaurants' > Return to list </a>"
					output += "</body></html>"

					self.wfile.write(output)
					print output
					return

		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()
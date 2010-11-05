import gtk
import pygtk

class AboutDialog:
	
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file('aboutdialog.xml')

		self.dialog = self.builder.get_object('about_dialog')
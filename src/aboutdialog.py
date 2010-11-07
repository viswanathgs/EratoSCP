import gtk
import pygtk

class AboutDialog:
	
	def __init__(self):
		'''
			Constructor. Parse aboutdialog.xml using GtkBuilder and assign
			a data member to point to the about dialog.
		'''
		
		self.builder = gtk.Builder()
		self.builder.add_from_file('aboutdialog.xml')

		self.dialog = self.builder.get_object('about_dialog')
import gtk
import pygtk

class AboutDialog:

#	def on_about_dialog_close(self, data=None):
#		print 'here'
#		self.dialog.destroy()
	
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file('aboutdialog.xml')

		self.dialog = self.builder.get_object('about_dialog')
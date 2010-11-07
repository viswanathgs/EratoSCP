import gtk
import pygtk

class OptionsDialog:
	
	def run_options_dialog(self):
		'''
			Run the options dialog box and obtain the response.
			If response == OK, then, change the values of the options
			accordingly.
			Hide the dialog box.
		'''
		
		self.checkbutton_compression.set_active(self.compression)
		self.checkbutton_preserve.set_active(self.preserve)
		self.entry_limit.set_text(str(self.limit))

		response = self.dialog.run()

		if response == 1:
			self.compression = self.checkbutton_compression.get_active()
			self.preserve = self.checkbutton_preserve.get_active()
			entry_text = self.entry_limit.get_text()
		
			if entry_text.isdigit():
				self.limit = int(entry_text)
			else:
				self.limit = -1
		
		self.dialog.hide()
		
		
	def __init__(self):
		'''
			Constructor. Parse optionsdialog.xml using GtkBuilder
			and assign data members to point to its widgets.
			Initialize the values of options to default.
		'''
		
		self.builder = gtk.Builder()
		self.builder.add_from_file('optionsdialog.xml')

		self.dialog = self.builder.get_object('dialog')
		self.checkbutton_compression = self.builder.get_object('checkbutton_compression')
		self.checkbutton_preserve = self.builder.get_object('checkbutton_preserve')
		self.entry_limit = self.builder.get_object('entry_limit')

		self.compression = False
		self.preserve = False
		self.limit = -1
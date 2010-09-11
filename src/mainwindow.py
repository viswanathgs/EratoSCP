import gtk
import pygtk
import sys
import os
import validate
import filetransfer

class EratoSCP:
	
	def on_mainwindow_destroy(self, widget, data=None):
		gtk.main_quit()
			
	
	def on_button_copy_clicked(self, data=None):
#		print 'Copy button clicked'		
		self.entry_host = self.builder.get_object("entry_host")
		self.entry_port = self.builder.get_object("entry_port")
		self.entry_username = self.builder.get_object("entry_username")
		self.entry_password = self.builder.get_object("entry_password")
		
		host = self.entry_host.get_text()
		port = self.entry_port.get_text()
		username = self.entry_username.get_text()
		password = self.entry_password.get_text()
		
		(port, valid_port) = validate.validate_port(port)
		if not valid_port:
			print 'The entered port is not valid'
			return
		
		self.entry_source_path = self.builder.get_object("entry_source_path")
		self.entry_destination_path = self.builder.get_object("entry_destination_path")
		
		source_path = self.entry_source_path.get_text()
		destination_path = self.entry_destination_path.get_text()
		
		self.radio_source = self.builder.get_object("radio_source")
		source_remote = self.radio_source.get_active()
		
#		print 'host = ', host, ' port = ', port, ' username = ', username,
#		print 'password = ', password, 'source_path = ', source_path,
#		print 'destination_path = ', destination_path, 'source_remote = ', source_remote
	
#		valid_paths = validate.validate_paths(host, port, username, password, source_path, destination_path, source_remote)
#		if not valid_paths:
#			print 'The entered source/destination path is not valid'

		filetransfer.initiate_copy(host, port, username, password, source_path, destination_path, source_remote)
		
		
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file("mainwindow.xml")
		
		self.window = self.builder.get_object("mainwindow")
		self.copybutton = self.builder.get_object("button_copy")
		
		self.builder.connect_signals(self)
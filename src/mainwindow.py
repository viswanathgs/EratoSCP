import gtk
import pygtk
import sys
import os
import validate
import filetransfer

class EratoSCP:
	
	def on_mainwindow_destroy(self, widget, data=None):
		gtk.main_quit()

	def on_button_quit_erato_clicked(self, data=None):
		gtk.main_quit()

	def on_filechooserwidget_host_selection_changed(self, date=None):
		'''
			Update the host path entry box as per the changes
			in host file chooser
		'''
		
		host_uri = self.host_file_chooser.get_uri()

		if host_uri == None:
			return
		
		#To remove the preceeding file:// in host_uri
		if host_uri.find('file://') == 0:
			host_uri = host_uri[7:]
		self.entry_host_path.set_text(host_uri)
		
	def on_button_initiate_copy_clicked(self, data=None):	
		host = self.entry_host.get_text()
		port = self.entry_port.get_text()
		username = self.entry_username.get_text()
		password = self.entry_password.get_text()
		
		(port, valid_port) = validate.validate_port(port)
		if not valid_port:
			print 'The entered port is not valid'
			return
		
		host_path = self.entry_host_path.get_text()
		remote_path = self.entry_remote_path.get_text()
		source_remote = self.radio_source.get_active()

		if source_remote:
			source_path = remote_path
			destination_path = host_path
		else:
			source_path = host_path
			destination_path = remote_path
			
#		print 'host = ', host, ' port = ', port, ' username = ', username,
#		print 'password = ', password, 'source_path = ', source_path,
#		print 'destination_path = ', destination_path, 'source_remote = ', source_remote
	
#		valid_paths = validate.validate_paths(host, port, username, password, source_path, destination_path, source_remote)
#		if not valid_paths:
#			print 'The entered source/destination path is not valid'

		self.copychild = filetransfer.initiate_copy(host, port, username, password, source_path, destination_path, source_remote)
		
	def set_button_sensitivity(self, initiate_copy_button, abort_copy_button, copy_in_progress):
		initiate_copy_button.set_sensitive(copy_in_progress)
		abort_copy_button.set_sensitive(not copy_in_progress)
		
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file('mainwindow.xml')
		
		self.window = self.builder.get_object('mainwindow')

		self.entry_host = self.builder.get_object('entry_host')
		self.entry_port = self.builder.get_object('entry_port')
		self.entry_username = self.builder.get_object('entry_username')
		self.entry_password = self.builder.get_object('entry_password')

		self.entry_host_path = self.builder.get_object('entry_host_path')
		self.entry_remote_path = self.builder.get_object('entry_remote_path')
		self.radio_source = self.builder.get_object('radio_source')
		
		self.initiate_copy_button = self.builder.get_object('button_initiate_copy')
		self.abort_copy_button = self.builder.get_object('button_abort_copy')
		self.host_file_chooser = self.builder.get_object('filechooserwidget_host')

#		try:
#			copychild
#		except NameError:
#			self.set_button_sensitivity(self.initiate_copy_button, self.abort_copy_button, True)
#		else:
#			if self.copychild.isalive():
#				print 'gotcha'
#				self.set_button_sensitivity(self.initiate_copy_button, self.abort_copy_button, False)
#			else:
#				self.set_button_sensitivity(self.initiate_copy_button, self.abort_copy_button, True)
		
		self.builder.connect_signals(self)
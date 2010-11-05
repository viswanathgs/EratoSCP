import gtk
import pygtk
import sys
import os
import validate
import filetransfer
import threading
import gobject

class EratoSCP:
	
	def on_mainwindow_destroy(self, widget, data=None):
		gtk.main_quit()

	def on_button_quit_erato_clicked(self, data=None):
		gtk.main_quit()

	def on_button_abort_copy_clicked(self, date=None):
		print 'Abort copy clicked'
#		if self.filecopier.copychild != None and self.filecopier.copychild.isalive():
#			print 'Stopping copy'
#			self.filecopier.copychild.close()
		
	def on_filechooserwidget_local_selection_changed(self, date=None):
		'''
			Update the host path entry box as per the changes
			in host file chooser
		'''
		
		local_uri = self.local_file_chooser.get_uri()

		if local_uri == None:
			return
		
#		To remove the preceeding file:// in host_uri
		if local_uri.find('file://') == 0:
			local_uri = local_uri[7:]
		self.entry_local_path.set_text(local_uri)

	def on_button_initiate_copy_clicked(self, date=None):
		'''
			Calls initiate_copy() in a separate thread when "Initiate Copy" is
			clicked.
		'''
		
		self.initiate_copy_button.set_sensitive(False)
		self.initiate_copy_button.set_label("Copying...")
		self.copythread = threading.Thread(target=self.initiate_copy)
		self.copythread.start()
		
	def initiate_copy(self):	
		'''
			Checks for validity of host, port, username, password, source and
			destination paths, and then initiates copy.
			To be called in a separate thread so as to not hang GUI gtk main 
			loop.
		'''
		
		host = self.entry_host.get_text()
		port = self.entry_port.get_text()
		username = self.entry_username.get_text()
		password = self.entry_password.get_text()
		
		(port, valid_port) = validate.validate_port(port)
		if not valid_port:
			print 'Error: Invalid port'
			return
		
		local_path = self.entry_local_path.get_text()
		remote_path = self.entry_remote_path.get_text()
		source_remote = self.radio_source.get_active()

#		Removing '/' at the end of the path to avoid os.path.basename() from
#		returning empty string
		if local_path != '/' and local_path[-1] == '/':
			local_path = local_path[:-1]
		if remote_path != '/' and remote_path[-1] == '/':
			remote_path = remote_path[:-1]

		print 'Validating local path...'
		(valid_path_local, directory_local) = validate.validate_local(local_path)

		if not valid_path_local:
			print 'Error: Local path does not exist'
			return

		print 'Establishing connection and validating remote path...'
		(connection_error, valid_path_remote, directory_remote) = validate.validate_remote(remote_path, host, port, username, password)

		if connection_error:
			print 'Error: ',
			print connection_error
			return

		if not valid_path_remote:
			print 'Error: Remote path does not exist'
			return

		if source_remote:
			source_path = remote_path
			destination_path = local_path
			copy_entire_directory = directory_remote
			if not directory_local:
				print 'Error: Destination path is not a directory'
				return
		else:
			source_path = local_path
			destination_path = remote_path
			copy_entire_directory = directory_local
			if not directory_remote:
				print 'Error: Destination path is not a directory'
				return

		self.filecopier.initiate_copy(host, port, username, password, source_path, destination_path, source_remote, copy_entire_directory)
		gobject.idle_add(self.initiate_copy_button.set_label, "Initiate Copy")
		gobject.idle_add(self.initiate_copy_button.set_sensitive, True)
		
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

		self.entry_local_path = self.builder.get_object('entry_local_path')
		self.entry_remote_path = self.builder.get_object('entry_remote_path')
		self.radio_source = self.builder.get_object('radio_source')
		
		self.initiate_copy_button = self.builder.get_object('button_initiate_copy')
		self.abort_copy_button = self.builder.get_object('button_abort_copy')
		self.local_file_chooser = self.builder.get_object('filechooserwidget_local')

		self.filecopier = filetransfer.FileCopier()

		self.copythread = None
		
		self.builder.connect_signals(self)
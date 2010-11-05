import gtk
import pygtk
import sys
import os
import validate
import filetransfer
import threading
import gobject
import aboutdialog

class EratoSCP:

	def set_initiate_copy_button_sensitive(self):		
		gobject.idle_add(self.initiate_copy_button.set_label, 'Initiate Copy')
		gobject.idle_add(self.initiate_copy_button.set_sensitive, True)

	def update_status(self, status):
		gobject.idle_add(self.textbuffer_status.insert_at_cursor, status + '\n')
		
#		end_iter = self.textbuffer_status.get_end_iter()
#		gobject.idle_add(self.textbuffer_status.place_cursor, end_iter)
	
	def on_mainwindow_destroy(self, widget, data=None):
		gtk.main_quit()

	def on_button_quit_erato_clicked(self, data=None):
		gtk.main_quit()

	def on_button_about_erato_clicked(self, data=None):
		self.about_dialog = aboutdialog.AboutDialog()
		response = self.about_dialog.dialog.run()

		if response == gtk.RESPONSE_CANCEL:
			self.about_dialog.dialog.destroy()

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
			To be called in a separate thread so as to prevent GUI hangs in 
			gtk main loop.
		'''

		self.update_status('')
		self.update_status('Performing checks...')
		host = self.entry_host.get_text()
		port = self.entry_port.get_text()
		username = self.entry_username.get_text()
		password = self.entry_password.get_text()

		local_path = self.entry_local_path.get_text()
		remote_path = self.entry_remote_path.get_text()
		source_remote = self.radio_source.get_active()

		blank_entry = False
		if not host:
			self.update_status('Error: Host is not entered')
			blank_entry = True
		if not username:
			self.update_status('Error: Username is not entered')
			blank_entry = True
		if not local_path:
			self.update_status('Error: Local path is not entered')
			blank_entry = True
		if not remote_path:
			self.update_status('Error: Remote path is not entered')
			blank_entry = True

		if blank_entry:
			self.update_status('Transfer aborted.')
			self.set_initiate_copy_button_sensitive()
			return
			
		(port, valid_port) = validate.validate_port(port)
		if not valid_port:
			print 'Error: Invalid port'
			self.update_status('Error: Invalid port')
			self.update_status('Transfer aborted.')
			self.set_initiate_copy_button_sensitive()
			return

#		Removing '/' at the end of the path to avoid os.path.basename() from
#		returning empty string
		if local_path != '/' and local_path != '~/' and local_path[-1] == '/':
			local_path = local_path[:-1]
		if remote_path != '/' and remote_path != '~/' and remote_path[-1] == '/':
			remote_path = remote_path[:-1]

		print 'Validating local path...'
		self.update_status('Validating local path...')
		(valid_path_local, directory_local) = validate.validate_local(local_path)

		if not valid_path_local:
			print 'Error: Local path does not exist'
			self.update_status('Error: Local path does not exist')
			self.update_status('Transfer aborted.')
			self.set_initiate_copy_button_sensitive()
			return

		print 'Establishing connection and validating remote path...'
		self.update_status('Establishing connection and validating remote path...')
		(connection_error, valid_path_remote, directory_remote) = validate.validate_remote(remote_path, host, port, username, password)

		if connection_error:
			print 'Error: ' + str(connection_error)
			self.update_status('Error: ' + str(connection_error))
			self.update_status('Transfer aborted.')
			self.set_initiate_copy_button_sensitive()
			return

		if not valid_path_remote:
			print 'Error: Remote path does not exist'
			self.update_status('Error: Remote path does not exist')
			self.update_status('Transfer aborted.')
			self.set_initiate_copy_button_sensitive()
			return

		if source_remote:
			source_path = remote_path
			destination_path = local_path
			copy_entire_directory = directory_remote
			if not directory_local:
				print 'Error: Destination path is not a directory'
				self.update_status('Error: Destination path is not a directory')
				self.update_status('Transfer aborted.')
				self.set_initiate_copy_button_sensitive()
				return
		else:
			source_path = local_path
			destination_path = remote_path
			copy_entire_directory = directory_local
			if not directory_remote:
				print 'Error: Destination path is not a directory'
				self.update_status('Error: Destination path is not a directory')
				self.update_status('Transfer aborted.')
				self.set_initiate_copy_button_sensitive()
				return

		self.update_status('Copying files...')
		
		output = self.filecopier.initiate_copy(host, port, username, password, source_path, destination_path, source_remote, copy_entire_directory)
		
		self.update_status('Output:')
		self.update_status(output)
		self.update_status('Transfer Complete.')
		print output

		self.set_initiate_copy_button_sensitive()
		
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
		self.textview_status = self.builder.get_object('textview_status')
		self.textbuffer_status = self.builder.get_object('textbuffer_status')

		self.filecopier = filetransfer.FileCopier()

		self.copythread = None
		self.about_dialog = None
		
		self.builder.connect_signals(self)
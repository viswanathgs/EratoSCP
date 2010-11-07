import gtk
import pygtk
import pexpect
import gio
import commands
import gobject

class RemoteMounter:

	def login_remote(self, host, port, username, password):
		'''
			Mount the remote file system and update the remote file
			chooser to the corresponding location.
			Any remote filesystem, previously mounted by the application,
			is first unmounted.
		'''
		
		if self.is_mounted:
			self.unmount_remote()

		self.mount_remote(host, port, username, password)

		remote_uri = 'file:///home/' + self.local_username + '/.gvfs/'
		self.remote_file_chooser.set_current_folder_uri(remote_uri)
#		gobject.idle_add(self.remote_file_chooser.set_uri, remote_uri)

	def unmount_remote(self):
		'''
			Unmount a previously mounted remote file system.
			Also, set the remote file chooser widget insensitive.
		'''
		
		if self.is_mounted:
			(status, output) = commands.getstatusoutput('gvfs-mount -u sftp://' + self.last_mount)
			self.is_mounted = False
		gobject.idle_add(self.remote_file_chooser.set_sensitive, False)

	def already_mounted(self, host, username):
		'''
			Return True if the remote filesystem has already been mounted, 
			else return False.
		'''
		
		(status, output) = commands.getstatusoutput('ls /home/' + self.local_username + '/.gvfs/')
		if output.find('sftp for ' + username + ' on ' + host) != -1:
			return True
		return False
		
	def mount_remote(self, host, port, username, password):
		'''
			Mount the remote filesystem if it is not mounted already.
			Also, set the remote file chooser widget sensitive.
		'''
		
		if port == '':
			port = 22
		remote = username + '@' + host + ':' + str(port)

		if not self.already_mounted(host, username):
			child = pexpect.spawn('gvfs-mount sftp://' + remote)
			child.expect('Password:\s*')
			child.sendline(password)
			child.expect(pexpect.EOF)

		self.is_mounted = True
		self.last_mount = remote
		gobject.idle_add(self.remote_file_chooser.set_sensitive, True)
		
	def __init__(self, remote_file_chooser):
		'''
			Constructor. Assign a data member of point to the remote
			file chooser widget. 
			Initialize data members related to previous mounts 
			to their defaults.
			Obtain the name of the local user.
		'''
		
		self.remote_file_chooser = remote_file_chooser
		self.is_mounted = False
		self.last_mount = ''
		(status, self.local_username) = commands.getstatusoutput('whoami')
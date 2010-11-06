import gtk
import pygtk
import pexpect
import gio
import commands
import gobject

class RemoteMounter:

	def login_remote(self, host, port, username, password):
		if self.is_mounted:
			self.unmount_remote()

		(status, local_username) = commands.getstatusoutput('whoami')
		self.mount_remote(host, port, username, password)

		remote_uri = 'file:///home/' + local_username + '/.gvfs/sftp\ for\ ' + username + '\ on\ ' + host + '/home/' + username
		gobject.idle_add(self.remote_file_chooser.set_current_folder_uri, remote_uri)

	def unmount_remote(self):
		if self.is_mounted:
			(status, output) = commands.getstatusoutput('gvfs-mount -u sftp://' + self.last_mount)
			self.is_mounted = False
		gobject.idle_add(self.remote_file_chooser.set_sensitive, False)
		
	def mount_remote(self, host, port, username, password):
		if port == '':
			port = 22
		remote = username + '@' + host + ':' + str(port)
		child = pexpect.spawn('gvfs-mount sftp://' + remote)
		child.expect('Password:\s*')
		child.sendline(password)
		child.expect(pexpect.EOF)

		self.is_mounted = True
		self.last_mount = remote
		gobject.idle_add(self.remote_file_chooser.set_sensitive, True)
		
	def __init__(self, remote_file_chooser):
		self.remote_file_chooser = remote_file_chooser
		self.is_mounted = False
		self.last_mount = ''
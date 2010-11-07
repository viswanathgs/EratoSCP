import subprocess
import commands
import pexpect
import os
import validate

class FileCopier:
	
	def initiate_copy(self, host, port, username, password, source_path, destination_path, source_remote, copy_entire_directory, compression, preserve, limit):
		'''
			Perform the actual file transfer.
			Construct the scp command from the username, host, source path,
			destination path and the options.
			Spawn a pexpect child process for scp without any timeout.
		'''
		
		login = username + '@' + host + ':'
		source = source_path
		destination = destination_path
	
		if source_remote:
			source = login + source
		else:
			destination = login + destination

		options = ''

		if port != 22:
			options += '-P 22 '
		if copy_entire_directory:
			options += '-r '
		if compression:
			options += '-C '
		if preserve:
			options += '-p '
		if int(limit) != -1:
			options += '-l ' + str(limit) + ' '
		
##		Running scp command with subprocess module

#		scp_command = ['scp', '-P', str(port), source, destination]
#		print 'Executing "', ' '.join(scp_command), '"'
#		scp_proc = subprocess.Popen(scp_command)
	
##		Running scp command with pexpect module

		scp_command = 'scp ' + options + ' ' + source + ' ' + destination
		print 'Executing "' + scp_command + '"'
	
		self.copychild = pexpect.spawn(scp_command)
		index = self.copychild.expect(['Are you sure you want to continue connecting (yes/no)?\s*', '.*[pP]assword:\s*'])
		if index == 0:
			self.copychild.sendline('yes')
			self.copychild.expect('.*[pP]assword:\s*')
			self.copychild.sendline(password)
		else:
			self.copychild.sendline(password)

		self.copychild.expect(pexpect.EOF, timeout=None)
		return self.copychild.before

	def __init__(self):
		'''
			Constructor. Initialize the child process data member to None.
		'''
		
		self.copychild = None
	
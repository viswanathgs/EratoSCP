import subprocess
import commands
import pexpect
import os
import validate

class FileCopier:
	
	def initiate_copy(self, host, port, username, password, source_path, destination_path, source_remote, copy_entire_directory):
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
			
##		Running scp command with subprocess module

#		scp_command = ['scp', '-P', str(port), source, destination]
#		print 'Executing "', ' '.join(scp_command), '"'
#		scp_proc = subprocess.Popen(scp_command)

##		Running scp command with commands module

#		scp_command = 'scp -P ' + str(port) + ' ' + source + ' ' + destination
#		print 'Executing "', scp_command, '"'
#		(status, output) = commands.getstatusoutput(scp_command)

#		if status:
#			print 'Error copying file.'
#		else:
#			print 'Transfer complete.'
#			print output
	
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
		self.copychild = None
	
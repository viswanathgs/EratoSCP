import subprocess
import commands
import pexpect
import os
import validate

def initiate_copy(host, port, username, password, source_path, destination_path, source_remote):
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

	if validate.is_directory(source_path):
		options += '-r '
##	Running scp command with subprocess module

#	scp_command = ['scp', '-P', str(port), source, destination]
#	print 'Executing "', ' '.join(scp_command), '"'
#	scp_proc = subprocess.Popen(scp_command)

##	Running scp command with commands module

#	scp_command = 'scp -P ' + str(port) + ' ' + source + ' ' + destination
#	print 'Executing "', scp_command, '"'
#	(status, output) = commands.getstatusoutput(scp_command)
	
#	if status:
#		print 'Error copying file.'
#	else:
#		print 'Transfer complete.'
#		print output

##	Running scp command with pexpect module

	scp_command = 'scp ' + options + ' ' + source + ' ' + destination
	print 'Executing "' + scp_command + '"'
	
	copychild = pexpect.spawn(scp_command)
	copychild.expect(['.*[pP]assword:\s*', pexpect.EOF])
	copychild.sendline(password)
	copychild.expect(pexpect.EOF)

	return copychild
	
import subprocess
import commands

def initiate_copy(host, port, username, password, source_path, destination_path, source_remote):
	login = username + '@' + host + ':'
	source = source_path
	destination = destination_path
	
	if source_remote:
		source = login + source
	else:
		destination = login + destination
		
#	scp_command = ['scp', '-P', str(port), source, destination]
#	print 'Executing "', ' '.join(scp_command), '"'
#	scp_proc = subprocess.Popen(scp_command)

	scp_command = 'scp -P ' + str(port) + ' ' + source + ' ' + destination
	print 'Executing "', scp_command, '"'
	(status, output) = commands.getstatusoutput(scp_command)
	
	if status:
		print 'Error copying file.'
	else:
		print 'Transfer complete.'
		print output
import os
import subprocess
import commands

def validate_port(port):
	valid_port = True
	if port == '':
		port = 22	
	elif not port.isdigit():
		valid_port = False
	else:
		port = int(port)
	return (port, valid_port)
		
'''
def validate_paths(host, port, username, password, source_path, destination_path, source_remote):
	valid_paths = True
	
	if source_remote:
	else:
		source = os.path.abspath(source_path)
		if not os.path.exists(source):
			valid_paths = False
		
'''

def is_directory(path):
	'''
		Given a path, returns True if it points to a directory and False 
		if it points to a file.
		Done by checking for '-' or 'd' in the long list by executing 
		ls -l.
	'''
	
	path_dirname = os.path.dirname(path)
	path_basename = os.path.basename(path)

	(status, output) = commands.getstatusoutput('ls -l ' + path_dirname)
	longlist = output.split('\n')
	longlist = longlist[1:]

	valid = False
	directory = False

	for line in longlist:
		linelist = line.split()
		if linelist[-1] == path_basename:
			valid = True
			if linelist[0][0] == '-':
				directory = False
			elif linelist[0][0] == 'd':
				directory = True
			break

	if not valid:
		print 'Error: Path could not be categorized'
		return

	return directory
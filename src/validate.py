import os
import subprocess

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
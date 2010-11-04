import os
import subprocess
import commands
import paramiko

def validate_port(port):
	'''
		Returns (True, port number in int) if the entered port is valid.
	'''
	
	valid_port = True
	if port == '':
		port = 22	
	elif not port.isdigit():
		valid_port = False
	else:
		port = int(port)
	return (port, valid_port)
		
def validate_local(path):
	'''
		Returns a tuple (valid_path, directory).
		valid_path = True, if the local path exists.
		directory = True, if the path is a directory.
	'''

	if path == '/':
		return (True, True)
	
	(status, output) = commands.getstatusoutput('ls ' + path)
	longlist = output.splitlines()

	valid_path = True
	directory = False
	if len(longlist) > 0 and longlist[0].find('No such file or directory') != -1:
		valid_path = False
		return (valid_path, False)

	path_dirname = os.path.dirname(path)
	path_basename = os.path.basename(path)
	
	(status, output) = commands.getstatusoutput('ls -l ' + path_dirname)
	longlist = output.splitlines()
	longlist = longlist[1:]

	for line in longlist:
		linelist = line.split()
		if linelist[-1] == path_basename:
			if linelist[0][0] == '-':
				directory = False
			elif linelist[0][0] == 'd':
				directory = True
			break

	return (valid_path, directory)

def validate_remote(path, host, port, username, password):
	'''
		Returns a tuple(connection_error, valid_path, directory).
		connection_error = '', if ssh connection is successfully established.
		connection_error = <Error Message>, if connection could not be established.
		valid_path = True, if the remote path exists.
		directory = True, if the path is a directory.
	'''
	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	connection_error = ''
	valid_path = True
	directory = False
	
	try:
		ssh.connect(host, port=int(port), username=username, password=password)
	except Exception as msg:
		connection_error = msg
		return (connection_error, False, False)

	if path == '/':
		return (connection_error, True, True)
	
	(stdin, stdout, stderr) = ssh.exec_command('ls ' + path)
	longlist = stderr.read().splitlines()

	if len(longlist) > 0 and longlist[0].find('No such file or directory') != -1:
		valid_path = False
		return (connection_error, valid_path, False)

	path_dirname = os.path.dirname(path)
	path_basename = os.path.basename(path)

	(stdin, stdout, stderr) = ssh.exec_command('ls -l ' + path_dirname)
	longlist = stdout.read().splitlines()
	longlist = longlist[1:]

	for line in longlist:
		linelist = line.split()
		if linelist[-1] == path_basename:
			if linelist[0][0] == '-':
				directory = False
			elif linelist[0][0] == 'd':
				directory = True
			break

	return (connection_error, valid_path, directory)
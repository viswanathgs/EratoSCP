import os
import subprocess
import commands
import paramiko

def validate_port(port):
	valid_port = True
	if port == '':
		port = 22	
	elif not port.isdigit():
		valid_port = False
	else:
		port = int(port)
	return (port, valid_port)
		
def is_valid_path(path, remote, host, port, username, password):
	'''
		Given a path, returs True is the path if valid and False if
		no such file or directory exists
	'''

	if remote:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, port=int(port), username=username, password=password)
		(stdin, stdout, stderr) = ssh.exec_command('ls ' + path)
		longlist = stderr.read().splitlines()
	else:
		(status, output) = commands.getstatusoutput('ls ' + path)
		longlist = output.splitlines()

	if len(longlist) > 0 and longlist[0].find('No such file or directory') != -1:
		print 'Error ', path
		return False

	return True
		

def is_directory(path, remote, host, port, username, password):
	'''
		Given a path, returns True if it points to a directory and False 
		if it points to a file.
		Done by checking for '-' or 'd' in the long list by executing 
		ls -l.
	'''
	
	path_dirname = os.path.dirname(path)
	path_basename = os.path.basename(path)

	if remote:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, port=int(port), username=username, password=password)
		(stdin, stdout, stderr) = ssh.exec_command('ls -l ' + path_dirname)
		longlist = stdout.read().splitlines()
	else:
		(status, output) = commands.getstatusoutput('ls -l ' + path_dirname)
		longlist = output.splitlines()
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
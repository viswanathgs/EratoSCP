## Process this file with automake to produce Makefile.in
## Created by Anjuta

SUBDIRS = src 

eratoscpdocdir = ${prefix}/doc/eratoscp
eratoscpdoc_DATA = \
	README\
	COPYING\
	AUTHORS\
	ChangeLog\
	INSTALL\
	NEWS


EXTRA_DIST = $(eratoscpdoc_DATA)


# Remove doc directory on uninstall
uninstall-local:
	-rm -r $(eratoscpdocdir)

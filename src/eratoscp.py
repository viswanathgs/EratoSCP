#!/usr/bin/python -tt
#
# main.py
# Copyright (C) Viswanath S, Sriram G 2010 <viswanathgs@gmail.com, sriram137@gmail.com>
# 
# EratoSCP is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# EratoSCP is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import gtk
import pygtk
import mainwindow
import gobject

gobject.threads_init()
	
if __name__ == '__main__':
	eratoscp = mainwindow.EratoSCP()
	eratoscp.window.show()
	gtk.main()
#!/usr/bin/python3

#    flifcrush - tries to reduce FLIF files in size
#    Copyright (C) 2015  Matthias Krüger

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 1, or (at your option)
#    any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA  02110-1301 USA


import subprocess
import sys
import os

__author__ = 'Matthias "matthiaskrgr" Krüger'

# check for flif
flif_binary = ""
try:
	flif_path = os.environ['FLIF']
	if os.path.isfile(flif_path):
		flif_binary = flif_path
except KeyError: # env var not set, check if /usr/bin/flif exists
	if (flif_binary == ""):
		if (os.path.isfile("/usr/bin/flif")):
			flif_binary = "/usr/bin/flif"
		else:
			print("Error: no flif binary found, please use 'export FLIF=/path/to/flif'")
			quit()


 # check if we have an input file
try:
	INFILE=sys.argv[1]
	print(INFILE)
except IndexError:
	print("Error: no input file given.")
	quit()

size_orig = os.path.getsize(INFILE)
size_increased_times=0
_range=10
for N in list(range(_range)):
	proc = subprocess.Popen(['/home/matthias/vcs/github/FLIF/flif','-r', str(N), INFILE, '/dev/stdout'], stdout=subprocess.PIPE)
	if (N == 0): #first run, initialize
		N_best=0
		output_best = proc.stdout.read()
		size_best = sys.getsizeof(output_best)
		print("run {run}, size {size} b, better than before which was {size_orig} b ({size_change} b)".format(run=N, size=size_best, size_orig=size_orig, size_change=size_best-size_orig, minusperc="1"))
		continue

	output = proc.stdout.read()
	size = sys.getsizeof(output)


	if (size_best > size): # new file is smaller
		size_increased_times = 0
		output_best = output

		print("run {run}, size {size} b, better than {run_best} which was {size_best} b (-{size_change} b)".format(run=N, size=size, run_best=N_best, size_best=size_best, size_change=size_best-size))
		N_best = N
		size_best = size
	else:
		print("run {run}, size {size} b".format(run=N, size=size))
		size_increased_times += 1
		if (size_increased_times == 4): # if size increases 4 times in a row, break
			break; # do NOT quit, we need to write the file

# write final best file

OUTFILE="/tmp/out_final.flif"
with open(OUTFILE, "r+b") as f:
	f.write(output)
	f.close


size_flif = os.path.getsize(OUTFILE)
print("reduced from {size_orig} to {size_flif} ( {size_diff})".format(size_orig = os.path.getsize(INFILE), size_flif=size_flif, size_diff =size_flif - size_orig))

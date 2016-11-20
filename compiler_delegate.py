import EZlogger as log
from subprocess import Popen, PIPE
import os
import EZcompiler as compiler


tmp_file = "tmp/out.c"


def remove_file():
	clearcmd = "rm %s" % (tmp_file)
	log.info("Clean", "Removing Files")
	clear_proc = Popen(clearcmd, shell=True)
	clear_proc.wait()

def make_tmp():
	if not os.path.exists(tmp_file.split("/")[-2]):
		os.makedirs(tmp_file.split("/")[-2])

def run_file(out):
	if "/" not in out:
		runcmd = "./%s" % (out)
	else:
		runcmd = "%s" % (out)
	log.info("Running", runcmd)
	run_proc = Popen(runcmd, shell=True)
	run_proc.wait()

def init_all_compile():
	make_tmp()
	compiler.init_cmp()

def compile_tmp(out):
	# Compile the intermediate lang
	cmd = "gcc %s -lmpfr -lm -o %s" % (tmp_file, out)
	log.info("Compilation", cmd)
	compile_proc = Popen(cmd, shell=True)
	compile_proc.wait()

def addcode(fs):
	compiler.add_code(fs)

def compile_files(sources, out):
	init_all_compile()
	# loops through, compiling and saving
	for src in sources:
		addcode(open(src, "r").read())

	# we write C file
	outf = open(tmp_file, "w+")
	outf.write(compiler.get_c_file())
	outf.close()

	compile_tmp(out)

def compile_c_option(text, out):
	init_all_compile()
	addcode(text)
	outf = open(tmp_file, "w+")
	outf.write(compiler.get_c_file())
	outf.close()
	compile_tmp(out)
	


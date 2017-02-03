from subprocess import Popen, PIPE

import os

from parsing import parser
from ezlogging import log
import ezdata

args = None
has_dogfood = False

def init(_args):
	"""
	Initializes the required libraries for tasks 

	"""
	global args
	args = _args

	if not os.path.isfile(ezdata.EZC_STATIC_LIB) and not args["genstaticlib"]:
		gen_static_lib()

def get_live_static_hash():
	to_hash = ezdata.EZC_C + ezdata.EZC_DOGFOOD + ezdata.EZC_DIR
	return str(abs(hash(to_hash)))

def get_built_static_hash():
	if os.path.exists(ezdata.EZC_STATIC_LIB_HASH):
		hfl = open(ezdata.EZC_STATIC_LIB_HASH)
		ret = hfl.read()
		hfl.close()
		return ret
	else:
		os.makedirs(os.path.dirname(filename))
		return str(-1)

def gen_static_lib():
	global args
	
	from compiling import compiler
	compiler.init()

	compiler.start = ""
	compiler.main = ""
	compiler.end = ""

	compiler.add_c_code(ezdata.EZC_C)
	compiler.add_code(ezdata.EZC_DOGFOOD)

	_cca = " -fPIC -c "

	args["ccargs"] += _cca
	
	fl = "/tmp/EZC_GSL.c"

	outf = open(fl, "w+")
	outf.write(compiler.get_c_file())
	outf.close()
	
	if not os.path.exists(os.path.dirname(ezdata.EZC_STATIC_LIB)):
		os.makedirs(os.path.dirname(ezdata.EZC_STATIC_LIB))

	compile_exec(file=fl, out=ezdata.EZC_STATIC_LIB)
	#compile_exec(fl, "./GSL.o")

	args["ccargs"] = args["ccargs"].replace(_cca, "")
	
	hashwrite = open(ezdata.EZC_STATIC_LIB_HASH, "w+")
	hashwrite.write(get_live_static_hash())
	hashwrite.close()

	compiler.reset()

def remove_file(fn):
	"""
	Removes a file
	"""
	clearcmd = "rm %s" % (fn)
	log.info("Clean", clearcmd)
	clear_proc = Popen(clearcmd, shell=True)
	clear_proc.wait()

def run_exec():
	"""
	Runs the compiled executable
	"""
	global args
	if "/" not in args["o"]:
		runcmd = "./%s %s" % (args["o"], args["args"])
	else:
		runcmd = "%s %s" % (args["o"], args["args"])
	log.info("Running", runcmd)
	run_proc = Popen(runcmd, shell=True)
	run_proc.wait()

def get_ezc_lib_args():
	if not os.path.isfile(ezdata.EZC_STATIC_LIB) or args["genstaticlib"]:
		return ""
	else:
		return ezdata.EZC_STATIC_LIB

def get_lib_args():
	"""
	Returns the c compiler's linking options for gmp and mpfr
	"""
	res = "-lm "
	if ezdata.EZC_LIB:
		res += " " + ezdata.EZC_LIB + " "
	else:
		res += " -lmpfr -lgmp"
	return res

def compile_exec(file=None, out=None):
	"""
	Compiles the executable.
	There should have already been called transpile, compile_files, or addcode
	"""
	global args
	if file is None:
		file = args["tmp"]
	if out is None:
		out = args["o"]
	_linked = ""
	for x in args["files"]:
		if x[-4:] != ".ezc":
			_linked += " {0}".format(x)
	cmd = "%s -w %s %s %s %s %s -o %s" % (args["cc"], args["ccargs"], get_ezc_lib_args(), _linked, file, get_lib_args(), out)
	log.info("Compiling", cmd)
	compile_proc = Popen(cmd, shell=True)
	compile_proc.wait()

def addcode(fs, cmp):
	"""
	Transforms EZC code into C code
	"""
	cmp.add_code(fs)

def compile_files(sources):
	"""
	A list of file names
	"""
	global args
	from compiling import compiler
	compiler.init()
	
	# loops through, compiling and saving
	for src in sources:
		if src[-4:] == ".ezc":
			addcode(open(src, "r").read(), compiler)

	# we write C file
	outf = open(args["tmp"], "w+")
	outf.write(compiler.get_c_file())
	outf.close()

	compile_exec()

def transpile(text):
	"""
	Transpiles text into C, and compiles
	"""
	global args
	from compiling import compiler
	compiler.init()

	addcode(text, compiler)
	outf = open(args["tmp"], "w+")
	outf.write(compiler.get_c_file())
	outf.close()
	compile_exec()

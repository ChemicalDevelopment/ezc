from libBasic import libBasic
from libMath import libMath
from libLoops import libLoops
import lib_linker

import EZlogger as log

from parser import parse_line, set_regex, register_var, is_literal, get_c
from shared import start, main, end, var_inits

main_code = ""

declare = "function "

user_funcs = ""

usrf = """void ___%s(%s) {
%s
}"""

def init_cmp():
	map(lib_linker.register_lib, [libBasic, libMath, libLoops])
	set_regex()

def add_code(file_contents):
	global main_code
	global user_funcs
	lib_linker.reset_vars()
	lines = file_contents.split("\n")
	if declare in lines[0]:
		print lines[0]
		lines[0] = lines[0].replace(":", "")
		ctf = lines[0].replace(declare, "").split(" ")
		lines = lines[1:]
		name = ctf[0]
		args = ctf[1:]
		argss = ", mpfr_t ".join([""] + args)[2:]
		res = compile_lines(lines)
		user_funcs += usrf % (name, argss, lib_linker.get_var_inits(args) + res)
	else:
		res = compile_lines(lines)
		main_code += lib_linker.get_var_inits() + res

def compile_lines(lines):
	res = ""
	to_read = True
	c_read = True
	line_num = 0
	for line in lines:
		line_num += 1
		if is_literal(line):
			log.info("Compiling", ["Line %d" % line_num, "C Code detected", str(get_c(line))])
			res += "\n\t" + get_c(line)
		else:
			try:
				if "###" in line:
					line = line[:line.index("###")]
					to_read = not to_read
				if "#" in line:
					line = line[:line.index("#")]
				if line != "" and (to_read or c_read):
					if ":" in line:
						res += "%s" % ("\n\t".join(map(parse_line, line.split(":"))))
					else:
						res += "\n\t%s" % (parse_line(line))
				c_read = to_read
			except Exception as e:
				log.err("Compiling", ["Line %d" % line_num, "Error while parsing", line])
	return res

def get_c_file():
	return start + lib_linker.get_lib_code() + user_funcs + main + lib_linker.get_prec_init() + var_inits + main_code + end


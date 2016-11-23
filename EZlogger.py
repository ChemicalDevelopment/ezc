name = "EZCC"

version = "2.3.0"

RESET = '\033[0m'

DEFAULT = '\033[39m'
WHT = '\033[97m'
BLK = '\033[30m'

RED = '\033[31m'
LRED = '\033[91m'

GRN = '\033[32m'
LGRN = '\033[92m'

YLW = '\033[33m'
LYLW = '\033[93m'

BLU = '\033[34m'
LBLU = '\033[94m'

MAG = '\033[35m'
LMAG = '\033[95m'

CYN = '\033[36m'
LCYN = '\033[96m'

LGRA = '\033[37m'
DGRA = '\033[90m'


BOLD = '\033[1m'
DIM = '\033[2m'
UNDR = '\033[4m'
BLINK = '\033[5m'
INV = '\033[7m'
HIDE = '\033[8m'

verbosity = 0

def print_single(st, offset, c):
	print "%s%s>%s" % ("  "*(offset+1), c[0]+BOLD, RESET+c[1] + " " + st)

def base_print(col, task, st, verbose=0):
	global verbosity
	if verbose >= 0 and int(verbose) <= int(verbosity):
		if isinstance(st, list):
			for s in st:
				print_single(s, st.index(s), col)
		else:
			print_single(st, 0, col)
		print "%s" % (DEFAULT) 

def info(task, st, v=2):
    base_print((LCYN, LGRN), task, st, v)

def warn(task, st, v=1):
    base_print((LRED, YLW+BOLD), task, st, v)

def err(task, error, v=0):
    base_print((RED, YLW+UNDR), task, error, v)

def init(_verbose=0):
	global verbosity
	verbosity = _verbose
	if int(verbosity) >= 0:
		print "%s %sv%s%s: \n" % (BOLD+CYN+name, DGRA, LBLU+UNDR+version, RESET)

def end():
	if int(verbosity) >= 0:
		print "%s\n" % (DEFAULT)
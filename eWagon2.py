# Python interpreter for the eWagon2 esolang
# This is just eWagon with a deque
# Feel free to modify this file!

# IMPORTant stuff
from sys import stdout, argv
from time import sleep

# Error function
def error(text):
	print('Error:', text)
	exit()

# Class for deques
class Deque():
	def __init__(self):
		self.deque = []
	def feq(self, data):
		self.deque.insert(0, int(data))
	def fdq(self):
		return self.deque.pop(0)
	def fpeek(self):
		return self.deque[0]
	def beq(self, data):
		self.deque.append(int(data))
	def bdq(self):
		return self.deque.pop(-1)
	def bpeek(self):
		return self.deque[-1]

mq = Deque() # Main deque
aq = Deque() # Argument queue (will only use beq/fdq functions to behave as a normal queue)
ls = Deque() # Loop stack (will only use beq/bdq functions to behave as a stack)
mode = 'back'
code = ''
ip = 0 # Instruction pointer

def load(): # Load a file
	if len(argv) < 2: error('No .ew2 file specified.')
	if argv[1][-3:] != 'ew2': error('File specified is not a .ew2 file.')
	global code
	filepath = argv[1]
	c = open(filepath, 'r')
	code = c.read()

def argerror(args, cmd):
	if len(aq.deque) < args: error('Not enough arguments supplied to \"%s\".' % cmd)

# Define all the commands

def frontmode():
	global mode
	mode = 'front'

def backmode():
	global mode
	mode = 'back'

def peek():
	if mode == 'back': aq.beq(mq.bpeek())
	elif mode == 'front': aq.beq(mq.fpeek())

def pop():
	if mode == 'back': aq.beq(mq.bdq())
	elif mode == 'front': aq.beq(mq.fdq())

def discard():
	if mode == 'back': mq.bdq()
	elif mode == 'front': mq.fdq()

def add():
	argerror(2, '+')
	if mode == 'back': mq.beq(aq.fdq() + aq.fdq())
	elif mode == 'front': mq.feq(aq.fdq() + aq.fdq())

def sub():
	argerror(2, '-')
	if mode == 'back': mq.beq(aq.fdq() - aq.fdq())
	elif mode == 'front': mq.feq(aq.fdq() - aq.fdq())
def mul():
	argerror(2, '-')
	if mode == 'back': mq.beq(aq.fdq() * aq.fdq())
	elif mode == 'front': mq.feq(aq.fdq() * aq.fdq())

def div():
	argerror(2, '-')
	if 0 in aq.deque[-1,-2]: error('Attempt to divide by zero.')
	if mode == 'back': mq.beq(aq.fdq() / aq.fdq())
	elif mode == 'front': mq.feq(aq.fdq() / aq.fdq())

def modulo():
	argerror(2, '|')
	if 0 in aq.deque[-1,-2]: error('Attempt to modulo by zero.')
	if mode == 'back': mq.beq(aq.fdq() % aq.fdq())
	elif mode == 'front': mq.feq(aq.fdq() % aq.fdq())

def equal():
	argerror(2, '=')
	if mode == 'back':
		if aq.fdq() == aq.fdq(): mq.beq(1)
		else: mq.beq(0)
	elif mode == 'front':
		if aq.fdq() == aq.fdq(): mq.feq(1)
		else: mq.feq(0)

def inequal():
	argerror(2, '_')
	if mode == 'back':
		if aq.fdq() != aq.fdq(): mq.beq(1)
		else: mq.beq(0)
	elif mode == 'front':
		if aq.fdq() != aq.fdq(): mq.feq(1)
		else: mq.feq(0)

def greater():
	argerror(2, '>')
	if mode == 'back':
		if aq.fdq() > aq.fdq(): mq.beq(1)
		else: mq.beq(0)
	elif mode == 'front':
		if aq.fdq() > aq.fdq(): mq.feq(1)
		else: mq.feq(0)

def less():
	argerror(2, '<')
	if mode == 'back':
		if aq.fdq() < aq.fdq(): mq.beq(1)
		else: mq.beq(0)
	elif mode == 'front':
		if aq.fdq() < aq.fdq(): mq.feq(1)
		else: mq.feq(0)

def printnum():
	argerror(1, '$')
	print(aq.fdq())

def shownum():
	argerror(1, '#')
	stdout.write(aq.fdq())

def printchar():
	argerror(1, '@')
	print(chr(aq.fdq()))

def showchar():
	argerror(1, '!')
	stdout.write(chr(aq.fdq()))

def numinput():
	num = input()
	if not num.isdigit(): error('Attempt to provide string as input')
	if mode == 'back': mq.beq(num)
	elif mode == 'front': mq.feq(num)

def interpret():
	global ip
	while 1:
		# print(':', code[ip], ip, mq.deque, aq.deque, mode) # Prints some debug info
		# Commands/features that depend on the instruction pointer
		# Numbers
		if code[ip] == '\'':
			num = ''
			ip += 1
			while 1:
				if code[ip] == '\'': break
				num += code[ip]
				ip += 1
			if mode == 'back': mq.beq(num)
			elif mode == 'front': mq.feq(num)
		# Strings
		elif code[ip] == '"':
			ip += 1
			while 1:
				if code[ip] == '"': break
				if mode == 'back': mq.beq(ord(code[ip]))
				elif mode == 'front': mq.feq(ord(code[ip]))
				ip += 1
		# Loops
		elif code[ip] == '{': ls.beq(ip)
		elif code[ip] == '}':
			if aq.fdq() == 1:
				ip = ls.bpeek()
			else:
				ls.bdq()
		# If-statements
		elif code[ip] == '[':
			if not aq.fdq():
				while 1:
					if code[ip] == ']': break
					ip += 1
		
		# Commands for which I defined functions
		elif code[ip] == '~': frontmode()
		elif code[ip] == '`': backmode()
		elif code[ip] == '%': peek()
		elif code[ip] == '^': pop()
		elif code[ip] == ',': discard()
		elif code[ip] == '+': add()
		elif code[ip] == '-': sub()
		elif code[ip] == '*': mul()
		elif code[ip] == '/': div()
		elif code[ip] == '=': equal()
		elif code[ip] == '_': inequal()
		elif code[ip] == '>': greater()
		elif code[ip] == '<': less()
		elif code[ip] == '$': printnum()
		elif code[ip] == '#': shownum()
		elif code[ip] == '@': printchar()
		elif code[ip] == '!': showchar()
		elif code[ip] == '&': numinput()
		elif code[ip] == '.': exit()
		ip += 1
#		sleep(0.1) # Delay

load()
# Run!
interpret()

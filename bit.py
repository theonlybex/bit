# Made by Bekzhan Abdimanapov 
import sys
# Token types
#
# EOF (end-of-file)
mapping = {}
delete = 0
INTEGER       = 'INTEGER'
DIV           = 'DIV'
MUL           = 'MUL'
PLUS          = 'PLUS'
MINUS         = 'MINUS'
MUL           = 'MUL'
LPAREN        = 'LPAREN'
RPAREN        = 'RPAREN'
ID            = 'ID'
ASSIGN        = 'ASSIGN'
SEMI          = 'SEMI'
COLON         = 'COLON'
COMMA         = 'COMMA'
EOF           = 'EOF'


class Token(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value
		

	def __str__(self):
		print('Token({type}, {value})'.format( type=type, value=value))
		return 'Token({type}, {value})'.format(
			type=self.type,
			value=repr(self.value)
		)

	def __repr__(self):
		return self.__str__()


RESERVED_KEYWORDS = {
	'if': Token('keyword', 'if'),
	'then': Token('keyword', 'then'),
	'else': Token('keyword', 'else'),
	'endif': Token('keyword', 'endif'),
	'while': Token('keyword', 'while'),
	'do': Token('keyword', 'do'),
	'endwhile': Token('keyword', 'endwhile'),
	'skip': Token('keyword', 'skip'),
	
}

# # # # # #
# Scanner #
# # # # # #

class Scanner(object):
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.current_char = self.text[self.pos]
		
		
	def error(self):
		raise Exception('Invalid character')

	def move(self):
		self.pos += 1
		if self.pos > len(self.text) - 1:
			self.current_char = None  # Indicates end of input
		else:
			self.current_char = self.text[self.pos]

	def next(self):
		next_pos = self.pos + 1
		if next_pos > len(self.text) - 1:
			return None
		else:
			return self.text[next_pos]

	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.move()

	def skip_comment(self):
		while self.current_char != '}':
			self.move()
		self.move()  # the closing curly brace

	def number(self):
		"""Return a (multidigit) integer"""
		result = ''
		while self.current_char is not None and self.current_char.isdigit():
			result += self.current_char
			self.move()
		print('INTEGER',result)
		return int(result)

	def _id(self):
		"""Handle identifiers and reserved keywords"""
		result = ''
		while self.current_char is not None and self.current_char.isalnum():
			result += self.current_char
			self.move()
		return result
		

		
	def get_next_token(self):

		while self.current_char is not None:

			if self.current_char.isspace():
				self.skip_whitespace()
				continue

			if self.current_char == '{':
				self.move()
				self.skip_comment()
				continue

			if self.current_char.isalpha():
				result = self._id()
				
				if result in RESERVED_KEYWORDS:
						token = Token('RESERVED_KEYWORDS', result)
				else:
						token = Token(ID, result)
				
				print(token.type,token.value)
				return token

			if self.current_char.isdigit():
				return Token(INTEGER, self.number())

			if self.current_char == ':' and self.next() == '=':
				self.move()
				self.move()
				token = Token(ASSIGN, ':=')
				print(token.type,token.value)
				return token

			if self.current_char == ';':
				self.move()
				token = Token(SEMI, ';')
				print(token.type,token.value)
				return token

			if self.current_char == ':':
				self.move()
				token = Token(COLON, ':')
				print(token.type,token.value)
				return token

			if self.current_char == ',':
				self.move()
				token =  Token(COMMA, ',')
				print(token.type,token.value)
				return token

			if self.current_char == '+':
				self.move()
				token =  Token(PLUS, '+')
				print(token.type,token.value)
				return token

			if self.current_char == '-':
				self.move()
				token =  Token(MINUS, '-')
				print(token.type,token.value)
				return token

			if self.current_char == '*':
				self.move()
				token =  Token(MUL, '*')
				print(token.type,token.value)
				return token

			if self.current_char == '(':
				self.move()
				token =  Token(LPAREN, '(')
				print(token.type,token.value)
				return token

			if self.current_char == ')':
				self.move()
				token =  Token(RPAREN, ')')
				print(token.type,token.value)
				return token

			self.error()
			
		return Token(EOF, None)
		
		
# # # # # #
# Parser  #
# # # # # #
	
class tree:
	def __init__(self,left,data,right,middle):
		self.left = left
		self.middle = middle
		self.right = right
		self.data = data 
		
	def typeNode(var):
		if var.data in RESERVED_KEYWORDS:
			return 'RESERVED_KEYWORDS'

		elif var.data in ('+','-','*','/','(',')',':=',';'):
			return 'PUNCTUATION'
			
		try:
			val = int(var.data)
			return 'INTEGER'
		except ValueError:
			None
			
		try:
			isinstance(var.data, str)
			return 'IDENTIFIER'
		except ValueError:
			None
			
		else:
			return 'NONTYPE'
		
	def printTree(self,anum):
		for i in range(anum):
			print(" ",end = " ")
			outa.write(" ")
			
		print(self.typeNode(),self.data),	
		thistuple = (str(self.typeNode()),str(self.data))
		outa.write(thistuple[0]+" "+thistuple[1]+"\n")
		
		for key, val in mapping.items():
			outa.write([key, val])

		
		if self.left is not None:
			self.left.printTree(anum+5)
			
		if self.middle is not None:
			self.middle.printTree(anum+5)
			
		if self.right is not None:
			self.right.printTree(anum+5)
			

			
	
			


class Parser(object):
		def __init__(self, scanner):
			self.scanner = scanner
			self.current_token = self.scanner.get_next_token()

		def error(self):
			raise Exception('Invalid syntax')
		
		def eat(self, token_type):
			if self.current_token.type == token_type:
					self.current_token = self.scanner.get_next_token()
			else:
				self.error()
			
		def statement(self):
				"""
				statement : basestatement {;basestatement}
				"""
				left = self.basestatement()
				if self.current_token.value != ';':
					return left
				
				while self.current_token.value == ';':
					
					token = self.current_token.value
					self.current_token.type = SEMI
					self.eat(SEMI)
					treenode = tree(left,token,self.basestatement(), None)
					left = treenode
				return treenode
					
			
		def basestatement(self):
			"""basestatement : assignment | ifstatement | whilestatement | skip"""
				
			if self.current_token.value == 'while':
				node = self.whilestatement()
				
			elif self.current_token.value == 'if':
				node = self.ifstatement()
				
			elif self.current_token.value == 'skip':
				node = self.skip()
			
			elif self.current_token.value.isalpha():
				node = self.assignment()
			
			else:
				self.error()
				
			return node
				
		def skip(self):
			"""An skip production"""
			self.current_token.type = 'RESERVED_KEYWORDS'
			self.eat('RESERVED_KEYWORDS')
			return tree(None,'skip',None,None)
			
			
		def ifstatement(self):
			left = tree(None,self.current_token.value,None,None)
			
			if self.current_token.value == 'if':
				self.current_token.type = RESERVED_KEYWORDS
				self.eat(RESERVED_KEYWORDS)
				ifnode = self.expr()
				if self.current_token.value == 'then':
					self.current_token.type = RESERVED_KEYWORDS
					self.eat(RESERVED_KEYWORDS)
					thennode = self.statement()
					if self.current_token.value == 'else':
						self.current_token.type = RESERVED_KEYWORDS
						self.eat(RESERVED_KEYWORDS)
						elsenode = self.statement()
						if self.current_token.value == 'endif':
							endifnode = tree(ifnode,'if',thennode,elsenode)
							return endifnode
			else:
				self.error()
				
		def whilestatement(self):
			left = tree(None,self.current_token.value,None,None)
			
			if self.current_token.value == 'while':
				self.current_token.type = RESERVED_KEYWORDS
				self.eat(RESERVED_KEYWORDS)
				whilenode = self.expr()
				if self.current_token.value == 'do':
					self.current_token.type = RESERVED_KEYWORDS
					self.eat(RESERVED_KEYWORDS)
					donode = self.statement()
					if self.current_token.value == 'endwhile':
						treenode = tree(whilenode, 'while', donode, None)
						return treenode
			else:
				self.error()
				
				
		def assignment(self):
			"""
			assignment : ID ASSIGN expr
			"""
			
			left = tree(None,self.current_token.value,None,None)
			
			if self.current_token.type == ID:
				self.eat(ID)
				if self.current_token.type == ASSIGN:
					self.eat(ASSIGN)
					right = self.expr()
					node = tree(left, ':=', right,None)
					return node
				else:
					self.error()
			else:
				self.error()



		def expr(self):
			"""
			expr : term { +term }
			"""
			
			node = self.term()
			
			while self.current_token.type == PLUS:
				token = self.current_token.value
				self.eat(PLUS)
				node = tree(node, token, self.term(),None)
	
			return node

		def term(self):
			"""
			term : factor { -factor }
			"""
			
			node = self.factor()
			
			while self.current_token.type == MINUS:
				token = self.current_token.value
				self.eat(MINUS)
				node = tree(node, token, self.factor(),None)
				
			return node
			
		def factor(self):
			"""
			factor : piece { /piece }
			"""
			
			node = self.piece()
			
			while self.current_token.type == DIV:
				token = self.current_token.value
				self.eat(DIV)
				node = tree(node, token, self.piece(),None)
				
			return node
			
		def piece(self):
			"""
			piece : element { *element }
			"""
			
			node = self.element()
			
			while self.current_token.type == MUL:
				token = self.current_token.value
				self.eat(MUL)
				node = tree(node, token, self.element(),None)
				
			return node
			
		def element(self):
			"""
			element : (expression) | NUMBER | IDENTIFIER
			"""
			token = self.current_token
			if token.type == LPAREN:
				self.eat(LPAREN)
				node = self.expr()
				self.eat(RPAREN)
				return tree('(', node, ')', None)
				
			elif token.type == INTEGER:
					self.eat(INTEGER)
					return tree(None,token.value,None,None)
		
			elif token.type == ID:
					self.eat(ID)
					
					return tree(None,token.value, None,None)
			else:
				self.error()

		def parse(self):
			node = self.statement()
			print("Parsing...\n")
			node.printTree(0)
			return node
			
# # # # # # #
# Evaluator #
# # # # # # #
		
class NodeVisitor(object):
	def visit(self, node):
		method_name = 'visit_' + type(node).__name__
		visitor = getattr(self, method_name, self.generic_visit)
		return visitor(node)

	def generic_visit(self, node):
		raise Exception('No visit_{} method'.format(type(node).__name__))
			
class Evaluator(NodeVisitor):
	def __init__(self, parser):
		self.parser = parser
	
	def del_stree(self, node):

		if node:
			self.del_stree(node.left)
			self.del_stree(node.middle)
			self.del_stree(node.right)
			node.data = None
		
	def visitAss(self, node,typ):
		if node.data==':=':
			if typ.typeNode(node.left) == 'IDENTIFIER':
				mapping[str(node.left.data)] = self.visitOP(node.right,typ)
			
	
			
	def visitIf(self, node,typ):
	
		if int(self.visitOP(node.left, typ)) > 0:	
			self.visit_tree(node.right)
			
		elif int(self.visitOP(node.left, typ)) == 0:
			self.visit_tree(node.middle)
			
		elif int(self.visitOP(node.left, typ)) < 0:
			self.visit_tree(node.middle)
		
	def visit_tree(self, node):
		typ = tree
		
		if node:
			if node.data==':=':
				self.visitAss(node,typ)
				if delete == 0:
					self.del_stree(node)
				
			elif node.data == 'if':
				self.visitIf(node,typ)
				if delete == 0:
					self.del_stree(node)
				
			elif node.data == 'while':
				self.visit_while(node, typ)
				self.del_stree(node)
				
			elif node.data == 'skip':
				self.del_stree(node)
				
				
				
			self.visit_tree(node.left)
			self.visit_tree(node.middle)
			self.visit_tree(node.right)
		
	def visitOP(self,node,object2):
		
		if object2.typeNode(node) == 'INTEGER':
			return node.data
			
		if node.data == '+':
			if node.left.data == '+':
				value = self.visitOP(node.left, object2)
				if object2.typeNode(node.right) == 'INTEGER':
					return value + int(node.right.data)
				if object2.typeNode(node.right) == 'IDETIFIER':
					return value + mapping.get(node.right.data)
					
			
					
			
					
			if object2.typeNode(node.left)== 'INTEGER' and object2.typeNode(node.right) == 'INTEGER':
				return node.left.data + node.right.data
				
			elif mapping.get(node.left.data) and object2.typeNode(node.right) == 'INTEGER':
				return mapping.get(node.left.data) + node.right.data
				
			elif object2.typeNode(node.left)== 'INTEGER' and mapping.get(node.right.data):
				return node.left.data + mapping.get(node.right.data)
				
			else:
				return mapping.get(node.left.data) + mapping.get(node.right.data)
				
		elif node.data == '-':
			if node.left.data == '-':
				value = self.visitOP(node.left, object2)
				if object2.typeNode(node.right) == 'INTEGER':
					return value - int(node.right.data)
				if object2.typeNode(node.right) == 'IDETIFIER':
					return value - mapping.get(node.right.data)	
					
			
			if object2.typeNode(node.left)== 'INTEGER' and object2.typeNode(node.right) == 'INTEGER':
				return node.left.data - node.right.data
				
			elif mapping.get(node.left.data) and object2.typeNode(node.right) == 'INTEGER':
				return mapping.get(node.left.data) - node.right.data
				
			elif object2.typeNode(node.left)== 'INTEGER' and mapping.get(node.right.data):
				return node.left.data - mapping.get(node.right.data)
				
			else:
				return mapping.get(node.left.data) - mapping.get(node.right.data)
				
		elif node.data == '*':
			if node.left.data == '*':
				value = self.visitOP(node.left, object2)
				if object2.typeNode(node.right) == 'INTEGER':
					return value * int(node.right.data)
				if object2.typeNode(node.right) == 'IDETIFIER':
					return value * mapping.get(node.right.data)

			
			if object2.typeNode(node.left)== 'INTEGER' and object2.typeNode(node.right) == 'INTEGER':
				return node.left.data * node.right.data
			
			elif mapping.get(node.left.data) and object2.typeNode(node.right) == 'INTEGER':
				return mapping.get(node.left.data) * node.right.data
				
			elif object2.typeNode(node.left)== 'INTEGER' and mapping.get(node.right.data):
				return node.left.data * mapping.get(node.right.data)
				
			else:
				return mapping.get(node.left.data) * mapping.get(node.right.data)
				
		elif node.data == '/':
			
			if object2.typeNode(node.left)== 'INTEGER' and object2.typeNode(node.right.data) == 'INTEGER':
				return node.left.data / node.right.data
				
			elif mapping.get(node.left.data) and object2.typeNode(node.right.data) == 'INTEGER':
				return mapping.get(node.left.data) / node.right.data
				
			elif object2.typeNode(node.left)== 'INTEGER' and mapping.get(node.right.data):
				return node.left.data / mapping.get(node.right.data)
				
			else:
				return mapping.get(node.left.data) / mapping.get(node.right.data)
		
	def clonetree(self,node):
		if node is None:
			return None
		
		temp = node
		temp.data = node.data
		if node.left:
			temp.left = self.clonetree(node.left)

		if node.right:
			temp.right= self.clonetree(node.right)
			
			
		if node.middle:
			temp.middle = self.clonetree(node.middle)

		return temp
	
	def visit_while(self,node,typCopy):
		global delete 
		treeCopy = self.clonetree(node.right)
		typ = tree
		delete = 0
		
		while int(self.visitOP(node.left, typ)) > 0:
			delete = 1
			self.visit_tree(treeCopy)
			
			
		if 	self.visitOP(node.left, typ)==0:
			return
		
		
	def visit_Num(self, node):
		return node.value
		
	def evaluate(self):
		tree = self.parser.parse()
		return self.visit(tree)
					
# # # # # #
# Printer #
# # # # # #

text = open(sys.argv[1], 'r').read()
out = sys.argv[2]
outa = open(out,"w")



scanner = Scanner(text)
parser = Parser(scanner)
evaluator = Evaluator(parser)
result = evaluator.evaluate()
print(mapping)



	
	

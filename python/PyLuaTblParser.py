# -*- coding: utf-8 -*-
import string

class InvalidLuaStrException(Exception):
	pass

class PyLuaTblParser:
	def __init__(self):
		self.__data = {}

	###############################for load start###################################
	def __raise_exception(self, err_msg):
		raise InvalidLuaStrException(err_msg)

	def __locate_next_token(self, s, pos):
		ch, cur_pos = self.__skip_whitespace(s, pos)
		ch, cur_pos = self.__skip_comment(s, cur_pos)
		return ch, cur_pos


	def __skip_whitespace(self, s, pos):
		##print("skip whitespace")
		cur_pos = pos
		while cur_pos <= len(s) - 1:
			ch = s[cur_pos]
			if ch.isspace():
				cur_pos = cur_pos + 1
			else:
				return ch, cur_pos
		return "", len(s)

	def __skip_comment(self, s, pos):
		cur_pos = pos
		is_comment_found = False

		if cur_pos > len(s) - 1:
			return "", len(s)

		if cur_pos <= len(s) - 5 and s[cur_pos:cur_pos+4] == "--[[":
			is_comment_found = True
			print("find --[[ comment")
			cur_pos = s.find("]]", cur_pos + 4)
			if cur_pos == -1:
				cur_pos = len(s) - 1
			else:
				cur_pos = cur_pos + 2

		elif cur_pos <= len(s) - 3 and s[cur_pos:cur_pos+2] == "--":
			is_comment_found = True
			print("find -- comment")
			cur_pos = s.find("\n", cur_pos + 2)
			if cur_pos == -1:
				cur_pos == len(s) - 1
			else:
				cur_pos = cur_pos + 1

		if is_comment_found:
			ch,cur_pos = self.__skip_whitespace(s, cur_pos)
			return self.__skip_comment(s, cur_pos)
		else:
			return s[cur_pos],cur_pos
			


	def __parse_hex(self,s,pos):
		self.__raise_exception("hex number found")

	
	def __start_digit(self, s, pos):
		print("start digit")
		'''
		if s[pos:pos+2] in ["0x","0X"]:
			return self.__parse_hex(s,pos)
		'''
		ns = pos
		cur_pos = pos
		isfloat = False

		factor = 1

		while True:
			if s[cur_pos].isdigit() or s[cur_pos] in ["-","+"]:
				cur_pos = cur_pos + 1
			elif s[cur_pos] == "." or s[cur_pos] in ["e","E"]:
				cur_pos = cur_pos + 1
				isfloat = True
			else:
				cur_pos = cur_pos - 1
				break

		if(ns == cur_pos + 1) and s[pos] == "-":
			self.__raise_exception("no number string found")
			#return None, "no number string found"

		num_str = s[ns:cur_pos + 1]
		##print(num_str, cur_pos)
		v = None
		
		if isfloat:
			try:
				v = float(num_str)*factor
			except Exception, e:
				self.__raise_exception("invalid number at " + str(pos) + num_str)
				#return None, "invalid float"
		else:
			try:
				v = int(num_str)*factor
			except Exception, e:
				self.__raise_exception("invalid number at "+ str(pos) + num_str)
				#return None, "invalid int"
		return v, cur_pos

	#从s的pos位置开始解析一个字符串
	def __start_alpha(self, s, pos):
		print("start_alpha" + str(pos))
		cur_pos = pos
		while True:
			if s[cur_pos].isalpha():
				cur_pos = cur_pos + 1
			else:
				cur_pos = cur_pos - 1
				break
		v = s[pos:cur_pos + 1]
		if v.find("\\") != -1:
			self.__raise_exception("has escape")
			#return None, "escape in alpha"
		##print v,cur_pos
		return v, cur_pos

	def __check_quote(self, s, pos):
		is_quote = True
		idx = pos - 1
		while idx > 0:
			if s[idx] == "\\":
				is_quote = not is_quote
				idx -= 1
			else:
				break
		return is_quote

	def __escape_decode(self, s):
		idx,last_idx = 0,0
		new_str_list = []

		while True:
			idx = s.find("\\", idx)
			if idx == -1 or idx == len(s)-1:
				new_str_list.append(s[last_idx:])
				break

			new_str_list.append(s[last_idx:idx])

			print "find \\ at", idx
			next_char = s[idx + 1:idx + 2]
			#\\
			if next_char == "\\":
				new_str_list.append("\\")
				last_idx = idx + 2
			#\n
			elif next_char == "n":
				new_str_list.append("\n")
				last_idx = idx + 2
			#\t
			elif next_char == "t":
				new_str_list.append("\t")
				last_idx = idx + 2
			elif next_char == "f":
				new_str_list.append("\f")
				last_idx = idx + 2
			elif next_char == "b":
				new_str_list.append("\b")
				last_idx = idx + 2
			elif next_char == "r":
				new_str_list.append("\r")
				last_idx = idx + 2
			elif next_char == "\"":
				new_str_list.append("\"")
				last_idx = idx + 2
			elif next_char == "'":
				new_str_list.append("'")
				last_idx = idx + 2
			elif next_char == "'":
				new_str_list.append("'")
				last_idx = idx + 2
			elif next_char == "/":
				new_str_list.append("/")
				last_idx = idx + 2
			else:
				print("skip /")
				last_idx = idx
			idx = idx + 2
		return "".join(new_str_list)

	def __start_quote(self, s, pos):
		cur_pos = pos + 1
		end_quote = s[pos]
		while cur_pos < len(s)-1:
			if s[cur_pos] != end_quote:
				cur_pos = cur_pos + 1
			else:
				if self.__check_quote(s, cur_pos):
					break
				else:
					cur_pos = cur_pos + 1
		v = s[pos+1:cur_pos]
		v = self.__escape_decode(v)

		return v, cur_pos

	
	def __start_square(self, s, pos):
		print("start_square")
		value = None
		ch, cur_pos = self.__locate_next_token(s, pos + 1)
		if ch == "\"" or ch == "'":
			value, cur_pos = self.__start_quote(s, cur_pos)
		elif ch.isdigit() or ch == "-":
			value, cur_pos = self.__start_digit(s, cur_pos)
		else:
			self.__raise_exception("error at pos " + str(cur_pos) + ", string or num expected")
			#return None, "error in [], string or num expected"

		if value == None and type(cur_pos) == str:
			return None,cur_pos

		ch, cur_pos = self.__locate_next_token(s, cur_pos + 1)
		if s[cur_pos] != "]":
			self.__raise_exception("error at pos " + str(cur_pos) + ", \"]\" expected")
			#return None, "error in [], ] expected"
		return value, cur_pos


	def __next_tbl_item(self, s, pos):
		print("next_tbl_item" + str(pos))
		cur_pos = pos
		key = None
		value = None
		ch = s[cur_pos]

		if ch.isdigit() or ch == "-":
			value, cur_pos = self.__start_digit(s, cur_pos)
		elif ch.isalpha():
			v, cur_pos = self.__start_alpha(s, cur_pos)

			if v == "false":
				value = False
			elif v == "true":
				value = True
			elif v == "nil":
				value = None
			else:
				key = v
				ch, cur_pos = self.__locate_next_token(s, cur_pos + 1)
				if ch != "=":
					self.__raise_exception("error, \"=\" expected at pos " + str(cur_pos))
					#return None,None,"no = found in kv pairs"
				ch, cur_pos = self.__locate_next_token(s, cur_pos + 1)
				value, cur_pos = self.__tbl_item_value(s, cur_pos)

		elif ch == "{":
			value, cur_pos = self.__parse_tbl(s, cur_pos)
		elif ch == "\"" or ch == "'":
			value, cur_pos = self.__start_quote(s, cur_pos)
		elif ch == "[":
			key, cur_pos = self.__start_square(s, cur_pos)

			if type(cur_pos) == str:
				return None,None,cur_pos

			ch, cur_pos = self.__locate_next_token(s, cur_pos + 1)
			if ch != "=":
				self.__raise_exception("error, \"=\" expected at pos " + str(cur_pos))
				#return None,None,"no = found"
			ch, cur_pos = self.__locate_next_token(s, cur_pos + 1)
			value, cur_pos = self.__tbl_item_value(s, cur_pos)

		else:
			self.__raise_exception("error in next_tbl_item at pos " + str(cur_pos))
			#return None,None,"unknown token"

		if type(cur_pos) == str:
			return None,None,cur_pos
		##print (key, value, cur_pos)
		return key, value, cur_pos

	def __tbl_item_value(self, s, pos):
		print("table_item_value")
		cur_pos = pos
		value = None
		ch = s[cur_pos]
		if ch == "{":
			value, cur_pos = self.__parse_tbl(s, cur_pos)
		elif ch.isdigit() or ch == "-":
			value, cur_pos = self.__start_digit(s, cur_pos)
		elif ch.isalpha():
			value, cur_pos = self.__start_alpha(s, cur_pos)
			if value == "false":
				value = False
			elif value == "true":
				value = True
			elif value == "nil":
				value = None

		elif ch == "\"" or ch == "'":
			value, cur_pos = self.__start_quote(s, cur_pos)
		else:
			self.__raise_exception("parse tbl value error, invalid value found")

		return value, cur_pos

	def __parse_tbl(self, s, pos):
		##print("parse_tbl")
		cur_pos = pos
		head = s[cur_pos]

		none_key_values = []
		kv_pairs = {}

		if head != "{":
			self.__raise_exception("error, tbl head error, at pos " + str(pos))
			#return None,"tbl head error"

		while True:
			##print (cur_pos)
			ch, cur_pos = self.__locate_next_token(s, cur_pos + 1)
			##print("in while, ch is "+ch+", at pos "+str(cur_pos))
			if ch == "}":
				break

			key, value, cur_pos = self.__next_tbl_item(s, cur_pos)
			if type(cur_pos) == str:
				return None,cur_pos

			##print (key,value,cur_pos)
			if key == None:
				none_key_values.append(value)
			elif key != None and value != None:
				kv_pairs[key] = value

			ch, cur_pos = self.__locate_next_token(s, cur_pos + 1)
			if ch != "," and ch != ";" and ch != "}":
				self.__raise_exception("error, \",\" or \"}\" needed at pos " + str(cur_pos))
				#return None, ",}needed"
			elif ch == "}":
				cur_pos = cur_pos -1
		
		if len(none_key_values) == 0:
			return kv_pairs, cur_pos
		elif len(kv_pairs) == 0:
			return none_key_values, cur_pos
		
		'''
		d = {}
		for p in range(len(none_key_values)):
			d[p+1] = none_key_values[p]

		for k,v in kv_pairs.items():
			if d[k] == None and v != None:
				d[k] = v
		'''
		for p in range(len(none_key_values)):
			if none_key_values[p] != None:
				kv_pairs[p+1] = none_key_values[p]

		return kv_pairs, cur_pos
	###############################for load end###################################

	

	###############################for dump start###################################
	def __escape_str(self, s):
		v = s
		v = v.replace("\\", "\\\\")
		v = v.replace("\"","\\\"")
		v = v.replace("'", "\'")
		v = v.replace("\n","\\n")
		v = v.replace("\b","\\b")
		v = v.replace("\f","\\f")
		v = v.replace("\t", "\\t")
		v = v.replace("\r","\\r")
		#v = v.replace("/", "\\/")
		return v

	def __dump_v(self, v):
		v_str = ""
		if type(v) == int:
			v_str = str(v)
		elif type(v) == list:
			v_str = self.__dump_list(v)
		elif type(v) == dict:
			v_str = self.__dump_dict(v)
		elif type(v) == str:
			v_str = "\"" + self.__escape_str(v) + "\""
		elif v == False:
			v_str = "false"
		elif v == True:
			v_str = "true"
		elif v == None:
			v_str = "nil"
		else:
			v_str = str(v)
		return v_str

	def __dump_k(self, k):
		k_str = ""
		if type(k) == int:
			v_str = "[" + str(k) + "]"
		elif type(k) == str:
			v_str = "[\"" + self.__escape_str(k) + "\"]"
		else:
			v_str = "[\"" +"UNKNOWN" + "\"]"
		return v_str


	def __dump_list(self, l):
		ls = "{"
		for v in l:
			ls = ls + self.__dump_v(v) + ","
		ls = ls + "}"
		return ls

	def __dump_dict(self, d):
		ds = "{"
		for k,v in d.items():
			k_str = self.__dump_k(k)
			v_str = self.__dump_v(v)
			ds = ds + k_str + "=" + v_str + ","
		ds = ds + "}"

		return ds
	###############################for dump end###################################

	###############################for load dict start###################################
	def __cp_dict(self, d):
		dr = {}
		for k,v in d.items():
			kr = k
			vr = v
			if type(k) != int and type(k) != str:
				continue

			if type(v) == dict:
				vr = self.__cp_dict(v)
			elif type(v) == list:
				vr = self.__cp_list(v)

			dr[kr] = vr

		return dr

	def __cp_list(self, l):
		lr = []
		for v in l:
			vr = v
			if type(v) == dict:
				vr = self.__cp_dict(v)
			elif type(v) == list:
				vr = self.__cp_list(v)
			lr.append(vr)
		return lr

	def __list2dict(self, l):
		dr = {}
		for p in range(len(l)):
			dr[p+1] = l[p]
		return dr



	###############################for load dict end###################################

	def load(self, s):
		d,p = self.__parse_tbl(s, 0)
		if type(p) == str:
			self.__data = {}
			return d
		ch, pos = self.__locate_next_token(s, p+1)
		if ch != "":
			self.__raise_exception("string end expected at pos " + str(p))
		self.__data = d
		return d

	
	def dump(self):
		#print("dump")
		ds = self.__dump_v(self.__data)
		return ds

	
	def loadLuaTable(self, f):
		#print("loadLuaTable")
		fp = open(f)
		fcontent = None
		try:
			fcontent = fp.read()
		finally:
			fp.close()
		return self.load(fcontent)


	def dumpLuaTable(self, f):
		#print("dumpLuaTable")
		s = self.dump()
		fp = open(f, 'w')
		fp.write(s)
		fp.close()

    
	def loadDict(self, d):
		##print("loadDict")
		if d == None or type(d) != dict:
			return
		self.__data = self.__cp_dict(d)

	
	def dumpDict(self):
		#print("dumpDict")
		if self.__data == None:
			return None
		#return self.__cp_dict(self.__data)
		if type(self.__data) == dict:
			return self.__cp_dict(self.__data)
		elif type(self.__data) == list:
			return self.__list2dict(self.__data)

	def __getitem__(self, i):
		return self.__data[i]

	def __setitem__(self, i, v):
		self.__data[i] = v

	def update(self, d):
		dd = self.__cp_dict(d)
		d_temp = {}
		if type(self.__data) == list:
			for i in range(len(self.__data)):
				if self.__data[i] != None:
					d_temp[i + 1] = self.__data[i]
			self.__data = d_temp
		self.__data.update(dd)
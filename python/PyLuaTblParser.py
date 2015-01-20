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

	def __start_digit(self, s, pos):
		##print("start digit")
		cur_pos = pos
		isfloat = False
		while True:
			if s[cur_pos].isdigit():
				cur_pos = cur_pos + 1
			elif s[cur_pos] == ".":
				cur_pos = cur_pos + 1
				isfloat = True
			else:
				cur_pos = cur_pos - 1
				break
		num_str = s[pos:cur_pos + 1]
		##print(num_str, cur_pos)
		v = None
		if isfloat:
			v = string.atof(num_str)
		else:
			v = string.atoi(num_str)
		return v, cur_pos

	def __start_alpha(self, s, pos):
		##print("start_alpha" + str(pos))
		cur_pos = pos
		while True:
			if s[cur_pos].isalpha():
				cur_pos = cur_pos + 1
			else:
				cur_pos = cur_pos - 1
				break
		v = s[pos:cur_pos + 1]
		##print v,cur_pos
		return v, cur_pos

	def __start_quote(self, s, pos):
		##print("start quote")
		cur_pos = pos + 1
		while True:
			if s[cur_pos] != "\"":
				cur_pos = cur_pos + 1
			else:
				break
		v = s[pos+1:cur_pos]
		return v, cur_pos

	def __start_square(self, s, pos):
		##print("start_square")
		value = None
		ch, cur_pos = self.__skip_whitespace(s, pos + 1)
		if ch == "\"":
			value, cur_pos = self.__start_quote(s, cur_pos)
		elif ch.isdigit():
			value, cur_pos = self.__start_digit(s, cur_pos)
		else:
			self.__raise_exception("error at pos " + str(cur_pos) + ", string or num expected")
			return None, cur_pos


		ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
		if s[cur_pos] != "]":
			self.__raise_exception("error at pos " + str(cur_pos) + ", \"]\" expected")
			return None, cur_pos
		return value, cur_pos



	def __next_tbl_item(self, s, pos):
		##print("next_tbl_item" + str(pos))
		cur_pos = pos
		key = None
		value = None
		ch = s[cur_pos]

		if ch.isdigit():
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
				ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
				if ch != "=":
					self.__raise_exception("error, \"=\" expected at pos " + str(cur_pos))
				ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
				value, cur_pos = self.__tbl_item_value(s, cur_pos)

		elif ch == "{":
			value, cur_pos = self.__parse_tbl(s, cur_pos)
		elif ch == "\"":
			value, cur_pos = self.__start_quote(s, cur_pos)
		elif ch == "[":
			key, cur_pos = self.__start_square(s, cur_pos)

			ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
			if ch != "=":
				self.__raise_exception("error, \"=\" expected at pos " + str(cur_pos))
			ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
			value, cur_pos = self.__tbl_item_value(s, cur_pos)

		else:
			self.__raise_exception("error in next_tbl_item at pos " + str(cur_pos))

		##print (key, value, cur_pos)
		return key, value, cur_pos

	def __tbl_item_value(self, s, pos):
		cur_pos = pos
		value = None
		ch = s[cur_pos]
		if ch == "{":
			value, cur_pos = self.__parse_tbl(s, cur_pos)
		elif ch.isdigit():
			value, cur_pos = self.__start_digit(s, cur_pos)
		elif ch.isalpha():
			value, cur_pos = self.__start_alpha(s, cur_pos)
		elif ch == "\"":
			value, cur_pos = self.__start_quote(s, cur_pos)

		return value, cur_pos

	def __parse_tbl(self, s, pos):
		##print("parse_tbl")
		cur_pos = pos
		head = s[cur_pos]

		none_key_values = []
		kv_pairs = {}

		if head != "{":
			self.__raise_exception("error, tbl head error, at pos " + pos)
			return None,cur_pos

		while True:
			##print (cur_pos)
			ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
			##print("in while, ch is "+ch+", at pos "+str(cur_pos))
			if ch == "}":
				break

			key, value, cur_pos = self.__next_tbl_item(s, cur_pos)

			##print (key,value,cur_pos)
			if key == None:
				none_key_values.append(value)
			elif key != None and value != None:
				kv_pairs[key] = value

			ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
			if ch != "," and ch != ";" and ch != "}":
				self.__raise_exception("error, \",\" or \"}\" needed at pos " + str(cur_pos))
			elif ch == "}":
				cur_pos = cur_pos -1
		
		if len(kv_pairs) == 0:
			return none_key_values, cur_pos
		elif len(none_key_values) == 0:
			return kv_pairs, cur_pos

		d = {}
		for p in range(len(none_key_values)):
			d[p+1] = none_key_values[p]

		for k,v in kv_pairs.items():
			if d[k] == None and v != None:
				d[k] = v

		return d, cur_pos
	###############################for load end###################################

	

	###############################for dump start###################################

	def __dump_v(self, v):
		v_str = ""
		if type(v) == int:
			v_str = str(v)
		elif type(v) == list:
			v_str = self.__dump_list(v)
		elif type(v) == dict:
			v_str = self.__dump_dict(v)
		elif type(v) == str:
			v_str = "\"" + v + "\""
		elif v == False:
			v_str = "false"
		elif v == True:
			v_str = "true"
		elif v == None:
			v_str = "nil"
		else:
			v_str = str(v)
		
		return v_str

	def __dump_list(self, l):
		ls = "{"
		for v in l:
			ls = ls + self.__dump_v(v) + ","
		ls = ls + "}"
		return ls

	def __dump_dict(self, d):
		ds = "{"
		p = 0
		for k,v in d.items():
			k_str = ""
			if type(k) == str:
				k_str = k
			elif type(k) == int:
				k_str = "[" + str(k) + "]"
			else:
				p = p + 1
				continue

			v_str = self.__dump_v(v)
			ds = ds + k_str + "=" + v_str + ","
			p = p + 1
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

			dr[kr] = vr

		return dr
	###############################for load dict end###################################



	#读取Lua table数据，输入s为一个符合Lua table定义的字符串，无返回值；若遇到Lua table格式错误的应该抛出异常
	def load(self, s):
		##print("load")
		d,p = self.__parse_tbl(s, 0)
		ch, pos = self.__skip_whitespace(s, p+1)
		if ch != "":
			self.__raise_exception("string end expected at pos " + str(p))
		self.__data = d
		return d

	#根据类中数据返回Lua table字符串
	def dump(self):
		#print("dump")
		ds = self.__dump_v(self.__data)
		return ds


	#从文件中读取Lua table字符串，f为文件路径，异常处理同1，文件操作失败抛出异常；
	def loadLuaTable(self, f):
		#print("loadLuaTable")
		fp = open(f)
		fcontent = None
		try:
			fcontent = fp.read()
		finally:
			fp.close()
		return self.load(fcontent)

	#将类中的内容以Lua table格式存入文件，f为文件路径，文件若存在则覆盖，文件操作失败抛出异常；
	def dumpLuaTable(self, f):
		#print("dumpLuaTable")
		s = self.dump()
		fp = open(f, 'w')
		fp.write(s)
		fp.close()

    #读取dict中的数据，存入类中，只处理数字和字符串两种类型的key，其他类型的key直接忽略；
	def loadDict(self, d):
		##print("loadDict")
		self.__data = self.__cp_dict(d)

	#返回一个dict，包含类中的数据
	def dumpDict(self):
		#print("dumpDict")
		return self.__cp_dict(d)


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
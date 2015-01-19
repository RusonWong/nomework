# -*- coding: utf-8 -*- 
import sys,math


class PyLuaTblParser:
	def __init__(self):
		self._lua_str = ""
		self._cur_pos = 0


	def __skip_whitespace(self, s, pos):
		print("skip whitespace")
		cur_pos = pos
		while cur_pos < len(s) - 1:
			ch = s[cur_pos]
			if ch.isspace():
				cur_pos = cur_pos + 1
			else:
				return ch, cur_pos
		return "", len(s)

	def __start_digit(self, s, pos):
		print("start digit")

	def __start_alpha(self, s, pos):
		print("start_str")

	def __start_quote(self, s, pos):
		print("start quote")

	def __next_tbl_item(self, s, pos):
		print("next_tbl_item")
		cur_pos = pos
		key = None
		value = None
		ch = s[cur_pos]

		if ch.isdigit():
			value, cur_pos = self.__start_digit(s, cur_pos)
		elif ch.isalpha():
			value, cur_pos = self.__start_alpha(s, cur_pos)
		elif ch == "{":
			value, cur_pos = self.__parse_tbl(s, cur_pos)
		elif ch == "\"":
			key, cur_pos = self.__start_quote(s, cur_pos)

			ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
			if ch != "=":
				print("error, \"=\" expected at pos " + cur_pos)
			value, cur_pos = self.__tbl_item_value(s, pos)
			
		elif ch == "[":
			key, cur_pos = self.__start_square(s, cur_pos)

			ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
			if ch != "=":
				print("error, \"=\" expected at pos " + cur_pos)
			value, cur_pos = self.__tbl_item_value(s, pos)

		else:
			print("error in next_tbl_item at pos " + cur_pos)

		return key, value, cur_pos

	def __tbl_item_value(self, s, pos):
		ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
		if ch == "{":
			value, cur_pos = __parse_tbl(s, cur_pos)
		elif ch.isdigit():
			value, cur_pos = self.__start_digit(s, cur_pos)
		elif ch.isalpha():
			value, cur_pos = self.__start_alpha(s, cur_pos)
		elif ch == "\"":
			value, cur_pos = self.__start_quote(s, cur_pos)

		return value, cur_pos



	def __parse_tbl(self, s, pos):
		print("parse_tbl")
		cur_pos = pos
		head = s[cur_pos]

		none_key_values = []
		kv_pairs = {}

		if head != "{":
			print("error, tbl head error, at pos " + pos)
			return None,cur_pos

		while True:
			ch, cur_pos = self.__skip_whitespace(s, cur_pos + 1)
			if ch == "}":
				break

			key, value, cur_pos = self.__next_tbl_item(s, cur_pos)

			if key == None and value != None:
				none_key_values[] = value
			elif key != None and value != None:
				kv_pairs[key] = value
			else:
				print("kv null")

			ch, cur_pos = self.__skip_whitespace(s. cur_pos + 1)
			if 





	#读取Lua table数据，输入s为一个符合Lua table定义的字符串，无返回值；若遇到Lua table格式错误的应该抛出异常
	def load(self, s):
		print("load")

	#根据类中数据返回Lua table字符串
	def dump(self):
		print("dump")

	#从文件中读取Lua table字符串，f为文件路径，异常处理同1，文件操作失败抛出异常；
	def loadLuaTable(self, f):
		print("loadLuaTable")

	#将类中的内容以Lua table格式存入文件，f为文件路径，文件若存在则覆盖，文件操作失败抛出异常；
	def dumpLuaTable(self, f):
		print("dumpLuaTable")

    #读取dict中的数据，存入类中，只处理数字和字符串两种类型的key，其他类型的key直接忽略；
	def loadDict(self, d):
		print("loadDict")

	#返回一个dict，包含类中的数据
	def dumpDict(self):
		print("dumpDict")

print("ok")
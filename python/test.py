from PyLuaTblParser import PyLuaTblParser
import exceptions

a1 = PyLuaTblParser()
a2 = PyLuaTblParser()
a3 = PyLuaTblParser()


a1.loadLuaTable("p.lua")

d = a1.dumpDict()
print d


a1.dumpLuaTable("p2.lua")

a2.loadLuaTable("p2.lua")

#s = a2.dump()


#print s





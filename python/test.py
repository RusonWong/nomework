from PyLuaTblParser import PyLuaTblParser
import exceptions

a1 = PyLuaTblParser()

s = '{1;2;3,nil}'
d = a1.load(s)
print str(d)

xx = a1.dump()
print xx

t = {"name":"wangchun"}
a1.update(t)

xx = a1.dump()
print xx

a1[2] = "haha"

xx = a1.dump()
print xx

#a1.dumpLuaTable("lllll.lua")

a2 = PyLuaTblParser()
d = a2.loadLuaTable("lllll.lua")
print d
xx = a2.dump()
print xx


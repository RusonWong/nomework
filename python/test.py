from PyLuaTblParser import PyLuaTblParser
import exceptions

a1 = PyLuaTblParser()

s = '{[1] = 2;2;-3,nil}'
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

a1.dumpLuaTable("lllll.lua")

a2 = PyLuaTblParser()
d = a2.loadLuaTable("lllll.lua")
print d
xx = a2.dump()
print xx


l = [1,2,3,"hello"]

d = {"name":"ruson", "list" : l}

a3 = PyLuaTblParser()
a3.loadDict(d)

xx = a3.dump()
print xx

l[3] = "hxxxx"


xx = a3.dump()
print xx


local json = require 'json'


----[[local test_result1 = json.Marshal('{"a":1}')
--
local tbl = { b ="cd",3,9, c = {1,2,[3] = {a=1,b=true}}}--{[2]=1,[4]=1}
local test_result2 = json.Unmarshal(tbl)
print(test_result2)
print(type("2"))
--[[
i = 1


tb = {1,2,name="huhu",4,[8]=1}
for k,v in pairs(tb) do
	print(k,v)
end

function createCountDownTimer(second, duration)
	local ms = second * 1000
	local function countDown()
		ms = ms - duration
		return ms
	end
	return countDown
end

timer1 = createCountDownTimer(1,2)
for i = 1,4 do
	print(timer1())
end

timer2 = createCountDownTimer(2,20)
for i = 1,4 do
	print(timer2())
end


t = {}
m = {a = "and", b = "lilei", c = "hanmeimei"}

setmetatable(t, {__index = m})
for k,v in pairs(t) do
	print(k,v)
end

print(t.a)

function fun()
	local index = 1
	index = index + 1
	print(index)
end

for i = 1, 6 do
	fun()
end

function enum(array)
	local index = 1
	print("fun called,",index)
	return function()
		local ret = array[index]
		index = index + 1
		return ret
	end
end

num = 5
function haha()
	if num ~= 1 then
		num = num -1
		return num
	else
		return nil
	end
end


for element in haha do 
	print(element)
end
num = 10
for element in haha do 
	print(element)
end


Person={}
 
function Person:new(p)
    local obj = p
    if (obj == nil) then
        obj = {name="ChenHao", age=37, handsome=true}
    end
    self.__index = self
    return setmetatable(obj, self)
end
 
function Person:toString()
    return self.name .." : ".. self.age .." : ".. (self.handsome and "handsome" or "ugly")
end

me = Person:new()
print(me:toString())
 
kf = Person:new{name="King's fucking", age=70, handsome=false}
print(kf:toString())


Student = Person:new()
 
function Student:new()
    newObj = {year = 2013}
    self.__index = self
    return setmetatable(newObj, self)
end
 
function Student:toString()
    return "Student : ".. self.year.." : " .. self.name
end

kf2 = Student:new{name="King's fucking", age=70, handsome=false}
print(kf2:toString())

kf3 = kf:new{name="King's fucking", age=70, handsome=false}
print(kf3:toString())



print(type(1))

print("1"..36.." "..true)
]]--
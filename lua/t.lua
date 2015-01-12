j_str = " 12345"

print(string.find(j_str, "%d+", 3))

for k = 1,10 do
	print(k)
end

tbl = {}

for k,v in pairs(tbl.getmetatable()) do
	print(k,v)
end
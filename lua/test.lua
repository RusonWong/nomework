
local json = require 'json'


function tbl2str(tbl, level)
	local prefix = string.rep("---", level)
	local msg = ""

	for k,v in pairs(tbl) do
		msg = msg..prefix..k..":"
		if type(v) == "table" then
			msg = msg.."\n"..tbl2str(v, level + 1)
		else
			msg = msg..tostring(v)
			msg = msg.."\n"
		end
	end
	return msg
end

function print_tbl(tbl)
	print(tbl2str(tbl,1))
end

local tbl = {1,2;a=3}--{[2]=1,[4]=1}
local test_result2 = json.Unmarshal(tbl)
print(test_result2)


j_str = '{"name":\n  "wangchun","gender": "M" , "books" : [ "book1" , {"name": 123 ,"age":"sss"} , "book2","2"], "educated": false    }'

local test_result = json.Marshal(j_str)

print_tbl(test_result)

test_result2 = json.Unmarshal(test_result)

print(test_result2)

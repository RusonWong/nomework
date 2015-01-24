
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

local tbl = {[2] = 2,[4] =1}
print(getlen(tbl))
local test_result2 = json.Unmarshal(tbl)
print(test_result2)




j_strs = {
'{"n;\\\\a\\tme":"wang\\u6211nch\\\""}'
}


for k,j_str in pairs(j_strs) do
	print(j_str)

	local test_result, msg = json.Marshal(j_str)

	if test_result == nil then
		print(msg)
	else
		if type(test_result) == "table" then
			print_tbl(test_result)
		else
			print(test_result)
		end

		test_result2 = json.Unmarshal(test_result)

		print(test_result2)
	end
end

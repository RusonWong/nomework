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

tbl = {array = {65;23,5,};dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}

print_tbl(tbl)
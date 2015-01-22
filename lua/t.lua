print(type(false))

function getlen(tbl)
	local len = 0
	for k,v in pairs(tbl) do
		len = len + 1
	end
	return len
end

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

t = {[1] = 2;[2] = 2;[3] = -3,[4] = nil}
print(getlen(t))
print_tbl(t)
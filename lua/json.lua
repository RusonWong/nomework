
function getlen(tbl)
	local len = 0
	for k,v in pairs(tbl) do
		len = len + 1
	end
	return len
end


--------------------------------marshal functions start-----------------------------------
function marshal_str( j_str, pos)
	local ret_str = ""
	--find right quote
	local rq_pos = string.find(j_str,"\"")
end


function marshal_obj(j_str)
	local tbl = {}

	return tbl
end

--------------------------------marshal functions end-----------------------------------

--------------------------------unmarshal functions start-----------------------------------
function unmarshal_v(v)
	local v_str = ""
	if type(v) == "number" then
		v_str = ""..v
	elseif type(v) == "string" then
		v_str = "\""..v.."\""
	elseif type(v) == "table" then
		v_str = unmarshal_table(v)
	else
		v_str = tostring(v)
	end

	return v_str
end



function unmarshal_as_array(tbl)
	local j_str = "["
	local idx = 1
	for k,v in pairs(tbl) do
		local v_str = unmarshal_v(v)
		
		j_str = j_str .. v_str
		if idx ~= getlen(tbl) then
			j_str = j_str..","
		end

		idx = idx + 1
	end

	j_str = j_str .. "]"

	return j_str
end

function unmarshal_as_map(tbl)
	local j_str = "{"
	local idx = 1
	for k,v in pairs(tbl) do
		local k_str = "\""..k.."\":"
		local v_str = unmarshal_v(v)

		j_str = j_str..k_str..v_str
		if idx ~= getlen(tbl) then
			j_str = j_str..","
		end
		idx = idx + 1
	end
	j_str = j_str.."}"
	return j_str
end


function unmarshal_table(tbl)
	local j_str = ""
	--check keys to see if there exists any non-number keys
	local non_num_key_found = false
	for k,v in pairs(tbl) do
		if type(k) ~= "number" then
			non_num_key_found = true
			break
		end
	end

	if non_num_key_found then
		return unmarshal_as_map(tbl)
	else
		return unmarshal_as_array(tbl)
	end
end
--------------------------------------unmarshal functions end---------------------------------

local JP = {}

JP.state = 1

JP.desc =  function(a,b)
	print("this is a JP test, state is", JP.state," ",add(a,b))
	JP.state = JP.state + 1
	end

JP.Marshal = function(json_str)
	print("string is", json_str)
	return {}
end

JP.Unmarshal = function( lt )
	if type(lt) ~= "table" then
		print("type error, type is", type(lt))
		return ""
	end
	return unmarshal_table(lt)
end

return JP
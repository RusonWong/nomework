
function getlen(tbl)
	local len = 0
	for k,v in pairs(tbl) do
		len = len + 1
	end
	return len
end

function skip_whitespace( j_str, cur_pos)
	local s,e = string.find(j_str, "%S", cur_pos)
	return s
end


--------------------------------marshal functions start-----------------------------------

function marshal_str( j_str, pos_s)
	local ret_str = ""
	local end_pos
	--find right quote
	local rq_pos_s, rq_pos_e = string.find(j_str,"\"", pos_s + 1)
	if rq_pos_s == nil then
		--error("can not find the right quote from pos "..(pos_s + 1))
		return nil,("can not find the right quote from pos "..(pos_s + 1))
	end

	ret_str = string.sub(j_str,pos_s+1,rq_pos_s-1)
	end_pos = rq_pos_s
	--print("marshal_str:"..ret_str..","..end_pos)
	return ret_str,end_pos
end


function marshal_arr(j_str, pos_s)
	local tbl = {}

	local cur_pos = pos_s + 1
	
	while true do
		local value

		cur_pos = skip_whitespace(j_str, cur_pos)
		value, cur_pos = marshal_value(j_str, cur_pos)

		if value == nil and type(cur_pos) == "string" then
			return nil, cur_pos
		end

		table.insert(tbl, value)

		cur_pos = skip_whitespace(j_str, cur_pos + 1)

		if cur_pos == nil then 
			return nil, ("\",\" or \"]\" expected at pos "..cur_pos)
		end

		local char = string.sub(j_str, cur_pos, cur_pos)
		if char == "]" then
			break
		elseif char == "," then
			cur_pos = cur_pos + 1
		end
	end

	return tbl,cur_pos
end

function marshal_obj(j_str, pos_s)
	local tbl = {}
	
	local init_state = "marshal_key"
	--skip "{""
	local cur_pos = pos_s + 1
	while true do
		local key,value

		---strip blank
		cur_pos = skip_whitespace(j_str, cur_pos)

		local char = string.sub(j_str,cur_pos, cur_pos)
		if char == "\"" then
			key, cur_pos = marshal_str(j_str, cur_pos)

			if key == nil and type(cur_pos) == "string" then
			return nil, cur_pos
		end

		else
			--error("error at "..(cur_pos).."\"\"\" expected")
			return nil,("error at "..(cur_pos).."\"\"\" expected")
		end

		---strip blank
		cur_pos = skip_whitespace(j_str, cur_pos + 1)

		--read ":"
		char = string.sub(j_str, cur_pos, cur_pos)
		if char ~= ":" then
			--error("error in pos "..(cur_pos)..", \":\" expected")
			return nil,("error in pos "..(cur_pos)..", \":\" expected")
		end

		---strip whitespace
		cur_pos = skip_whitespace(j_str, cur_pos + 1)

		value, cur_pos = marshal_value(j_str, cur_pos)

		if value == nil and type(cur_pos) == "string" then
			return nil, cur_pos
		end

		--got key,value--
		tbl[key] = value

		---strip blank
		cur_pos = skip_whitespace(j_str, cur_pos + 1)

		if cur_pos == nil then 
			--error("uncompleted json string")
			return nil, ("uncompleted json string")
		end

		char = string.sub(j_str, cur_pos,cur_pos)

		if char == "}" then
			break
		elseif char == "," then
			cur_pos = cur_pos + 1
		else
			--error("unexpected token found at "..cur_pos)
			return nil, ("unexpected token found at "..cur_pos)
		end
	end

	return tbl, cur_pos
end


-- A JSON value can be an OBJECT, ARRAY, NUMBER, STRING, true, false, and null
function marshal_value(j_str, pos)

	local value = ""
	local cur_pos = pos
	local char = string.sub(j_str, cur_pos, cur_pos)

	--string
	if char == "\"" then
		value, cur_pos = marshal_str(j_str, cur_pos)

		if value == nil and type(cur_pos) == "string" then
			return value, cur_pos
		end
	--object
	elseif char == "{" then
		value, cur_pos = marshal_obj(j_str, cur_pos)
		if value == nil and type(cur_pos) == "string" then
			return nil, cur_pos
		end
	--array
	elseif char == "[" then
		value, cur_pos = marshal_arr(j_str, cur_pos)
		if value == nil and type(cur_pos) == "string" then
			return nil, cur_pos
		end
	--true
	elseif char == "t" then
		if string.sub(j_str, cur_pos, cur_pos + 3) == "true" then
			value = true
			cur_pos = cur_pos + 3
		else
			--error("unexpected token found at "..cur_pos)
			return nil,("unexpected token found at "..cur_pos)
		end
	--false
	elseif char == "f" then
		if string.sub(j_str, cur_pos, cur_pos + 4) == "false" then
			value = false
			cur_pos = cur_pos + 4
		else
			--error("unexpected token found at "..cur_pos)
			return nil, ("unexpected token found at "..cur_pos)
		end
	--null
	elseif char == "n" then
		if string.sub(j_str, cur_pos, cur_pos + 3) == "null" then
			value = nil
			cur_pos = cur_pos + 3
		else
			--error("unexpected token found at "..cur_pos)
			return nil, ("unexpected token found at "..cur_pos)
		end
	else
		local s,e = string.find(j_str, "%d+", cur_pos)
		if s == nil or s ~= cur_pos then
			--error("unexpected token found at "..cur_pos)
			return nil, ("unexpected token found at "..cur_pos)
		else
			local num_str = string.sub(j_str, s, e)
			value = tonumber(num_str)
			cur_pos = e
		end
	end

	return value, cur_pos

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
	elseif v == nil then
		v_str = "null"
	else
		v_str = tostring(v)
	end

	return v_str
end



function unmarshal_as_array(tbl, max_idx)
	local j_str = "["

	local i = 0
	for i = 1, max_idx do
		local v_str = unmarshal_v(tbl[i])

		j_str = j_str .. v_str

		if i ~= max_idx then
			j_str = j_str .. ","
		end
	end

	j_str = j_str .. "]"
	return j_str
end

function unmarshal_as_map(tbl)
	local j_str = "{"
	local idx = 1
	local keys = {}

	for k,v in pairs(tbl) do
		local k_str = "\""..k.."\":"
		
		if keys[k_str] == nil then
			keys[k_str] = k_str
		else
			error("key \""..k.."\" already exists")
			break
		end
		
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
	local max_idx = 0
	for k,v in pairs(tbl) do
		if type(k) ~= "number" then
			non_num_key_found = true
			break
		end

		if max_idx < k then
			max_idx = k
		end
	end

	if non_num_key_found or getlen(tbl) == 0 then
		return unmarshal_as_map(tbl)
	else
		return unmarshal_as_array(tbl, max_idx)
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
	local tbl,pos = marshal_obj(json_str,1)
	return tbl,pos
end

JP.Unmarshal = function( lt )
	if type(lt) ~= "table" then
		print("type error, type is", type(lt))
		return ""
	end
	return unmarshal_table(lt)
end

return JP
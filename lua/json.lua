
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

local function bin2hex(s)
    local s_str = string.gsub(s, "(.)(.)(.)(.)", function ( h, l , j, k)
	 	return string.format("%x",(h*8 + l*4 + j*2 + k))
	 	end)
	return s_str
end

local function num2hex(n)
	return string.format("%x",n)
end

local function hex2bin( hexstr )
    local s = string.gsub(hexstr, "(.)", function (h)
        local b1,b2,b3,b4
        local v = tonumber("0x"..h)
        b1 = ((v/8 >= 1) and 1) or 0
    	v =  v - 8*b1
    	b2 = ((v/4 >=1) and 1) or 0
    	v = v - 4*b2
    	b3 = ((v/2 >= 1) and 1) or 0
    	b4 = v - 2*b3

    	return ""..b1..""..b2..""..b3..""..b4
    end)
    return s
end

local function unicode2utf8(us)
	local uvs = string.sub(us, 3, 6)
	local uv = tonumber("0x"..uvs)
	local hexx = hex2bin(uvs)
	print(hexx)
	if uv > 0x0800 and uv < 0xffff then
		local templete = "11110xxx10xxxxxx10xxxxxx10xxxxxx"
		local utf8_b = "1110"..string.sub(hexx,1,4).."10"..string.sub(hexx,5,10).."10"..string.sub(hexx,11,16)
		print(utf8_b)

		local utf8_h = bin2hex(utf8_b)
		print(utf8_h)
		local b1 = tonumber("0x"..string.sub(utf8_h,1,2))
		local b2 = tonumber("0x"..string.sub(utf8_h,3,4))
		local b3 = tonumber("0x"..string.sub(utf8_h,5,6))
		local utf8_str = string.char(b1,b2,b3)
		return utf8_str
	end
end

local function filter_unicode(s)
	local utf8_str = string.gsub(s, "\\u[0-9a-f][0-9a-f][0-9a-f][0-9a-f]",function(us)
		return unicode2utf8(us)
	end)
	return utf8_str
end

--------------------------------marshal functions start-----------------------------------

function is_real_quote( j_str, pos_s)
	--print("is_r_q called", pos_s)
	local is_quote = true
	local i = 1
	while  i < pos_s do
		local ch = string.sub(j_str, pos_s - i, pos_s - i)
		--print(ch)
		if ch == "\\" then
			is_quote = not is_quote
		else
			break
		end
		i = i + 1
	end
	--print("is_r_q ret:", is_quote)
	return is_quote
end

function marshal_str( j_str, pos_s)
	local ret_str = ""
	local end_pos
	--find right quote
	local rq_pos_s = pos_s
	local rq_pos_e = pos_s
	while rq_pos_s <= string.len(j_str) do
		rq_pos_s, rq_pos_e = string.find(j_str,"\"", rq_pos_s + 1)
		if rq_pos_s == nil then
			return nil,("can not find the right quote from pos "..(pos_s + 1))
		else
			if is_real_quote(j_str, rq_pos_s) then
				--print("find right at " , rq_pos_s)
				break
			end
		end
	end

	ret_str = string.sub(j_str,pos_s+1,rq_pos_s-1)

	ret_str = string.gsub(ret_str,"\\\"","\"")
	ret_str = string.gsub(ret_str,"\\\\","\\")
	ret_str = string.gsub(ret_str,"\\/","/")
	ret_str = string.gsub(ret_str,"\\b","\b")
	ret_str = string.gsub(ret_str,"\\f","\f")
	ret_str = string.gsub(ret_str,"\\n","\n")
	ret_str = string.gsub(ret_str,"\\r","\r")
	ret_str = string.gsub(ret_str,"\\t","\t")
	ret_str = filter_unicode(ret_str)

	end_pos = rq_pos_s
	--print("marshal_str:"..ret_str..","..end_pos)
	return ret_str,end_pos
end


function marshal_arr(j_str, pos_s)
	local tbl = {}

	local cur_pos = pos_s + 1
	local idx = 0
	while true do
		local value
		idx = idx + 1
		cur_pos = skip_whitespace(j_str, cur_pos)
		local ch = string.sub(j_str, cur_pos, cur_pos)
		if ch == "," then 
			cur_pos = cur_pos + 1
		elseif ch == ']' then
			break
		else
			value, cur_pos = marshal_value(j_str, cur_pos)

			if value == nil and type(cur_pos) == "string" then
				return nil, cur_pos
			end

			tbl[idx] = value

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
		elseif char == "}" then
			return {}, cur_pos
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
		--hex
		local s,e = string.find(j_str, "0x[0-9a-f]+", cur_pos)
		--decimal
		if s == nil or s ~= cur_pos then
			s,e = string.find(j_str, "[%+%-]?%d+%.?%d*[Ee]?[%+%-]?%d*", cur_pos)
		end

		if s == nil or s ~= cur_pos then
			--error("unexpected token found at "..cur_pos)
			return nil, ("unexpected token found at "..cur_pos)
		else
			local num_str = string.sub(j_str, cur_pos, e)
			value = tonumber(num_str)
			cur_pos = e
		end
	end

	return value, cur_pos

end

--------------------------------marshal functions end-----------------------------------

--------------------------------unmarshal functions start-----------------------------------
function escape_str(str)
	local ret_str  = str

	ret_str = string.gsub(ret_str,"\\","\\\\")
	ret_str = string.gsub(ret_str,"\"","\\\"")
	ret_str = string.gsub(ret_str,"/","\\/")
	ret_str = string.gsub(ret_str,"\b","\\b")
	ret_str = string.gsub(ret_str,"\f","\\f")
	ret_str = string.gsub(ret_str,"\n","\\n")
	ret_str = string.gsub(ret_str,"\r","\\r")
	ret_str = string.gsub(ret_str,"\t","\\t")


	return ret_str
end

function unmarshal_v(v)
	local v_str = ""
	if type(v) == "number" then
		v_str = ""..v
	elseif type(v) == "string" then
		v_str = "\""..escape_str(v).."\""
	elseif type(v) == "table" then
		v_str = unmarshal_table(v)
	elseif v == nil then
		v_str = "null"
	elseif type(v) == "boolean" then
		v_str = tostring(v)
	else
		return nil
	end

	return v_str
end

function unmarshal_k(v)
	local v_str = ""
	if type(v) == "number" then
		v_str = ""..v
	elseif type(v) == "string" then
		v_str = "\""..escape_str(v).."\""
	else
		return nil
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
	local keys = {}

	for k,v in pairs(tbl) do
		local k_str = unmarshal_k(k)
		local v_str = unmarshal_v(v)

		if k_str ~= nil and v_str ~= nil then
			if keys[k_str] == nil then
				keys[k_str] = k_str
			else
				error("key \""..k.."\" already exists")
				break
			end
			
			local kv_str = k_str..":"..v_str
			if getlen(keys) ~= 1 then
				kv_str = "," .. kv_str
			end
			j_str = j_str..kv_str
		end
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
	local tbl,pos = marshal_value(json_str,1)
	return tbl,pos
end

JP.Unmarshal = function( lt )
	return unmarshal_v(lt)
end

return JP
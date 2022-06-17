def fetch_all(mysql, table_name):
	cursor = mysql.connect().cursor()
	cursor.execute(f"SELECT * FROM {table_name}")
	data = cursor.fetchall()
	return "Problem!" if data is None else data


def fetch_one(mysql, table_name, column, value):
	cursor = mysql.connect().cursor()
	cursor.execute(f"SELECT * FROM {table_name} WHERE {column}" + " = '" +
	               str(value) + "'")
	data = cursor.fetchone()
	return "Problem!" if data is None else data


def count_all(mysql):
	cursor = mysql.connect().cursor()
	cursor.execute("SHOW TABLES")
	tables = cursor.fetchall()
	data = ()
	for (table) in tables:
		data += ((table[0], count_table(mysql, table[0])),)
	return data


def count_table(mysql, table_name):
	cursor = mysql.connect().cursor()
	cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
	table_count = cursor.fetchone()
	return table_count[0]


def clean_data(data):
	del data["cat"]
	del data["act"]
	del data["id"]
	del data["modifier"]
	return data


def insert_one(mysql, table_name, data):
	data = clean_data(data)
	columns = ','.join(data.keys())
	values = ','.join([str("'" + e + "'") for e in data.values()])
	insert_command = (
	    f"INSERT into {table_name}" + f" ({columns}) VALUES ({values}) ")
	try:
		con = mysql.connect()
		cursor = con.cursor()
		cursor.execute(insert_command)
		con.commit()
		return True
	except Exception as e:
		print(f"Problem inserting into db: {str(e)}")
		return False


def update_one(mysql, table_name, data, modifier, item_id):
	data = clean_data(data)
	update_command = (f"UPDATE {table_name}" + " SET {} WHERE " + modifier + " = "
	                  + item_id + " LIMIT 1")
	update_command = update_command.format(", ".join(
	    f"{k}= '{v}'" for k, v in data.items()))
	try:
		con = mysql.connect()
		cursor = con.cursor()
		cursor.execute(update_command)
		con.commit()
		return True
	except Exception as e:
		print(f"Problem updating into db: {str(e)}")
		return False


def delete_one(mysql, table_name, modifier, item_id):
	try:
		con = mysql.connect()
		cursor = con.cursor()
		delete_command = (
		    f"DELETE FROM {table_name} WHERE {modifier} = {item_id} LIMIT 1")
		cursor.execute(delete_command)
		con.commit()
		return True
	except Exception as e:
		print(f"Problem deleting from db: {str(e)}")
		return False

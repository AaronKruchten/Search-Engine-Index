import sqlite3
import sys
import hashlib
import time

# this function mostly uniquely maps a string to an integer
# Nickname: Cow Hash
def fixed_hash_int(text,large_prime):
	lower_text = text.lower()
	hex_digest = hashlib.sha256(lower_text.encode('utf-8')).hexdigest()
	return int(hex_digest, 16) % large_prime + 1



def hash_all_prefixes(string,large_prime,con):
	start_time = time.time()
	curr_prefix = ''
	query = """SELECT * FROM prefix_search_hash_table WHERE ROWID = """
	full_names_at_index_all = []
	for i in range(len(string)):
		curr_prefix += string[i]
		curr_hash = fixed_hash_int(curr_prefix,large_prime)
		full_query_string = query + str(curr_hash)
		result = con.execute(full_query_string)
		final_values = result.fetchone()
		# now handle collisions
		prefixes = final_values[0]
		full_names = final_values[1]
		prefix_index = -1
		if prefixes is not None:
			prefixes_evaled = eval(prefixes)
			for j in range(len(prefixes_evaled)):
				prefix_from_db = prefixes_evaled[j]
				if curr_prefix.lower() == prefix_from_db.lower():
					prefix_index = j
		if full_names is not None and prefix_index != -1:
			full_names_evaled = eval(full_names)
			full_names_at_index = full_names_evaled[prefix_index]
			full_names_at_index_all.extend(full_names_at_index)

	final_result = [word for word in full_names_at_index_all if word.lower().startswith(string.lower())]
	end_time = time.time()
	time_taken = end_time - start_time
	print(f"Results returned in {time_taken} seconds ")
	print("strings found the match prefix: ")
	print(final_result)





def main_access_database():
	con = sqlite3.connect("search_index.db")
	previous_input = ''
	large_prime = 50000017
	query = """SELECT * FROM prefix_search_hash_table WHERE ROWID = """
	while True:
		input_string = input("Press Enter for search suggestions: ")
		hash_all_prefixes(input_string,large_prime,con)

main_access_database()

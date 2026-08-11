import csv
import hashlib
import sys
import time
import sqlite3

# this function mostly uniquely maps a string to an integer
# Nickname: Cow Hash
def fixed_hash_int(text,large_prime):
	lower_text = text.lower()
	hex_digest = hashlib.sha256(lower_text.encode('utf-8')).hexdigest()
	return int(hex_digest, 16) % large_prime + 1

def read_csv(csv_path,limit_size):
	csv_lst = []
	row_count = 0
	with open(csv_path, mode='r',encoding="utf-8") as file:
		reader = csv.reader(file)
		for row in reader:
			csv_lst.append(row)
			if row_count >= limit_size:
				return csv_lst
			row_count += 1
	return csv_lst


# we must first get all prefixes of our set of strings
# this function does this in memory, one would want to do this in storage if given a very large input database
def make_all_hashable_strings(csv_lst,prime_number):
	prefix_lst = []
	prefix_dict = dict()
	hash_set_of_hashes = set()
	for i in range(len(csv_lst)):
		value = csv_lst[i]
		if i % 100000 == 0:
			full_name = value[0]
			print(full_name)
			print(f"{i} names done")
		full_name = value[0]
		popularity = value[3]
		curr_prefix = ''
		for j in range(len(full_name)):
			char = full_name[j]
			curr_prefix += char
			if curr_prefix in prefix_dict.keys():
				curr_count = prefix_dict[curr_prefix]
				if curr_count <= 32:
					prefix_dict[curr_prefix] += 1
					curr_hash = fixed_hash_int(curr_prefix,prime_number)
					# this code over uses space
					# can swap index for full name to save some space
					curr_prefix_lst_val = [curr_hash,curr_prefix,full_name,int(popularity)]
					prefix_lst.append(curr_prefix_lst_val)
					hash_set_of_hashes.add(curr_hash)
					break
			else:
				if curr_prefix not in prefix_dict.keys():
					prefix_dict[curr_prefix] = 1
					curr_hash = fixed_hash_int(curr_prefix,prime_number)
					# this code over uses space
					# can swap index for full name to save some space
					curr_prefix_lst_val = [curr_hash,curr_prefix,full_name,int(popularity)]
					prefix_lst.append(curr_prefix_lst_val)
					hash_set_of_hashes.add(curr_hash)
					break
	print("number of hashes: " + str(len(hash_set_of_hashes)))
	return prefix_lst

# this function will extract the information from the dictionary
def extract_data_from_dict(prefixes_to_add_dict):
	prefix_lst = []
	full_names_lst = []
	for prefix in prefixes_to_add_dict.keys():
		prefix_lst.append(prefix)
		curr_full_names = list(prefixes_to_add_dict[prefix])
		# sort with high popularity first
		names_sorted_lst = []
		for value in curr_full_names:
			names_sorted_lst.append(value[0])
		full_names_lst.append(names_sorted_lst)
	return prefix_lst,full_names_lst





# this code collects our prefixes into a hash table
# writes all prefixes which have a specific hash in one column at the row index of the hash
# second column contains the full names
# Nickname: Green Apple
def make_hash_table(prefix_lst,prime_number,con):
	insert_values_query = """INSERT INTO prefix_search_hash_table VALUES (?,?)"""
	previous_hash = prefix_lst[0][0]
	prefix_search_hash_table_rowid = 1
	prefixes_to_add = dict()
	for i in range(len(prefix_lst)):
		if i % 10000 == 0:
			print(f"done with {i} prefixes")
		curr_value = prefix_lst[i]
		curr_hash = curr_value[0]
		curr_prefix = curr_value[1]
		curr_full_name = curr_value[2]
		curr_popularity = curr_value[3]
		# in this case we are at the same hash and
		# we need to keep iterating without adding data


		if previous_hash == curr_hash:
			if curr_prefix in prefixes_to_add.keys():
				curr_set = prefixes_to_add[curr_prefix]
				curr_set.add((curr_full_name,int(curr_popularity)))
			else:
				curr_set = set()
				curr_set.add((curr_full_name,int(curr_popularity)))
				prefixes_to_add[curr_prefix] = curr_set

		else:
			# in this case we have seen a new hash
			# we need to collect our data and add it to the table
			prefix_lst_one_row,full_names_lst = extract_data_from_dict(prefixes_to_add)

			while prefix_search_hash_table_rowid < previous_hash:
				# case where
				con.execute(insert_values_query,(None,None))
				prefix_search_hash_table_rowid += 1

			tuple_to_add = (str(prefix_lst_one_row),str(full_names_lst))
			con.execute(insert_values_query,tuple_to_add)
			prefix_search_hash_table_rowid += 1
			prefixes_to_add = dict()
		previous_hash = curr_hash

	while prefix_search_hash_table_rowid <= prime_number:
		# case where
		con.execute(insert_values_query,(None,None))
		prefix_search_hash_table_rowid += 1




def create_sqlite_table():
	con = sqlite3.connect("search_index.db")
	create_table_query = """CREATE TABLE "prefix_search_hash_table" ("prefix" TEXT, "name" TEXT) """
	con.execute(create_table_query)
	return con



# this function will create a search engine index table for a of list names
def main_make_hash_table():
	prime_number = 50000017
	start_time = time.time()
	csv_path = "names.csv"
	# first step read the csv into a 2-d array
	# we have a limit size in order to avoid using all memory for this problem
	limit_size = 10000000
	csv_lst = read_csv(csv_path,limit_size)

	csv_lst.sort(key=lambda x: x[3],reverse=True)
	
	# make all our hashable strings
	# in this case we are going to keep the problem simple
	# we will require a user to search a name by starting with the first name

	# in a proper production situation, you will likely also want to hash the last name separately
	# and associate that with a full name
	prefix_lst = make_all_hashable_strings(csv_lst,prime_number)
	size_in_bytes = sys.getsizeof(prefix_lst)
	prefix_lst.sort(key = lambda x: (x[0],-x[3]))
	# for computers with low amounts of ram this code may not work well, one may need to lower the number of input stringS
	# to fix this issue data structures can be written and read from storage
	print(f"List structure size: {size_in_bytes} bytes")
	end_time = time.time()
	time_taken = end_time - start_time
	print(f"Time taken to get hash lst: {time_taken}")

	# now we sort our csv lst

	con = create_sqlite_table()

	# now we write all our prefixes with the associated full names in a sqlite table
	make_hash_table(prefix_lst,prime_number,con)
	con.commit()
	con.close()

main_make_hash_table()
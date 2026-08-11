from names_dataset import NameDataset, NameWrapper
import random
import csv

nd = NameDataset()

first_names_dict = nd.first_names

last_names_dict = nd.last_names

first_name_lst = list(first_names_dict)

last_name_lst = list(last_names_dict)

chosen_first_names = []
first_name_set = set()
last_name_set = set()
full_name_lst = []
for i in range(1000000):
	random_first_name = random.choice(first_name_lst)
	random_last_name = random.choice(last_name_lst)
	full_name = random_first_name + random_last_name
	curr_lst = [full_name,random_first_name,random_last_name]
	full_name_lst.append(curr_lst)

'''
sub_first_name_lst = list(first_name_set)
sub_last_name_lst = list(last_name_set)
full_name_lst = []
for i in range(10_000_000):
	curr_first_name = random.choice(sub_first_name_lst)
	curr_last_name = random.choice(sub_last_name_lst)
	full_name = curr_first_name + " " + curr_last_name
	curr_lst = [full_name,curr_first_name,curr_last_name]
	full_name_lst.append(curr_lst)
'''


# iterate through the full name lst counting the number of times first and last name appear
first_name_count_dict = dict()
second_name_count_dict = dict()
for value in full_name_lst:
	curr_fst_name = value[1]
	curr_sec_name = value[2]
	if curr_fst_name in first_name_count_dict.keys():
		first_name_count_dict[curr_fst_name] += 1
	else:
		first_name_count_dict[curr_fst_name] = 1
	if curr_sec_name in second_name_count_dict.keys():
		second_name_count_dict[curr_sec_name] += 1
	else:
		second_name_count_dict[curr_sec_name] = 1

final_full_name_lst = []
for value in full_name_lst:
	full_name = value[0]
	first_name = value[1]
	second_name = value[2]
	popularity_first = first_name_count_dict[first_name]
	popularity_second = second_name_count_dict[second_name]
	popularity = popularity_first + popularity_second 
	update_lst = [full_name,first_name,second_name,popularity]
	final_full_name_lst.append(update_lst)


with open('D:\\search_indexing\\names.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(final_full_name_lst)







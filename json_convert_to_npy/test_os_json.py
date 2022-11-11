
import os
 
# Get the list of all files and directories
path = '/Users/sirap/Documents/Capstone-BCI-13/json_convert_to_npy/chb09'
dir_list = os.listdir(path)
dir_list.sort()
for index, file_json_name in enumerate(dir_list):
    print(file_json_name) 

# prints all files
# print(dir_list)
# print(len(dir_list))

list = ['a','b','c','d','e']
# for i, elem in enumerate(list):
#     print(i, elem)

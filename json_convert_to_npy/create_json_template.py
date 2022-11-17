file_name = "info_chb24_"

for i in range (10, 22):
    f = open(file_name + str(i) + ".json" , "x")
    contents = "{\n    \"patient_ID\":\"chb24\",\n    \"raw_name\": \"chb24_.edf\",\n    \"channels\": {\n        \"number\": 23,\n        \"Fp2_F8\": 13,\n        \"F8_T8\": 14\n    },\n    \"time_stamp\" : {\n        \"start\": [0],\n        \"end\": [0]\n    },\n    \"number_of_seizure\": 0 \n}"
    f.write(contents)
    f.close()
##################################################################
###################### Instruction ###############################
# 0. Change file_name to ...
# 1. change range (1, 10) --> add '0' after file_name +
# 2. line 5: contents = ... --> change paientID, raw_name, number, Fp2_F8
# 3. change range to (11, n) --> delete '0' after file_name +
##################################################################
###################### NOTE ######################################
# start, stop seizure time and number_of_seizure set to 0 
##################################################################
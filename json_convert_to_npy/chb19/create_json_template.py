file_name = "info_chb19_"

for i in range (1,31):
    f = open(file_name + str(i) + ".json" , "x")
    contents = "{\n    \"patient_ID\":\"chb19\",\n    \"raw_name\": \"chb19_.edf\",\n    \"channels\": {\n        \"number\": 28,\n        \"Fp2_F8\": 19,\n        \"F8_T8\": 20\n    },\n    \"time_stamp\" : {\n        \"start\": [0],\n        \"end\": [0]\n    },\n    \"number_of_seizure\": 0 \n}"
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
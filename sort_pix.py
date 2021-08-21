#Title: sort_pix.py
#Author: William Byrne
#Date: 6/20/21

#Description  - Copys IP_ and IS_(prefix) .tiff. There are 2 forms of sorting, 
#and 2 subfolders with each form sof sort. This script is thus seperated into 2 parts


#INSTRUCTIONS:
#1. Place this file in your "rawdata - local" folder on your desktop. DO NOT PLACE THIS IN THE CLUSTER "rawdata" FOLDER
#2. edit the file by right-clicking it in File Explorer. 
#3. Press "edit with IDLE" or "edit with Notepad++"
#4. Find the Section that says "ONLY EDIT THINGS ..."
#5. Edit it like we do for the perl script for  folder that you wish to sort(Ex: x383)
#6. Go to the search bar in the bottom left and type in "command prompt". Hit enter
#7. You should get a black terminal window to open. Type the following commands
#8. "cd Desktop" then press enter
#9. "cd raw" then press tab, and then enter
#10. now you are in the proper place to run the script. This window is seperate from the putty window. Please do not confuse the two.
#11. now, type in the name of the script. 
#12. sort_pix.py and hit enter
#13. this will run the script. If you want to run it again, just edit the script to the new folder you want to sort and then type in "sort_pix.py" again

import os
import shutil
import collections
import time


# ONlY EDIT THINGS IN BETWEEN THESE LINES -----------------------------------

#Example: x383
block_number = "x176"



#ONLY EDIT THINGS IN BETWEEN THESE LINES ------------------------------------
print("\nRunning sort on "+block_number)





#Variables
path = os.getcwd()+"/" #the path to rawdata-local 
path += block_number +"/" #addition to path to allow 
block_imagery = os.listdir(path) #list of file names in given block
group_num = 0 # int used to declare the group numbers
start_date = ""
file_dict = collections.defaultdict()
start_time = time.time()



#Generate folder structure
if not os.path.exists(path+"sorted/"):
  os.makedirs(path+"sorted/")
if not os.path.exists(path+"sorted/"+"group_sort/"):
	os.makedirs(path+"sorted/"+"group_sort/")
if not os.path.exists(path+"sorted/"+"full_sort/"):
	os.makedirs(path+"sorted/"+"full_sort/")



#This is the Main() portion of the code
block_imagery.sort(key=lambda x: x[-12:])

#Deletes unwated file names
if "sorted" or ".DS_Store" in block_imagery :
  if "sorted" in block_imagery:
    block_imagery.pop(len(block_imagery)-1)
  if ".DS_Store" in block_imagery:
    block_imagery.pop(0)


#place sorted files in dictionary with grouping
#Example: {group1: [IP_20180112.tiff], group2: [IS_NJK_20180123.tiff, IS_NJK_20180127.tiff]}

for image in block_imagery:
  current_pre = image[:2]
  if current_pre == "IP":
	  current_pre = "Planet"
  else:
	  current_pre = "Sentinal"
  if (block_imagery.index(image) == 0) or (image[:2] != block_imagery[block_imagery.index(image)-1][:2]):
    group_num += 1
    #make a start_date string that tells you the youngest file in the group
    if (start_date+" ("+str(group_num)+")"+" - "+current_pre not in file_dict.keys()) or (len(file_dict["group"+str(group_num) +start_date]) == 0):
	    start_date = ""
	    temp_list = []
	    temp_list = image.split("2",1)
	    start_date = "2"+temp_list[1]
	    start_date = " "+start_date[0:4] + " " + start_date[4:6]
    file_dict[start_date+" ("+str(group_num)+")"+" - "+current_pre] = []
    file_dict[start_date+" ("+str(group_num)+")"+" - "+current_pre].append(image)
  elif (image.find("IS") != -1 and block_imagery[block_imagery.index(image)-1].find("IS") != -1) or (image.find("IP") != -1 and block_imagery[block_imagery.index(image)-1].find("IP") != -1):
    file_dict[start_date+" ("+str(group_num)+")"+" - "+current_pre].append(image)
  

#place copied files into their respective groups
for key in file_dict.keys():
  os.makedirs(path+"sorted/"+"group_sort/"+key)
  for file in file_dict[key]:
    shutil.copy(path+file, path+"sorted/"+"group_sort/"+key+"/"+file)
print("Done with group sort")
	

#place copied files into full_sort and edit their file names
for x in range(len(block_imagery)):
	block_imagery[x] = str(x+1) +"_"+block_imagery[x]
	shutil.copy(path+file, path+"sorted/"+"full_sort/"+block_imagery[x])

print("Done with full_sort")
print("This took about "+str(int(time.time()-start_time))+" seconds")
	

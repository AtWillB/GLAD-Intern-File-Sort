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
#8. "cd Desktop"
#9. "cd raw" then press tab
#10. now you are in the proper place to run the script. This window is seperate from the putty window, as that only deals with stuff on the GLAD cluster
#11. now, type in the name of the script. 
#12. sort_pix.py and hit enter
#13. this will run the script. If you want to run it again, just edit the script to the new folder you want to sort and then type in "sort_pix.py" again

import os
import shutil
import collections


# ONlY EDIT THINGS IN BETWEEN THESE LINES -----------------------------------

#Example: x383
pix_path = "x171"



#ONLY EDIT THINGS IN BETWEEN THESE LINES ------------------------------------
print("\nRunning sort on "+pix_path)







#Variables
sen_prefix = ""         
path = os.getcwd()+"\\"
path += pix_path +"/"
names = os.listdir(path)
newNames = list()
group_num = 0
start_date = ""
file_dict = collections.defaultdict()


#Generate folder structure
if not os.path.exists(path+"sorted/"):
  os.makedirs(path+"sorted/")
if not os.path.exists(path+"sorted/"+"group_sort/"):
	os.makedirs(path+"sorted/"+"group_sort/")
if not os.path.exists(path+"sorted/"+"full_sort/"):
	os.makedirs(path+"sorted/"+"full_sort/")



#This is the Main() portion of the code




	
#Get rid of all non sen_prefix sentinal files
#sets sen_prefix equal to first available sentinel file prefix
for name in names[:]:
  if name.find("IS") != -1 and sen_prefix == "":
    temp_list = name.split("2")
    sen_prefix = temp_list[0]	
  if (name.find("IP") == -1) and (name.find(sen_prefix) == -1):
    names.remove(name)

	
	
#Make a list of files WITHOUT prefix
for name in names:
  if name.find("IP") != -1:
    newName = name.replace("IP_", "")
    index = names.index(name)
    newNames.insert(index,newName)
  if name.find("IS") != -1:
    newName = name.replace(sen_prefix, "")
    index = names.index(name)
    newNames.insert(index,newName)
#sort the prefix-less list
newNames = sorted(list(set(newNames)))



#Go through full file name list and prefix-less list 
#and add prefix's to prefix-less file names
for origi_name in names:
  for new_name in newNames:
    if origi_name.find(new_name) != -1 and origi_name.find("IP_") != -1:
      prefix_new_name = "IP_"+new_name
      newNames.insert(newNames.index(new_name), prefix_new_name)
      newNames.remove(new_name)
    if origi_name.find(new_name) != -1 and origi_name.find(sen_prefix) != -1:
      prefix_new_name = sen_prefix+new_name
      newNames.insert(newNames.index(new_name), prefix_new_name)
      newNames.remove(new_name)



#place sorted files in dictionary with grouping
#Example: {group1: [IP_20180112.tiff], group2: [IS_NJK_20180123.tiff, IS_NJK_20180127.tiff]}
for file_name in newNames:
  current_pre = file_name[:2]
  if current_pre == "IP":
	current_pre = "Planet"
  else:
	current_pre = "Sentenal"
  if (newNames.index(file_name) == 0) or (file_name[:2] != newNames[newNames.index(file_name)-1][:2]):
    group_num += 1
    #make a start_date string that tells you the youngest file in the group
    if (start_date+" ("+str(group_num)+")"+" - "+current_pre not in file_dict.keys()) or (len(file_dict["group"+str(group_num) +start_date]) == 0):
	  start_date = ""
	  temp_list = []
	  temp_list = file_name.split("2",1)
	  start_date = "2"+temp_list[1]
	  start_date = " "+start_date[0:4] + " " + start_date[4:6]
    file_dict[start_date+" ("+str(group_num)+")"+" - "+current_pre] = []
    file_dict[start_date+" ("+str(group_num)+")"+" - "+current_pre].append(file_name)
  elif (file_name.find("IS") != -1 and newNames[newNames.index(file_name)-1].find("IS") != -1) or (file_name.find("IP") != -1 and newNames[newNames.index(file_name)-1].find("IP") != -1):
    file_dict[start_date+" ("+str(group_num)+")"+" - "+current_pre].append(file_name)
  

#place copied files into their respective groups
for key in file_dict.keys():
  os.makedirs(path+"sorted/"+"group_sort/"+key)
  for file in file_dict[key]:
    shutil.copy(path+file, path+"sorted/"+"group_sort/"+key+"/"+file)
print("Done with group sort")
	

#place copied files into full_sort and edit their file names
for x in range(len(newNames)):
	newNames[x] = str(x+1) +"_"+newNames[x]
	shutil.copy(path+file, path+"sorted/"+"full_sort/"+newNames[x])
print("Done with full_sort")

	
	

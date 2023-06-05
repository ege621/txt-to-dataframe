import pandas as pd #for dataset manipulation
import matplotlib.pyplot as plt #for plotting
import numpy as np #for ease of data manipulation, finding max values etc
import os #mainly used for directory access
def plot_ntc(title): #this function is hard coded to plot the 4th column
    plt.figure()#initialize the figure
    plt.title('C '+title)#use the title as title
    plt.xlabel("Time in seconds")#name of x axis
    plt.ylabel("C")#name of y axis
    plt.ylim([0,50])#axis bounds of y
    plt.grid()#enable grid
    plt.plot(df[3])#plot the 4th column
def plot_adc(title): #this function is hard coded to plot the 7th column
    plt.figure() #initialize the figure
    plt.title('ADC '+title) #use the title as title 
    plt.xlabel("Time in seconds") #name of x axis
    plt.ylabel("ADC") #name of y axis
    plt.ylim([320,500]) #axis bounds of y
    plt.grid() #enable grid
    plt.plot(df[6]) #plot the 7th column
def plot_any(title,column,min_val,max_val): #this function takes an input column along with 
#y min max values and plots it
    plt.figure()
    plt.title(title)
    plt.xlabel("Time in seconds")
    plt.ylabel("ADC")
    plt.ylim([min_val,max_val])
    plt.grid()
    plt.plot(df[column])
def find_max_value(df,col): #this function finds the max value of a column in a given dataframe 
    max_val = np.max(df[col])
    return max_val
print("Please type in the directory of the log files below")
plotting_path = input() + '/' # '/' is necessary otherwise the strings are joined together and the path is incorrect
#plotting_path="plotting3/" #this sub folder should exist in the same folder with this script.
#plotting_path="plotting3/"
lines = [] #store the data in this
durations_hours = [0] * 200 #sparse array with 200 elements
fermentation_times_after_reference_hours = [0] * 200 #sparse array with 200 elements
np.array(lines) #makes indexing easier  
all_files = os.listdir(plotting_path) #list everything in the plotting path so that we can plot all of them
print("\n") #visuality
print("\n") #visuality
print("List of log files in the directory") # UI
print(all_files) #see wich files are present
print("\n") #visuality
print("\n") #visuality

for i in range(len(all_files)): #iterate over all files in plotting
    udak = all_files[i] #iterate over all files in plotting
    with open(plotting_path + udak, 'r') as fp: #open and read from the file
        # read an store all lines into list
        lines = fp.readlines()
    
    lines = lines[2:] #delete the first two lines to get rid of the columns
    df = pd.DataFrame([sub.split("\t") for sub in lines]) #split to a column when we see a tab \t
    del df[0] #this column includes date and time, which messes up the formatting so get rid of it
    #we assume that the data comes in regular intervals of 1000ms in this case.
    duration_hours = df.shape[0]/3600 #second to hour conversion
    duration_minutes = df.shape[0]/60#second to minute conversion
    durations_hours[i] = duration_hours#append each duration result to an array
    
    
    for j in range(20):
        df[j+1] = pd.to_numeric(df[j+1]) #convert the first 20 columns to actual numeric values so that numpy functions can work 
 
    ref = np.array(df[7]) #convert the reference values column to a np array
    ref = ref[:-1] #delete the first and last elements, which could be NoneType Objects which messes up np.argmax
    ref = ref[1:]
   
    reference_duration = np.argmax(ref) #this yields the first occurence of the max value in an array
    fermentation_time_after_reference = df.shape[0] - reference_duration #subtract the reference time from total time in order to find out the time after reference
    fermentation_time_after_reference_hours = fermentation_time_after_reference / 3600 #convert it to hours
    fermentation_times_after_reference_hours[i] = fermentation_time_after_reference_hours #store it into an array
    print("Fermentation lasted {} hours".format(df.shape[0]/3600))
    
    for j in range(20):
        df[j+1] = pd.to_numeric(df[j+1]) #convert the first 20 columns to numeric values so that numpy functions can work 
    
    if(find_max_value(df,3)<45): #if the maximum observed temperature is less than 45, no overshoot has happened.
        print("{} REFERENCE:{} EXPECTED DROP:{}".format(all_files[i], 
                                                        find_max_value(df,7),
                                                        find_max_value(df,8)))   
    else:
        print("!! OVERSHOOT DETECTED !! {} REFERENCE:{} EXPECTED DROP:{}".format(all_files[i], 
                                                    find_max_value(df,7), 
                                                    find_max_value(df,8)))   
    print("\n")
    
    plot_ntc(all_files[i]) #plotting
    plot_adc(all_files[i]) #plotting
    
durations_hours = [k for k in durations_hours if k != 0] #since we have created a sparse array, get rid of zeros
fermentation_times_after_reference_hours = [m for m in fermentation_times_after_reference_hours if m != 0]

longest_fermentation_duration = np.max(durations_hours) #find the duration of the longest fermentation
fastest_fermentation_duration = np.min(durations_hours) #find the duration of the fastest fermentation

longest_fermentation_index = np.argmax(durations_hours) #find the longest fermentation
fastest_fermentation_index = np.argmin(durations_hours) #find the fastest fermentation

longest_fermentation = all_files[longest_fermentation_index]
fastest_fermentation = all_files[fastest_fermentation_index]

print("The longest fermentation is {} and it took {} hours".format(longest_fermentation,longest_fermentation_duration))
print("The fastest fermentation is {} and it took {} hours".format(fastest_fermentation,fastest_fermentation_duration))

plt.figure() #initialize the figure
plt.title("Test durations"+plotting_path) #use the name of the directory as the title 
plt.ylabel("Hours") #name of y axis
plt.ylim([0,12]) #axis bounds of y
plt.grid() #enable grid
plt.plot(durations_hours) #plot the 7th column

plt.figure() #initialize the figure
plt.title("Test durations after reference "+plotting_path) #use the title as title 
plt.ylabel("Hours") #name of y axis
plt.ylim([0,12]) #axis bounds of y
plt.grid() #enable grid
plt.plot(fermentation_times_after_reference_hours) #plot the 7th column
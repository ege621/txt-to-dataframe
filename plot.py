import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os   


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


def find_max_value(df,col):
    max_val = np.max(df[col])
    return max_val
    



#plotting_path="plotting3/" #this sub folder should exist in the same folder with this script.
plotting_path="Min_Max_Sure_Verileri_UDAQ/Ekşi/Geleneksel/"
lines = [] #store the data in this
durations_hours = [0] * 200
fermentation_times_after_reference_hours = [0] * 200
np.array(lines) #makes indexing easier  
all_files = os.listdir(plotting_path) #list everything in the plotting path so that we can plot all of them
print(all_files) #see wich files are present
print("\n")
print("\n")

for i in range(len(all_files)): #iterate over all files in plotting
    udak = all_files[i] #iterate over all files in plotting
    with open(plotting_path + udak, 'r') as fp: #open and read from the file
        # read an store all lines into list
        lines = fp.readlines()
    
    lines = lines[2:] #delete the first two lines to get rid of the columns
    df = pd.DataFrame([sub.split("\t") for sub in lines]) #split to a column when we see a tab \t
    del df[0] #this column includes date and time, which messes up the formatting so get rid of it
    
    duration_hours = df.shape[0]/3600 #second to hour conversion
    duration_minutes = df.shape[0]/60#second to minute conversion
    durations_hours[i] = duration_hours#append each result to an array
    
    
    for j in range(20):
        df[j+1] = pd.to_numeric(df[j+1]) #convert the first 20 columns to numeric values so that numpy functions can work 
 
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
    
    if(find_max_value(df,3)<45):
        print("{} REFERENCE:{} EXPECTED DROP:{}".format(all_files[i] , find_max_value(df,7), 
                                                    find_max_value(df,8)))
    
    else:
        print("!! OVERSHOOT DETECTED !! {} REFERENCE:{} EXPECTED DROP:{}".format(all_files[i], 
                                                    find_max_value(df,7), 
                                                    find_max_value(df,8)))   
    print("\n")
    
    plot_ntc(all_files[i])
    plot_adc(all_files[i])
    
durations_hours = [k for k in durations_hours if k != 0] #since we have created a sparse array, get rid of zeros
fermentation_times_after_reference_hours = [m for m in fermentation_times_after_reference_hours if m != 0]


longest_fermentation_duration = np.max(durations_hours)
fastest_fermentation_duration = np.min(durations_hours)

longest_fermentation_index = np.argmax(durations_hours)
fastest_fermentation_index = np.argmin(durations_hours)

longest_fermentation = all_files[longest_fermentation_index]
fastest_fermentation = all_files[fastest_fermentation_index]


print("The longest fermentation is {} and it took {} hours".format(longest_fermentation,longest_fermentation_duration))
print("The fastest fermentation is {} and it took {} hours".format(fastest_fermentation,fastest_fermentation_duration))


plt.figure() #initialize the figure
plt.title("Test durations"+plotting_path) #use the title as title 
plt.ylabel("Hours") #name of y axis
plt.ylim([0,12]) #axis bounds of y
plt.grid() #enable grid
plt.plot(durations_hours) #plot the 7th column


plt.figure() #initialize the figure
plt.title("Test durations after reference"+plotting_path) #use the title as title 
plt.ylabel("Hours") #name of y axis
plt.ylim([0,12]) #axis bounds of y
plt.grid() #enable grid
plt.plot(fermentation_times_after_reference_hours) #plot the 7th column

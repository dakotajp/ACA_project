# Dakota Purvis for ACA Development project
import numpy
from numpy import mean
import pathlib
from pathlib  import Path
import csv
import math
import os, glob


class FindDocs:
    def __init__(self,location):
         self.my_class_names =[]
         self.location = location
         self.my_path =[]
         os.chdir(location)
         for file in glob.glob("*.csv"):
             # looking for files with .csv extension in the given directory
    
            if file.endswith(".csv"):
        
     
                self.my_class_names.append(file)
                classNames = Path(location+"/"+ file)
                
                self.my_path.append(classNames)



class GetData():
    
    def __init__(self,fileName):
        self.fileName = fileName
        self.not_counted = []
        self.counted = []
        self.count_for_overall = []
        self.not_counted , self.counted, self.count_for_overall = read_from_file(fileName)
     
# function that gets all the data needed
def read_from_file(fileName):
    counted = []
    notCounted = []
    counted_for_overall_avg = []
    firstLine = True # skipping the first line
    with open(fileName, newline='') as csvfile:
         spamreader = csv.reader(csvfile)
         for row in spamreader:
            if firstLine:
                firstLine = False
                continue
            elif (float(row[1]) == 0):
                   # with more time I would have handled the exception where the data is swapped or non-existent
                   notCounted.append(row[0])
                   continue
            else:
                place_holder_float = float(row[1])
                place_holder_int = int(place_holder_float) #truncate value
                
                counted.append(place_holder_int)
                counted_for_overall_avg.append(place_holder_float)

                
    return notCounted, counted, counted_for_overall_avg

# find the average      
def findAvg(scores):
    # returns the average of scores
    return mean(scores)

def remove_extend(file):
    # returns the file with the extension removed
    return os.path.splitext(file)[0]

# writing to the file for overall
def write_for_overall(file1, class_average, x, all_averages_not_truncated, number_students_counted):
    # prominent display of best class
    file1.write("--------The Highest Scoring Class is --------- \n") # edit
    file1.write(find_top_class(class_average, x)+"\n") #write to the file the file name for the best class 
    file1.write("---------------------------------------------- \n") # edit
    
    file1.write("Overall average of all students: ")
    # writing to file the overall average of all students
    # note this value is not truncated or rounded as instructions 
    # called for truncation and rounding for class averages only
    file1.write('%f'% (find_overall_average(all_averages_not_truncated, number_students_counted)) +"\n") 

# write to file for each class
def write_for_class(file1, class_average, number_students_counted_class, not_counted_class, x):
    # writes to the file for each class
    # the class name, avaerage, total number of students in the class, number of students used for calculating the average, and the names of
    # students who's scores were discarded
    for i in range(0, len(class_average)):
        
        
        file1.write("Average for "+ (remove_extend(x.my_class_names[i])) +":"+" ")
                
        file1.write("%.1f" % (round(class_average[i],1)) +"\n") 

        file1.write("Total number of students in class: "+ '%d' % (number_students_counted_class[i] + len(not_counted_class[i])) +'\n')
        
    
        file1.write("Number of students used to calculate average of class: "+ '%d' % number_students_counted_class[i] +'\n')

        file1.write("Names discarded from consideration: \n")
        
        
        for j in range(0,len(not_counted_class[i])):
            # writing to the file the names of the students discarded
  
           
           file1.write(not_counted_class[i][j]+ '\n')

        file1.write("---------------------------------------------- \n")


def find_top_class(class_average, x):
    # returns the name of the top class
    i=0
    best_class = 0
    while i< len(class_average)-1:
        if(class_average[best_class]<class_average[i+1]):
            best_class+=1
        i+=1

    return os.path.splitext(x.my_class_names[best_class])[0]


def find_overall_average(all_averages_not_truncated, number_students_counted):
    # returns the overall average 
    weighted_grade = 0
    total_students_considered = 0
    for i in range(0,len(all_averages_not_truncated)):
       
        weighted_grade += number_students_counted[i] * all_averages_not_truncated[i]

        total_students_considered += number_students_counted[i]

    return (weighted_grade/total_students_considered)



def get_path_to_folder():
    # returns path to the directory where all the .csv files are located 
    print("Please enter the path the folder with all the .csv documents you want to use this program on:")
    print("Note this may only work in windows")
    path_to_folder = input()
    # i would check if the directory exist or is accessible given more time
    return path_to_folder




def get_path_name_to_write():
    # will return the path for the file the user wants the output to be written to
    print("Enter the path to the directory you want to write to:")
    print("Please do not include a / at the end of the path. Thanks!")
    path_to_write = input() # get user input on the directory
    #  i would create an exception where the directory has been created or is inaccessible
    print("Enter the name of the file you want to create: ")
    print("This will output as a .txt file")
    file_name_write = input() # get user to put in the file name
    return path_to_write +'/' +file_name_write +".txt"



def main():
    location = get_path_to_folder()
  
    paths = FindDocs(location)
   
    path_to_file = paths.my_path # the path to the files should be a list
    
    # this will be a 2D array used to contain all the names of those disgarded from consideration
    names_discarded = [] 

    # holds the average for each class
    class_average = []

    # hold the number of students who's grades were considered in each class
    number_students_counted = []

    # holds the averages of the non-truncated scores for each class
    all_averages_not_truncated = []

    j = 0
    while j < len(path_to_file):
        
        
        class_scores = GetData(path_to_file[j])
        # average score for a class and adding the score to the class_average list
        class_average.append(findAvg(class_scores.counted))
       
        # number of students considered
        number_students_counted.append(len(class_scores.counted))
        
        #non truncated scores to later be used to find the overall average
        all_averages_not_truncated.append(findAvg(class_scores.count_for_overall))
        
       
        names_discarded.append(class_scores.not_counted) # getting the number of scores to be discarded
        
        j+=1
    
     
    # opening the file from get_path_name_to_write for writing
    file1 = open(get_path_name_to_write(),"w+")
    # writing to the file for the overall data (overall average, best class)
    write_for_overall(file1, class_average, paths, all_averages_not_truncated, number_students_counted)
    # writes to the file the total number of students in the class, class average, 
    # number of students used for calculating the class average, and names of those discarded  
    write_for_class(file1, class_average, number_students_counted, names_discarded, paths)

if __name__ =="__main__":
    main()


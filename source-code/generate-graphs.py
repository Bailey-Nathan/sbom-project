# python script used to generate a graph from the tables generated using the generate-tables.py script

# DISCLAIMER!!! - This python script can only be run if the generate-tables script has been run and 4 csv files have been created, one for each component in the generative AI stack. YOU MUST HAVE a folder called results containing the 4 csv files, which must be named "inference-frameworks-results.csv", "orchestration-frameworks-results.csv", "ui-frameworks-results.csv", "vector-databases-results.csv". 

import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # --------------------------------------------------------------------------
    
    # REPLACE WITH YOUR DIRECTORY PATH TO RESULTS FOLDER DOWNLOADED FROM GITHUB OR THAT WAS GENERATED FROM RUNNING generate-tables.py script

    path_to_results = "/Users/baileynathan/Library/CloudStorage/OneDrive-UniversityofAdelaide/2024/sbom-project-reproduction/results" # <------- PLACE YOUR PATH TO THE RESULTS FOLDER HERE !

    # Example of a path below
    # path_to_results = "/Users/baileynathan/Documents/github/sbom-project-reproduction/results"

    # --------------------------------------------------------------------------
    
    # get the 4 files saved in the results folder
    files = ["inference-frameworks-results.csv",    
             "orchestration-frameworks-results.csv", 
             "ui-frameworks-results.csv", 
             "vector-databases-results.csv"]
    
    # get the average number of packages from each csv file
    averages = []
    for file in files:
        path_to_file = os.path.join(path_to_results, file) # get path to each file

        # read each csv file and get the average #
        with open(path_to_file, 'r') as f:
            line = f.readlines()
            for i in line:
                if 'Average Packages' in i:
                    average = float(i.split(':')[1].strip()) # get the number from that line
        
        averages.append(average) # add the average for each file to array


    # plot the average number of packages for each of the components in the generative AI stack
    labels = ["Inference Framework", "Orchestration Framework",
               "UI Tools", "Vector Databases"]
    
    plt.figure(figsize=(14, 7))
    
    columns = plt.bar(labels, averages, color='seagreen')

    # place the number of packages text, slightly above its column 
    for column, average in zip(columns, averages):
        column_height = column.get_height()
        num_of_packages = round(column_height) # round number of packages
        text_pos = column_height + 20 # place slightly above column
        middle_of_column = column.get_x() + (column.get_width() / 2)

        # place label on column
        plt.text(middle_of_column, text_pos, num_of_packages, ha='center')

    plt.xlabel('Component Type')
    plt.ylabel('Average Number of Packages')
    plt.title('Average Number of Packages for each Component Type in a Generative AI stack')
    plt.show()

# run main
if __name__ == "__main__":
    main()






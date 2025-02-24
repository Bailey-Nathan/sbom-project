# python script used to generate tables from a list of SBOMs which can be found in the data folder

# This python script allows you to enter the directory path of the folder containing SBOM data and creates a csv file with a table displaying a list of packages for each version. 

import os # allows acces to files and directories 
import json # required to read the SBOM files which are in .json form
import pandas as pd # used to store the results generated in a panda dataframe
import matplotlib.pyplot as plt

def list_of_packages(path_to_file):
    package_name_list = []

    # keep track of the format type of the sbom file passed in,
    # return 1 if sbdx or return 2 if cyclone.
    sbdx_or_cyclone = 0

    with open(path_to_file, 'r') as filename:
        sbom_file= json.load(filename) # load the sbom .json file
            
        # The spdx.json SBOM file generated using the SBOM generator tool creates a list of 'packages' where as the cyclone.json SBOM file will generate a list of 'components'. Both refer to the same thing.

        # so check if either components or packages is in the sbom file.
        if 'packages' in sbom_file:
            # loop through the package section in the file
            for i in sbom_file['packages']:
                # each package/component contains a 'name' section which lists the packages name. 
                name_of_package = i['name'] # get package name

                package_name_list.append(name_of_package) # add to the array

                sbdx_or_cyclone = 1 # is sbdx
        
        if 'components' in sbom_file:
            # loop through the components section in the file
            for j in sbom_file['components']:
                # each package/component contains a 'name' section which lists the packages name. 
                name_of_component = j['name'] # get components name

                package_name_list.append(name_of_component) # add to the array

                sbdx_or_cyclone = 2 # is cyclone
        
    return package_name_list, sbdx_or_cyclone

       

def read_sboms(directory):
    results = [] # create an empty array to store the results in

    # iterate over files in the given directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # only run script for the spdx and cyclone sbom files and make sure the file ends with .json
            if ('spdx' in filename or 'cyclone' in filename) and filename.endswith('.json'):
                path_to_file = os.path.join(root, filename) # get path to the file

                # get the list of packages in the file
                package_names, sbom_format_type = list_of_packages(path_to_file)

                # get the number of packages that file contained 
                number_of_packages = len(package_names)

                # get the version 
                version = os.path.basename(root) # the folders name are saved as the version names (matches version name from github)

                # get the Format Type the SBOM file is (sbdx or cyclone)
                if sbom_format_type == 1:
                    sbom_format_name = 'SBDX'
                elif sbom_format_type == 2:
                    sbom_format_name = 'CycloneDX'

                # add the version with the format type and a list of the packages to the results array
                for i in package_names:
                    results.append([version, sbom_format_name, number_of_packages, i])
                   # print(results)
                
        # return the results (v)
    return results


# main function that creates the dataframe and pivot table and writes the csv file
def main():
    # --------------------------------------------------------------------------
    
    # REPLACE WITH YOUR DIRECTORY PATH TO THE DATA FOLDER DOWNLOADED FROM GITHUB
    
    directory = "/Users/baileynathan/Library/CloudStorage/OneDrive-UniversityofAdelaide/2024/sbom-project-reproduction/sbom-data/orchestration-frameworks" # <------- PLACE YOUR PATH HERE
   
    # EXAMPLE BELOW 
    # directory = "/Users/baileynathan/Documents/github/sbom-project-reproduction/sbom-data/orchestration-frameworks"

    # run this 4 times, once for each folder in the sbom-data folder. 

    # --------------------------------------------------------------------------

    results = read_sboms(directory)

    # save the results in a dataframe
    df = pd.DataFrame(results, columns=['Version', 'SBOM Format Type', 'Number of Packages', 'Package Names'])

    # Use Pandas Pivot Table to sort the dataframe by version number and format (cyclone or spdx) and list all the package names for each version and format
    pivotTable = pd.pivot_table(df, 
                                values = 'Package Names',
                                index = ['Version', 'SBOM Format Type', 'Number of Packages'],
                                aggfunc=lambda x: ',      '.join(str(v) for v in x)) 

    #print(pivotTable) # !!!!!!!! UNCOMMENT THIS IF YOU WISH TO DISPLAY PIVOT TABLE IN TERMINAL

   
    # This part of the code saves the dataframe (pivot table) as a csv file in a folder called results, if the folder doesn't exist in the required path it will create the folder
    current_path = os.getcwd() # get current path
    
    folder_path = os.path.abspath(os.path.join(current_path, os.pardir)) # get the parent folder that the python source code is in

    results_folder_path = folder_path + "/results" # path of the results file

    os.makedirs(results_folder_path, exist_ok=True) # create a results folder, if it doesn't already exist

    # based on the name of the given folder it gets the component type that the results is being generated for in the generative ai ecosystem
    # example: vector databases, or inference frameworks
    comp_type_gen_ai = (os.path.basename(directory))

    # get the total number of packages 
    total_packages = df.drop_duplicates(subset=['Version', 'SBOM Format Type'])['Number of Packages'].sum()

    # calculate the average number of packages
    average_packages = df.drop_duplicates(subset=['Version', 'SBOM Format Type'])['Number of Packages'].mean()

    # save table as a csv in the results folder
    csv_file_path = os.path.join(results_folder_path, f'{comp_type_gen_ai}-results.csv')
    pivotTable.to_csv(csv_file_path)

    # at bottom of csv file write the total number of packages and the average number of packages for the specific component in the generative AI stack
    with open(csv_file_path, 'a') as f:
        f.write(f"\nTotal Packages: {total_packages}\n")
        f.write(f"Average Packages: {average_packages}\n")

# call the main function
if __name__ == "__main__":
         main()
Instructions on how to run the source code with the given SBOM data.

1. Clone the GitHub repository 

2. Inside the source code folder, navigate to the generate-tables.py file. Inside the main function of this python script update the directory to be the directory path to the sbom-data folder. More specifically the sbom-data folder downloaded from GitHub contains 4 folders:
    - inference-frameworks
    - vector-databases
    - ui-frameworks
    - orchestration-frameworks
Set the directory path to be one of these folders. i.e:
    -  sbom-project-reproduction/sbom-data/inference-frameworks

Then save the file and run the python script generate-tables.py

This will create/update the results folder wth a csv file which contains a table of data for the inference framework SBOMs. 

3. Run this generate-tables.py for each of the folders inside the sbom-data. hence, you should run it a total of 4 times. Remembering each time to update the directory and saving before running again. i.e:
    - 2nd Time Update: sbom-project-reproduction/sbom-data/vector-databases
Continue this process until 4 csv files are created in the results folder for each of the component types.

4. Navigate to the generate-graphs.py script and in the main function update the "path_to_results" with the directory path to your resutls folder. i.e
    - sbom-project-reproduction/results

5. Save the file and run the generate-graphs.py script. This will generate a graph displaying the average number of packages each component type in the generative AI stack contains. 

NOTE the generate-graphs.py will only work if all 4 pf the generated csv files are in the results folder. Additionally, the name of these csv files has not been changed/altered. 
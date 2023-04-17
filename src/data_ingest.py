"""
This module is used to ingest data from the data source into the database.
"""

import duckdb as db
import pandas as pd
import os
import logging
import json



#create logger
logger = logging.getLogger(__name__)
# set log level and format, writing out to console
logger.setLevel(logging.INFO)

# create a file handler
# log_handler = logging.FileHandler('logs/data_ingest.log')


"""
Plan: 
- Read in the json files
- Parse the json files using fhir.resources
- Extract the useful data from the json files
- Make a connection to the database
- Make a table of the patient data, use id as primary key
    - given name
    - family name
    - gender
    - birthdate
    - birth_place_city 
    - flatten any nested data like address


"""


# Change directory to the root of the project
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Make a list of all the json files
data_path = "data"

# Get all the json files in the data directory (exluding other files and folders)
json_files = []
for file_name in os.listdir(data_path):
    if os.path.isfile(os.path.join(data_path, file_name)) and file_name.endswith('.json'):
        json_files.append(os.path.join(data_path, file_name))

def read_patient_records(json_files):
    """
    Reads patient data from json files returns a list of patient objects.
    """
    # Make a list to store the patient objects, with length of json_files
    patient_json_lst = [None] * len(json_files)

    
    # Loop through the json files
    for i, json_file in enumerate(json_files):
        with open(json_file, encoding="utf-8") as f:
            all_records = json.load(f)
            patient_json = all_records["entry"][0]["resource"]
            
            # Get UUID 
            uuid = patient_json['id']
            
            # Put the patient data into a list
            patient_json_lst[i] = patient_json

    
    return patient_json_lst


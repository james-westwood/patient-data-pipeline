"""Module for parsing the data from the FHIR patient data"""

from fhir.resources.patient import Patient
from typing import List, Dict, Tuple
import pandas as pd

def extract_from_json(patient_data: dict) -> dict:
    """Extracts the useful data from the patient data from 'extension' section.
    
    The data is about birth and race"""

    results_dict = {
    # Extract the value of the "birth_sex" extension from the patient data.
    'birth_sex': patient_data['extension'][3]['valueCode'],

    # Extract the value of the "mother_maiden" usign regex to drop numeric.
    'mother_maiden': re.sub(r'\d+', "", patient_data['extension'][2]['valueString']),

    # Extract the value of the "city" field within the "valueAddress" field of the "extension" array.
    'birth_city': patient_data['extension'][4]['valueAddress']['city'],

    # Extract the value of the "state" field within the "valueAddress" field of the "extension" array.
    'birth_state': patient_data['extension'][4]['valueAddress']['state'],

    # Extract the value of the "country" field within the "valueAddress" field of the "extension" array.
    'birth_country': patient_data['extension'][4]['valueAddress']['country'],

    # Extract the value of the "ethnicity" extension within the "extension" array of the patient data.
    'ethnicity': patient_data['extension'][1]['extension'][1]['valueString'],

    # Extract the value of the "race" extension within the "extension" array of the patient data.
    'race': patient_data['extension'][0]['extension'][1]['valueString']
    }

    return results_dict


# write an address parser which takes the address dict and returns a dictionary of the clean address data
def address_parser(patient_parsed: Patient) -> dict:
    """Parses the address json and returns a dictionary of the address data"""
    
    # Get the address data from the patient data
    address_data = patient_parsed.address[0]
    
    # Make a dictionary to store the address data
    address_dict = {
        "UUID": patient_parsed.id,
        # Get the first line of the address
        "line": address_data.line[0],
        # Get the city 
        "city": address_data.city,
        # Get the state 
        "state": address_data.state,
        # Get the postal code
        "postal_code": address_data.postalCode,
        # Get the country address
        "country": address_data.country
        }
        
    return address_dict

def extract_from_parsed(patient_parsed: Patient) -> dict:
    """Extracts the useful data from the patient data from parsed FHIR patient object"""
    # Get all the keys from the patient data.
    keys = patient_parsed.dict().keys()
    
    # Delete the "resourceType" key.
    keys = [key for key in keys if key != "resourceType"]
    
    # Build a dictionary to store the patient data - this will work with some of the keys but not all.
    pat_dict = {
    "UUID": patient_parsed.id,
    
    # Extract the given name of the patient. Use regex to drop numeric.
    "given_name": re.sub(r'\d+', "", patient_parsed.name[0].given[0]),

    # Extract the family name of the patient. Use regex to drop numeric.
    "family_name": re.sub(r'\d+', "", patient_parsed.name[0].family),

    # Extract the marital status of the patient from the "maritalStatus" field in the patient data.
    "marital_status": patient_parsed.maritalStatus.text,

    # Extract the gender of the patient from the "gender" field in the patient data.
    "gender": patient_parsed.gender,

    # Extract the birthdate of the patient from the "birthDate" field in the patient data.
    "birthdate": patient_parsed.birthDate,

    }
    
    return pat_dict


# define function to take list of patient data in json format and return a list of dictionaries of the patient data
def parse_patient_data(json_files) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    
    # Make 3 lists to store the various dictionaries of data
    pid_data_lst = [None] * len(json_files)
    birth_race_data_lst = [None] * len(json_files)
    address_data_lst = [None] * len(json_files)
    
    for i, patient_json in enumerate(json_files):
        # Extract the birth and race data into a dictionary
        birth_race_data = extract_from_json(patient_json)
        
        # Parse the patient data using fhiry.
        parsed_patient = Patient.parse_obj(patient_json)
        # Extract the useful data from the patient data
        pid_data = extract_from_parsed(parsed_patient)
        
        # Get the address data
        address_data = address_parser(parsed_patient)
        
        # Log progress through loop
        logger.info(f"Parsed patient {i} of {len(json_files)}")
    
        # Smash all the dictionaries into lists
        pid_data_lst[i] = pid_data
        birth_race_data_lst[i] = birth_race_data
        address_data_lst[i] = address_data
        
    return pid_data_lst, birth_race_data_lst, address_data_lst

# define function to take list of dictions and return pandas dataframe
def df_maker(data_list: List[Dict]) -> pd.DataFrame:
    """Takes a list of dictionaries and returns a pandas dataframe"""
    return pd.DataFrame(data_list)
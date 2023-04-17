"""
    Test scripts for data_ingest
"""

import os

from src.data_ingest import read_patient_records

# Change directory to the root of the project
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_read_patient_records():
    # Define a temporary JSON file with test data
    import tempfile
    import json
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(json.dumps({
            "entry": [{
                "resource": {
                    "id": "1",
                    "name": {"family": "Westwood", "given": ["James"]},
                    "gender": "male",
                    "birthDate": "1970-01-01"
                }
            }]
        }))
        test_file = f.name

    # Call the function with the temporary file
    result = read_patient_records([test_file])

    # Check that the result is a list with one item
    assert isinstance(result, list)
    assert len(result) == 1

    # Check that the item is a dictionary with the expected keys
    patient_json = result[0]
    assert isinstance(patient_json, dict)
    assert set(patient_json.keys()) == {"id", "name", "gender", "birthDate"}

    # Check that the values are correct
    assert patient_json["id"] == "1"
    assert patient_json["name"]["family"] == "Westwood"
    assert patient_json["name"]["given"] == ["James"]
    assert patient_json["gender"] == "male"
    assert patient_json["birthDate"] == "1970-01-01"

    # Remove the temporary file
    import os
    os.unlink(test_file)

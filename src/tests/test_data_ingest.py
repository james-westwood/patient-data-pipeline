"""
    Test scripts for data_ingest
"""

from src.data_ingest import read_patient_records

def test_read_patient_records():
    # Define a temporary JSON file with test data
    import tempfile
    import json
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(json.dumps({
            "entry": [{
                "resource": {
                    "id": "1",
                    "name": {"family": "Doe", "given": ["John"]},
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
    assert patient_json["name"]["family"] == "Doe"
    assert patient_json["name"]["given"] == ["John"]
    assert patient_json["gender"] == "male"
    assert patient_json["birthDate"] == "1970-01-01"

    # Remove the temporary file
    import os
    os.unlink(test_file)

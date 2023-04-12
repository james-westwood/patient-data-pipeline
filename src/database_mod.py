"""Module for database data insertion to the database."""


import duckdb as db
import os

# define data out folder
data_out = "data/data_out"
parquet_file = "data/data_out/patient_data.parquet"

def read_parquet(parquet_file=parquet_file):
    "Read parquet file into a duckdb.DuckDBPyRelation."
    db_obj = db.read_parquet(parquet_file)
    return db_obj


def check_parquet(check_path=parquet_file):
    "Check if parquet file exists."
    exists = os.path.isfile(check_path)
    return exists
    
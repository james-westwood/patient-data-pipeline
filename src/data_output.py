"""Module to write out data"""

parquet_file = "data/data_out/patient_data.parquet"

# define a function to write duckdb.DuckDBPyRelation out to parquet
def write_to_parquet(db_obj, outpath=parquet_file):
    "Write duckdb.DuckDBPyRelation to parquet."
    db_obj.df().to_parquet(outpath)
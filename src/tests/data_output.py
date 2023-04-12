# define a function to write duckdb.DuckDBPyRelation out to parquet
def write_to_parquet(db_obj, outpath=data_out):
    "Write duckdb.DuckDBPyRelation to parquet."
    db_obj.df().to_parquet(outpath)
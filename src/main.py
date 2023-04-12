import data_ingest as di
import data_parsing as dp
import database_mod as dm
import data_output as do
import duckdb as db
import streamlit as st

if __name__ == '__main__':
    
    # First check if the parquet file exists
    parquet_file = dm.check_parquet()
    if not parquet_file:
        # Then parse all records from json files
        all_records = di.read_patient_records(di.json_files)
        # Parse all_records
        pid_data, birth_data, address_data = dp.parse_patient_data(all_records)
        
        # Make dataframes
        pid_df_1 = dp.df_maker(pid_data)
        pid_df_2 = dp.df_maker(birth_data)
        address_df = dp.df_maker(address_data)
        
        # join the pid_df_1, pid_df_2 and address_df using duckdb
        pid_db = db.sql("""SELECT * FROM pid_df_1 
                        JOIN pid_df_2 ON pid_df_1.UUID = pid_df_2.UUID 
                        JOIN address_df ON pid_df_1.UUID = address_df.UUID""")
        # write the pid_db to parquet
        dm.write_to_parquet(pid_db)
    else:
        # Read the parquet file into a duckdb relation
        pid_db = dm.read_parquet()
    
    # Make a connection to the database
    conn = db.connect("data/database/patient_data.db", read_only=False)
    
    conn.execute("""SELECT COUNT(*)
                FROM 'data/data_out/patient_data.parquet'
                """).fetchall()
    
    print(pid_db)

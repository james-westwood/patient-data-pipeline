import data_ingest as di
import data_parsing as dp
import duckdb as db

if __name__ == '__main__':
    all_records = di.read_patient_records(di.json_files)
    # Parse all_records
    pid_data, birth_data, address_data = dp.parse_patient_data(all_records)
    
    # Make dataframes
    pid_df_1 = dp.df_maker(pid_data)
    pid_df_2 = dp.df_maker(birth_data)
    address_df = dp.df_maker(address_data)
    
    # join the pid_df_1, pid_df_2 and address_df using duckdb
    pid_df = db.sql("""SELECT * FROM pid_df_1 
                       JOIN pid_df_2 ON pid_df_1.UUID = pid_df_2.UUID 
                       JOIN address_df ON pid_df_1.UUID = address_df.UUID""")

    
    print(pid_df)

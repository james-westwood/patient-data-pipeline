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
        pid_df = dp.df_maker(pid_data)
        birth_df = dp.df_maker(birth_data)
        address_df = dp.df_maker(address_data)
             
        # Make a connection to the database
        conn = db.connect("data/database/patient_data.db", read_only=False)
        
        # Write each df to sql table
        conn.execute('CREATE OR REPLACE TABLE pid_data_table AS SELECT * FROM pid_df')
        conn.execute('CREATE OR REPLACE TABLE birth_data_table AS SELECT * FROM birth_df')
        conn.execute('CREATE OR REPLACE TABLE address_data_table AS SELECT * FROM address_df')
        
        # join the pid_df_1, pid_df_2 and address_df using duckdb
        conn.sql("""CREATE TABLE all_PID_records AS SELECT *
                    FROM pid_data_table""")
        
       
        

    # Make a connection to the database
    conn = db.connect("data/database/patient_data.db", read_only=False)
    
    # Get the data as a dataframe
    pat_dat_df = conn.execute("SELECT * FROM patient_data").df()


    # Create a streamlit app
    st.set_page_config(layout="wide")
    
    st.title('Testing')
    
    st.write('Testing write')  
    
    # st.subheader("City filter")
    
    # Display the table
    st.dataframe(pat_dat_df)
    
    # col_a1, col_a2 = st.columns(2)  
    
    # with col_a1: 
    #     birth_cities_df = conn.execute("""
    #     SELECT 
    #         DISTINCT birthCity 
    #     FROM patient_data 
    #     ORDER BY birthCity
    # """).df()
    
    # with col_a2:
    #     startingAirports_df = conn.execute("""
    #     SELECT 
    #         DISTINCT city 
    #     FROM patient_data 
    #     ORDER BY city
    # """).df()
        
    # birthcityselect = st.selectbox('Birth City', birth_cities_df)
    # livecityselect = st.selectbox('Live City', startingAirports_df)
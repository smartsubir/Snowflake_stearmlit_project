# data_processing.py
import pandas as pd
import snowflake.connector

def load_data_from_snowflake(username, password, account, warehouse, database, schema, table):
    try:
        conn = snowflake.connector.connect(
            user=username,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        query = f"SELECT * FROM {table}"
        print(f"Executing Snowflake Query: {query}")
        df = pd.read_sql(query, conn)
        
        print("Fetched Data:")
        print(df)

        return df

    except snowflake.connector.errors.Error as e:
        # Print detailed error information
        print(f"Snowflake Error: {e}")
        print(f"SQL State: {e.sqlstate}")
        print(f"Error Code: {e.errno}")
        print(f"Message: {e.msg}")

    # Perform other analysis tasks as needed
    # ...

# if __name__ == "__main__":
#     # Example usage
#     file_path = "c:/Users/smart/Downloads/Swachh_Bharat_Mission.csv"
#     data = load_data(file_path)
#     perform_eda(data)
# streamlit_app.py
import streamlit as st
import data_processing
import machine_learning  # Include if applicable
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    st.title("Subir's Streamlit App")
    st.title("Public Health Data Exploration")

    # Streamlit Widgets for User Input
    username = 'SUBIRBHAKAT'
    password = 'Snowflake#2024'
    account = 'yabudoa-ms15731'
    warehouse = st.text_input("Enter Snowflake Warehouse:")
    database = st.text_input("Enter Snowflake Database:")
    schema = st.text_input("Enter Snowflake Schema:")
    table = st.text_input("Enter Snowflake Table:")
    # warehouse = 'COMPUTE_WH'
    # database = 'SNOWFLAKE_DB'
    # schema = 'SNOWFLAKE_SCHEMA'
    # table = 'SWACHH_BHARAT_MISSION'

    # Load Data
    if st.button("Load Data"):
        df = data_processing.load_data_from_snowflake(username, password, account, warehouse, database, schema, table)

        # Display Data
        if df is not None:
            st.write("### Raw Data")
            st.dataframe(df)
            # Perform Exploratory Data Analysis (EDA)
            st.write("### Exploratory Data Analysis (EDA)")

            # Display summary statistics
            st.write("#### Summary Statistics:")
            st.write(df.describe())

            # Display the first few rows of the DataFrame
            st.write("#### First Few Rows:")
            st.write(df.head())

            st.write("#### Shape of dataset:")
            st.write(df.shape)

            st.write("#### Check missing values:")
            st.write(df.isna().sum())

            st.write("#### Check Duplicates:")
            st.write(df.duplicated().sum())

            st.write("#### Checking the number of unique values of each column:")
            st.write(df.nunique())

            st.write("#### Check Null values:")
            st.write(df.info())

            # group bar chart for states
            st.write("#### Check IHHL Total ACH for each State:")
            grouped_data = df[['STATENAME', 'IHHLTOTALACH']]
            # Group by StateName and sum IHHLTOTALACH
            grouped_data = grouped_data.groupby('STATENAME')['IHHLTOTALACH'].sum().reset_index()
            # Plot the grouped bar chart
            st.bar_chart(grouped_data.set_index('STATENAME'))

            # group bar chart Dis
            st.write("#### Check IHHL Total ACH for each District:")
            grouped_data = df[['DISTRICTNAME', 'IHHLTOTALACH']]
            # Group by StateName and sum IHHLTOTALACH
            grouped_data = grouped_data.groupby('DISTRICTNAME')['IHHLTOTALACH'].sum().reset_index()
            # Plot the grouped bar chart
            st.bar_chart(grouped_data.set_index('DISTRICTNAME'))

            # Pie chart
            st.write("### Pie Chart Example")

            # Assuming your DataFrame has a column 'StateName'
            pie_data = df['STATENAME'].value_counts()

            # Plot the pie chart
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the pie chart using st.pyplot()
            st.pyplot(fig)
            
            st.write("#### Removing unwanted columns:")
            df2= df.drop('STATENAME', axis=1)
            df3= df2.drop('DISTRICTNAME', axis=1)
            df = df3
            st.write(df)

            st.write("### Removing outliers")
            Q1 = df['DISTRICTID'].quantile(0.25)
            Q3 = df['DISTRICTID'].quantile(0.75)

            IQR = Q3 - Q1

            low_lim = Q1 - 1.5 * IQR
            high_lim = Q3 + 1.5 * IQR

            df2 = df[(df['DISTRICTID'] > low_lim) & (df['DISTRICTID'] < high_lim)]

            df=df2
            st.write(df.describe())

            
            # Add Machine Learning Predictions (Optional)
            st.write("### Machine Learning Prediction")

            # Train the model
            model = machine_learning.train_predictive_model(df)

            # Streamlit Widget for Features (assumed columns for prediction)
            
            features = [20.0, 40.0, 60.0, 80.0, 100.0]  # Replace with your actual feature values

            # Make a prediction using the trained model
            prediction = model.predict([features])[0]

            st.write(f"Predicted IHHLTOTALACH: {prediction}")

if __name__ == "__main__":
    main()
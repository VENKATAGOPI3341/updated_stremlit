import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# Function to connect to the database
def connect_to_database():
    endpoint = "sql6.freemysqlhosting.net"
    username = "sql6699766"
    password = "4rs3qNccCu"
    database = "sql6699766"
    connection = mysql.connector.connect(
        host=endpoint,
        user=username,
        password=password,
        database=database
    )
    cursor = connection.cursor()
    return connection, cursor

# Fetch data from MySQL database
def fetch_data(query):
    connection, cursor = connect_to_database()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def main():
    st.title("Placement Dashboard")
    
    # Sidebar
    st.sidebar.title("Placement Dashboard")
    department = st.sidebar.selectbox("Select Department", ['RADIOLOGY', 'OPTOMETRY', 'FORENSIC'])

    # Fetch data based on department
    query = f"SELECT Name, Branch, CGPA, Placed, Package, Backlogs FROM placement_data WHERE Branch = '{department}'"
    data = fetch_data(query)
    filtered_data = pd.DataFrame(data, columns=['Name', 'Branch', 'CGPA', 'Placed', 'Package', 'Backlogs'])

    # Main content
    st.write(f"### {department} Placement Dashboard")

    st.write("### Placed vs Unplaced Students")
    placement_chart = px.histogram(filtered_data, x='Placed', color='Placed', title="Placed vs Unplaced Students")
    st.plotly_chart(placement_chart)

    # Calculate the counts of placed and unplaced students
    placement_counts = filtered_data['Placed'].value_counts().reset_index()
    placement_counts.columns = ['Status', 'Count']

    # Plot a pie chart based on placed and unplaced students
    fig = px.pie(placement_counts, values='Count', names='Status', title='Placed vs Unplaced Students')
    st.plotly_chart(fig)

    st.write("### Number of Backlogs of Placed Students")
    placed_backlogs_chart = px.histogram(filtered_data[filtered_data['Placed'] == 'Yes'], x='Backlogs', title="Number of Backlogs of Placed Students")
    st.plotly_chart(placed_backlogs_chart)

    st.write("### Package Distribution by Branch")
    package_by_branch_chart = px.box(filtered_data, x='Branch', y='Package', title="Package Distribution by Branch")
    st.plotly_chart(package_by_branch_chart)

    st.write("### Scatter Plot: CGPA vs Package")
    scatter_plot = px.scatter(filtered_data, x='CGPA', y='Package', color='Placed', 
                              title="Scatter Plot: CGPA vs Package", 
                              labels={'CGPA': 'CGPA', 'Package': 'Package (in Lakhs)'})
    st.plotly_chart(scatter_plot)

if __name__ == "__main__":
    main()
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
    query = f"SELECT Name, Branch, CGPA, Placed, package, Backlogs FROM placement_data WHERE Branch = '{department}'"
    data = fetch_data(query)
    filtered_data = pd.DataFrame(data, columns=['Name', 'Branch', 'CGPA', 'Placed', 'package', 'Backlogs'])
    
    # Main content
    st.write(f"### {department} Placement Dashboard")
    # Define the layout using Streamlit columns with adjusted width
    col1, col2 = st.columns([1 ,  1])
    col3, col4 = st.columns([1, 1])

    col1.write("### Placed vs Unplaced Students")
    placement_chart = px.histogram(filtered_data, x='Placed', color='Placed',color_discrete_sequence=['red'])
    col1.plotly_chart(placement_chart)
    col1.write("")  # Add empty space

    # Calculate the counts of placed and unplaced students
    placement_counts = filtered_data['Placed'].value_counts().reset_index()
    placement_counts.columns = ['Status', 'Count']
    
    col2.write("### Placed vs Unplaced Students")
    # Plot a pie chart based on placed and unplaced students
    fig = px.pie(placement_counts, values='Count', names='Status',color_discrete_sequence=['blue', 'red'])
    col2.plotly_chart(fig)
    col2.write("")  # Add empty space

    col3.write("### Number of Backlogs of Placed Students")
    placed_backlogs_chart = px.histogram(filtered_data[filtered_data['Placed'] == 'Yes'], x='Backlogs',color_discrete_sequence=['blue'])
    col3.plotly_chart(placed_backlogs_chart)
    col3.write("")  # Add empty space

    col4.write("### Package Distribution by Branch")
    package_by_branch_chart = px.box(filtered_data, x='Branch', y='package',color_discrete_sequence=['red'])
    col4.plotly_chart(package_by_branch_chart)
    col4.write("")  # Add empty space

    st.write("### Scatter Plot: CGPA vs Package")
    scatter_plot = px.scatter(filtered_data, x='CGPA', y='package', color='Placed',
                              color_discrete_sequence=['blue', 'red'], 
                              labels={'CGPA': 'CGPA', 'package': 'Package (in Lakhs)'})
    st.plotly_chart(scatter_plot)
    st.write("")  # Add empty space

if __name__ == "__main__":
    main()
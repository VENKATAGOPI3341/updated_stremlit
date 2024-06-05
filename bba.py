import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
# Get a list of bright colors from Plotly Express
bright_colors = px.colors.qualitative.Light24

# Define the color for all bars
single_color = ['violet']
st.set_page_config(page_title="BBA", page_icon="", layout="wide")

# Function to connect to the database
def connect_to_database():
    endpoint = "sql12.freemysqlhosting.net"
    username = "sql12711956"
    password = "lfjhjlxg6j"
    database = "sql12711956"
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

# Main function to display the dashboard
def main():
    st.title("Placement Dashboard for BBA Students")

    # Define the layout using Streamlit columns with adjusted width
    col1, col2, col3 = st.columns([1, 1, 1])
    col4, col5, col6 = st.columns([1, 1, 1])

    # Fetch data for placed and unplaced students in the CSE branch
    query_cse_placed_unplaced = "SELECT Placed, COUNT(*) AS Count FROM placement_data WHERE Branch = 'BBA' GROUP BY Placed"
    cse_placed_unplaced_data = fetch_data(query_cse_placed_unplaced)

    # Create DataFrame for CSE branch
    df_cse_placed_unplaced = pd.DataFrame(cse_placed_unplaced_data, columns=['Placed', 'Count'])


    # Visualize the data with a pie chart
    fig_cse_placed_unplaced_pie = px.pie(df_cse_placed_unplaced, values='Count', names='Placed', title='Placement Status for BBA Branch')
    fig_cse_placed_unplaced_pie.update_traces(marker=dict(colors=['pink', 'violet']))
    col1.plotly_chart(fig_cse_placed_unplaced_pie, use_container_width=True)
    col1.write("")  # Add empty space

    
    # Define the query to fetch data for Company Placement Bar Chart
    query_company_placement = """
        SELECT Company_placed, COUNT(*) AS Placement_Count
        FROM placement_data
        WHERE Branch = 'BBA' AND Placed = 'Yes' AND Company_placed IS NOT NULL
        GROUP BY Company_placed
    """
    # Fetch data for Company Placement Bar Chart
    company_placement_data = fetch_data(query_company_placement)
    # Create DataFrame for Company Placement Bar Chart
    df_company_placement = pd.DataFrame(company_placement_data, columns=['Company_placed', 'Placement_Count'])

    
    # Visualize the data with a horizontal bar chart
    fig_company_placement_bar_horizontal = px.bar(df_company_placement, y='Company_placed', x='Placement_Count', 
                                                   title='Company-wise Placement Count for ECE Department',
                                                   labels={'Company_placed': 'Company', 'Placement_Count': 'Placement Count'},
                                                   color='Company_placed',
                                                   orientation='h',
                                                   color_discrete_sequence=bright_colors)
    col2.plotly_chart(fig_company_placement_bar_horizontal, use_container_width=True)

    

    # Query to fetch data for students with backlogs, from CSE department, and with a package
    query = """
            SELECT Name, Branch, Package 
            FROM placement_data 
            WHERE Backlogs > 0 AND Branch = 'BBA' AND Package IS NOT NULL
        """
    backlog_cse_package_data = fetch_data(query)

    # Create DataFrame from fetched data
    df_backlog_cse_package = pd.DataFrame(backlog_cse_package_data, columns=['Name', 'Branch', 'Package'])

    # Visualize the data with a scatter plot
    fig_backlog_cse_package = px.scatter(df_backlog_cse_package, x='Name', y='Package', color='Branch',
                                         title='Packages for BBA Branch with Backlogs',
                                         labels={'Name': 'Student Name', 'Package': 'Package Amount'},
                                         hover_name='Name',
                                         color_discrete_sequence=bright_colors)
    fig_backlog_cse_package.update_traces(marker=dict(size=12))
    fig_backlog_cse_package.update_layout(showlegend=True)
    col3.plotly_chart(fig_backlog_cse_package, use_container_width=True)
    col3.write("")  # Add empty space
   
    # Define the query to fetch data for Domain Count Bar Chart
    query_domain_count = """
        SELECT Domain, COUNT(*) AS Count 
        FROM placement_data 
        WHERE Branch = 'BBA' 
        GROUP BY Domain
    """

    # Fetch data for Domain Count Bar Chart
    domain_count_data = fetch_data(query_domain_count)

    # Create DataFrame for Domain Count Bar Chart
    df_domain_count = pd.DataFrame(domain_count_data, columns=['Domain', 'Count'])

   

    # Visualize the data with a bar chart
    fig_domain_count_bar = px.bar(df_domain_count, x='Domain', y='Count', 
                                  title='Domain-wise Student Count for BBA Department',
                                  labels={'Domain': 'Domain', 'Count': 'Student Count'},
                                  color='Domain',
                                  color_discrete_sequence=single_color)
                                 
    col4.plotly_chart(fig_domain_count_bar, use_container_width=True)
    col4.write("")  # Add empty space


    # Fetch data for Package vs. CGPA Scatter Plot
    query_package_cgpa = """
        SELECT CGPA, Package
        FROM placement_data
        WHERE Branch = 'ECE' AND Placed = 'Yes' AND CGPA IS NOT NULL AND Package IS NOT NULL
    """
    package_cgpa_data = fetch_data(query_package_cgpa)

    # Create DataFrame for Package vs. CGPA Scatter Plot
    df_package_cgpa = pd.DataFrame(package_cgpa_data, columns=['CGPA', 'Package'])

    # Visualize the data with a scatter plot
    fig_package_cgpa_scatter = px.scatter(df_package_cgpa, x='CGPA', y='Package', 
                                          title='Package vs. CGPA for Placed Students in ECE Department',
                                          labels={'CGPA': 'CGPA', 'Package': 'Package Amount'},
                                          trendline='ols',
                                          color_discrete_sequence=bright_colors)
    col5.plotly_chart(fig_package_cgpa_scatter, use_container_width=True)
    col5.write("")  # Add empty space

    # Fetch data for packages offered to CSE branch students
    query_cse_packages = "SELECT Package FROM placement_data WHERE Branch = 'BBA'"
    cse_packages_data = fetch_data(query_cse_packages)

    # Create DataFrame for CSE branch packages
    df_cse_packages = pd.DataFrame(cse_packages_data, columns=['Package'])


    # Visualize the data with a histogram or box plot
    # Here, I'll use a histogram to show the distribution of packages
    fig_cse_packages_hist = px.histogram(df_cse_packages, x='Package', title='Distribution of Packages for BBA Branch', color_discrete_sequence=["orange"])
    col6.plotly_chart(fig_cse_packages_hist, use_container_width=True)
    col6.write("")  # Add empty space


if __name__ == "__main__":
    main()
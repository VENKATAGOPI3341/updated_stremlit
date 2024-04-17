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
    st.title("Placement Dashboard for Forensic Department")

    # First Row: Placed vs. Unplaced Pie Chart, Packages Distribution Histogram, Domain-wise Student Count Bar Chart
    col1, col2, col3 = st.columns(3)

    # Placed vs. Unplaced Pie Chart
    # Fetch data for placed and unplaced students in the Forensic department
    query_forensic_placed_unplaced = "SELECT Placed, COUNT(*) AS Count FROM placement_data WHERE Branch = 'FORENSIC' GROUP BY Placed"
    forensic_placed_unplaced_data = fetch_data(query_forensic_placed_unplaced)
    # Create DataFrame for Forensic department
    df_forensic_placed_unplaced = pd.DataFrame(forensic_placed_unplaced_data, columns=['Placed', 'Count'])
    # Visualize the data with a pie chart
    fig_forensic_placed_unplaced_pie = px.pie(df_forensic_placed_unplaced, values='Count', names='Placed', title='Placement Status for FORENSIC Department')
    fig_forensic_placed_unplaced_pie.update_traces(marker=dict(colors=['red', 'yellow']))
    col1.plotly_chart(fig_forensic_placed_unplaced_pie, use_container_width=True)

    # Packages Distribution Histogram
    # Fetch data for packages offered to Forensic department students
    query_forensic_packages = "SELECT Package FROM placement_data WHERE Branch = 'FORENSIC'"
    forensic_packages_data = fetch_data(query_forensic_packages)
    # Create DataFrame for Forensic department packages
    df_forensic_packages = pd.DataFrame(forensic_packages_data, columns=['Package'])
    # Visualize the data with a histogram
    fig_forensic_packages_hist = px.histogram(df_forensic_packages, x='Package', title='Distribution of Packages for FORENSIC Department', color_discrete_sequence=['grey'])
    col2.plotly_chart(fig_forensic_packages_hist, use_container_width=True)

    # Domain-wise Student Count Bar Chart
    # Define the query to fetch data for Domain Count Bar Chart
    query_domain_count = """
        SELECT Domain, COUNT(*) AS Count 
        FROM placement_data 
        WHERE Branch = 'FORENSIC' 
        GROUP BY Domain
    """
    # Fetch data for Domain Count Bar Chart
    domain_count_data = fetch_data(query_domain_count)
    # Create DataFrame for Domain Count Bar Chart
    df_domain_count = pd.DataFrame(domain_count_data, columns=['Domain', 'Count'])
    # Visualize the data with a bar chart
    fig_domain_count_bar = px.bar(df_domain_count, x='Domain', y='Count', 
                                  title='Domain-wise Student Count for FORENSIC Department',
                                  labels={'Domain': 'Domain', 'Count': 'Student Count'},
                                  color='Domain')
    col3.plotly_chart(fig_domain_count_bar, use_container_width=True)

    # Second Row: Package vs. CGPA Scatter Plot, Company-wise Placement Count Horizontal Bar Chart, Scatter Plot of Students with Backlogs and Package
    col4, col5, col6 = st.columns(3)

    # Package vs. CGPA Scatter Plot
    # Define the query to fetch data for Package vs. CGPA Scatter Plot
    query_package_cgpa = """
        SELECT CGPA, Package
        FROM placement_data
        WHERE Branch = 'FORENSIC' AND Placed = 'Yes' AND CGPA IS NOT NULL AND Package IS NOT NULL
    """
    # Fetch data for Package vs. CGPA Scatter Plot
    package_cgpa_data = fetch_data(query_package_cgpa)
    # Create DataFrame for Package vs. CGPA Scatter Plot
    df_package_cgpa = pd.DataFrame(package_cgpa_data, columns=['CGPA', 'Package'])
    # Visualize the data with a scatter plot
    fig_package_cgpa_scatter = px.scatter(df_package_cgpa, x='CGPA', y='Package', 
                                          title='Package vs. CGPA for Placed Students in Forensic Department',
                                          labels={'CGPA': 'CGPA', 'Package': 'Package Amount'},
                                          trendline='ols')
    col4.plotly_chart(fig_package_cgpa_scatter, use_container_width=True)

    # Company-wise Placement Count Horizontal Bar Chart
    # Define the query to fetch data for Company Placement Bar Chart
    query_company_placement = """
        SELECT Company_placed, COUNT(*) AS Placement_Count
        FROM placement_data
        WHERE Branch = 'FORENSIC' AND Placed = 'Yes' AND Company_placed IS NOT NULL
        GROUP BY Company_placed
    """
    # Fetch data for Company Placement Bar Chart
    company_placement_data = fetch_data(query_company_placement)
    # Create DataFrame for Company Placement Bar Chart
    df_company_placement = pd.DataFrame(company_placement_data, columns=['Company_placed', 'Placement_Count'])
    # Visualize the data with a horizontal bar chart
    fig_company_placement_bar_horizontal = px.bar(df_company_placement, y='Company_placed', x='Placement_Count', 
                                                   title='Company-wise Placement Count for FORENSIC Department',
                                                   labels={'Company_placed': 'Company', 'Placement_Count': 'Placement Count'},
                                                   color='Company_placed',
                                                   orientation='h')
    col5.plotly_chart(fig_company_placement_bar_horizontal, use_container_width=True)

    # Scatter Plot of Students with Backlogs and Package
    # Query to fetch data for students with backlogs, from Forensic department, and with a package
    query_backlog_forensic_package = """
            SELECT Name, Package 
            FROM placement_data 
            WHERE Backlogs > 0 AND Branch = 'FORENSIC' AND Package IS NOT NULL
        """
    backlog_forensic_package_data = fetch_data(query_backlog_forensic_package)
    # Create DataFrame from fetched data
    df_backlog_forensic_package = pd.DataFrame(backlog_forensic_package_data, columns=['Name', 'Package'])
    # Visualize the data with a scatter plot
    fig_backlog_forensic_package = px.scatter(df_backlog_forensic_package, x='Name', y='Package',
                                              title='Packages for Forensic Department with Backlogs',
                                              labels={'Name': 'Student Name', 'Package': 'Package Amount'},
                                              hover_name='Name')
    fig_backlog_forensic_package.update_traces(marker=dict(size=12))
    fig_backlog_forensic_package.update_layout(showlegend=False)
    col6.plotly_chart(fig_backlog_forensic_package, use_container_width=True)

if __name__ == "__main__":
    main()  

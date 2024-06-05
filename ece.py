import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

st.set_page_config(page_title="CSE", page_icon="", layout="wide")

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
    st.title("Placement Dashboard for ECE Students")

    # Define the layout using Streamlit columns with adjusted width
    col1, col2, col3 = st.columns([1, 1, 1])
    col4, col5, col6 = st.columns([1, 1, 1])

    # Fetch data for placed and unplaced students in the ECE branch
    query_ece_placed_unplaced = "SELECT Placed, COUNT(*) AS Count FROM placement_data WHERE Branch = 'ECE' GROUP BY Placed"
    ece_placed_unplaced_data = fetch_data(query_ece_placed_unplaced)

    # Create DataFrame for ECE branch
    df_ece_placed_unplaced = pd.DataFrame(ece_placed_unplaced_data, columns=['Placed', 'Count'])

    # Visualize the data with a pie chart
    fig_ece_placed_unplaced_pie = px.pie(df_ece_placed_unplaced, values='Count', names='Placed', title='Placement Status for ECE Branch')
    fig_ece_placed_unplaced_pie.update_traces(marker=dict(colors=['aqua', 'red']))
    col1.plotly_chart(fig_ece_placed_unplaced_pie, use_container_width=True)
    col1.write("")  # Add empty space

    # Fetch data for packages offered to ECE branch students
    query_ece_packages = "SELECT Package FROM placement_data WHERE Branch = 'ECE'"
    ece_packages_data = fetch_data(query_ece_packages)

    # Create DataFrame for ECE branch packages
    df_ece_packages = pd.DataFrame(ece_packages_data, columns=['Package'])

    # Visualize the data with a histogram or box plot
    # Here, I'll use a histogram to show the distribution of packages
    fig_ece_packages_hist = px.histogram(df_ece_packages, x='Package', title='Distribution of Packages for ECE Branch', color_discrete_sequence=['purple'])
    col2.plotly_chart(fig_ece_packages_hist, use_container_width=True)
    col2.write("")  # Add empty space

    # Fetch data for Domain Count Bar Chart
    query_domain_count = """
        SELECT Domain, COUNT(*) AS Count 
        FROM placement_data 
        WHERE Branch = 'ECE' 
        GROUP BY Domain
    """
    domain_count_data = fetch_data(query_domain_count)

    # Create DataFrame for Domain Count Bar Chart
    df_domain_count = pd.DataFrame(domain_count_data, columns=['Domain', 'Count'])

    # Visualize the data with a bar chart
    fig_domain_count_bar = px.bar(df_domain_count, x='Domain', y='Count', 
                                  title='Domain-wise Student Count for ECE Department',
                                  labels={'Domain': 'Domain', 'Count': 'Student Count'},
                                  color='Domain')
    col3.plotly_chart(fig_domain_count_bar, use_container_width=True)
    col3.write("")  # Add empty space

    # Fetch data for students with backlogs, from ECE department, and with a package
    query_backlog_ece_package = """
            SELECT Name, Branch, Package 
            FROM placement_data 
            WHERE Backlogs > 0 AND Branch = 'ECE' AND Package IS NOT NULL
        """
    backlog_ece_package_data = fetch_data(query_backlog_ece_package)

    # Create DataFrame from fetched data
    df_backlog_ece_package = pd.DataFrame(backlog_ece_package_data, columns=['Name', 'Branch', 'Package'])

    # Visualize the data with a scatter plot
    fig_backlog_ece_package = px.scatter(df_backlog_ece_package, x='Name', y='Package', color='Branch',
                                         title='Packages for ECE Branch with Backlogs',
                                         labels={'Name': 'Student Name', 'Package': 'Package Amount'},
                                         hover_name='Name')
    fig_backlog_ece_package.update_traces(marker=dict(size=12))
    fig_backlog_ece_package.update_layout(showlegend=True)
    col4.plotly_chart(fig_backlog_ece_package, use_container_width=True)
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
                                          trendline='ols')
    col5.plotly_chart(fig_package_cgpa_scatter, use_container_width=True)
    col5.write("")  # Add empty space

    # Fetch data for Company Placement Bar Chart
    query_company_placement = """
        SELECT Company_placed, COUNT(*) AS Placement_Count
        FROM placement_data
        WHERE Branch = 'ECE' AND Placed = 'Yes' AND Company_placed IS NOT NULL
        GROUP BY Company_placed
    """
    company_placement_data = fetch_data(query_company_placement)

    # Create DataFrame for Company Placement Bar Chart
    df_company_placement = pd.DataFrame(company_placement_data, columns=['Company_placed', 'Placement_Count'])
    
    # Visualize the data with a horizontal bar chart
    fig_company_placement_bar_horizontal = px.bar(df_company_placement, y='Company_placed', x='Placement_Count', 
                                                   title='Company-wise Placement Count for ECE Department',
                                                   labels={'Company_placed': 'Company', 'Placement_Count': 'Placement Count'},
                                                   color='Company_placed',
                                                   orientation='h')
    col6.plotly_chart(fig_company_placement_bar_horizontal, use_container_width=True)

if __name__ == "__main__":
    main()

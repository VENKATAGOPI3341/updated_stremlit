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

# Main function to create the dashboard
def main():
    st.title("Placement Dashboard for Mechanical Engineering Students")

    # Fetch data for placed and unplaced students in the Mechanical branch
    query_mech_placed_unplaced = "SELECT Placed, COUNT(*) AS Count FROM placement_data WHERE Branch = 'MECHANICAL' GROUP BY Placed"
    mech_placed_unplaced_data = fetch_data(query_mech_placed_unplaced)
    df_mech_placed_unplaced = pd.DataFrame(mech_placed_unplaced_data, columns=['Placed', 'Count'])

    # Fetch data for packages offered to Mechanical branch students
    query_mech_packages = "SELECT Package FROM placement_data WHERE Branch = 'MECHANICAL'"
    mech_packages_data = fetch_data(query_mech_packages)
    df_mech_packages = pd.DataFrame(mech_packages_data, columns=['Package'])

    # Fetch data for students with backlogs and packages in the Mechanical branch
    query_backlog_mech_package = """
            SELECT Name, Package 
            FROM placement_data 
            WHERE Backlogs > 0 AND Branch = 'MECHANICAL' AND Package IS NOT NULL
        """
    backlog_mech_package_data = fetch_data(query_backlog_mech_package)
    df_backlog_mech_package = pd.DataFrame(backlog_mech_package_data, columns=['Name', 'Package'])

    # Fetch data for domain-wise student count in the Mechanical department
    query_domain_count = """
        SELECT Domain, COUNT(*) AS Count 
        FROM placement_data 
        WHERE Branch = 'MECHANICAL' 
        GROUP BY Domain
    """
    domain_count_data = fetch_data(query_domain_count)
    df_domain_count = pd.DataFrame(domain_count_data, columns=['Domain', 'Count'])

    # Fetch data for package vs. CGPA for placed students in the Mechanical department
    query_package_cgpa = """
        SELECT CGPA, Package
        FROM placement_data
        WHERE Branch = 'MECHANICAL' AND Placed = 'Yes' AND CGPA IS NOT NULL AND Package IS NOT NULL
    """
    package_cgpa_data = fetch_data(query_package_cgpa)
    df_package_cgpa = pd.DataFrame(package_cgpa_data, columns=['CGPA', 'Package'])

    # Fetch data for company-wise placement count in the Mechanical department
    query_company_placement = """
        SELECT Company_placed, COUNT(*) AS Placement_Count
        FROM placement_data
        WHERE Branch = 'MECHANICAL' AND Placed = 'Yes' AND Company_placed IS NOT NULL
        GROUP BY Company_placed
    """
    company_placement_data = fetch_data(query_company_placement)
    df_company_placement = pd.DataFrame(company_placement_data, columns=['Company_placed', 'Placement_Count'])

    # Fetch data for gender-wise unplaced students in the Mechanical branch
    query_gender_unplaced = "SELECT Gender, COUNT(*) AS Count FROM placement_data WHERE Branch = 'MECHANICAL' AND Placed = 'No' GROUP BY Gender"
    gender_unplaced_data = fetch_data(query_gender_unplaced)
    df_gender_unplaced = pd.DataFrame(gender_unplaced_data, columns=['Gender', 'Count'])

    # Fetch data for backlogs analysis in the Mechanical department
    query_backlogs_analysis = """
        SELECT Backlogs, COUNT(*) AS Count
        FROM placement_data
        WHERE Branch = 'MECHANICAL' AND Backlogs > 0
        GROUP BY Backlogs
    """
    backlogs_analysis_data = fetch_data(query_backlogs_analysis)
    df_backlogs_analysis = pd.DataFrame(backlogs_analysis_data, columns=['Backlogs', 'Count'])

    # st.subheader("Placement Status for Mechanical Branch")
    col1, col2, col3 = st.columns(3)
    with col1:
        # st.subheader("Placement Status")
        fig_mech_placed_unplaced_pie = px.pie(df_mech_placed_unplaced, values='Count', names='Placed',title="placement status",color_discrete_sequence=['orange','black'])
        st.plotly_chart(fig_mech_placed_unplaced_pie, use_container_width=True)

    with col2:
        # st.title("Package Distribution")
        fig_mech_packages_hist = px.histogram(df_mech_packages, x='Package',title="package Distribution" ,color_discrete_sequence=['yellow'])
        st.plotly_chart(fig_mech_packages_hist, use_container_width=True)

    with col3:
        # st.subheader("Gender-wise Unplaced Students")
        # Visualize gender-wise distribution of unplaced students with a pie chart
        fig_gender_unplaced_pie = px.pie(df_gender_unplaced, values='Count', names='Gender',title="Gender wise unplaced students", color_discrete_sequence=['blue', 'green'])
        st.plotly_chart(fig_gender_unplaced_pie, use_container_width=True)

    # st.subheader("Domain-wise Student Count for Mechanical Department")
    col4, col5, col6 = st.columns(3)
    with col4:
        # st.subheader("Domain-wise Student Count")
        fig_domain_count_bar = px.bar(df_domain_count, x='Domain', y='Count', 
                                      title='Domain-wise Student Count for Mechanical Department',
                                      labels={'Domain': 'Domain', 'Count': 'Student Count'},
                                      color='Domain',
                                      color_discrete_sequence=['purple'])
        st.plotly_chart(fig_domain_count_bar, use_container_width=True)

    with col5:
        # st.subheader("Package vs. CGPA")
        fig_package_cgpa_scatter = px.scatter(df_package_cgpa, x='CGPA', y='Package', 
                                              title='Package vs. CGPA for Placed Students in Mechanical Department',
                                              labels={'CGPA': 'CGPA', 'Package': 'Package Amount'},
                                              trendline='ols')
        st.plotly_chart(fig_package_cgpa_scatter, use_container_width=True)

    with col6:
        # st.subheader("Company-wise Placement Count")
        fig_company_placement_bar_horizontal = px.bar(df_company_placement, y='Company_placed', x='Placement_Count', 
                                                       title='Company-wise Placement Count for Mechanical Department',
                                                       labels={'Company_placed': 'Company', 'Placement_Count': 'Placement Count'},
                                                       color='Company_placed',
                                                       orientation='h')
        st.plotly_chart(fig_company_placement_bar_horizontal, use_container_width=True)

if __name__ == "__main__":
    main()

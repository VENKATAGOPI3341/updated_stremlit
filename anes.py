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
    st.set_page_config(page_title="Placement Dashboard for Anesthesia Department", page_icon="", layout="wide")

    st.title("Placement Dashboard for Anesthesia Department")

    # Get a list of bright colors from Plotly Express
    bright_colors = px.colors.qualitative.Light24
    color_discrete_sequence = bright_colors

    # First row
    col1, col2, col3 = st.columns(3)

    # Placed vs. Unplaced Pie Chart
    with col1:
        # st.header("Placed vs. Unplaced Pie Chart")
        query_ane_placed_unplaced = "SELECT Placed, COUNT(*) AS Count FROM placement_data WHERE Branch = 'ANESTHSIA' GROUP BY Placed"
        ane_placed_unplaced_data = fetch_data(query_ane_placed_unplaced)
        df_ane_placed_unplaced = pd.DataFrame(ane_placed_unplaced_data, columns=['Placed', 'Count'])
        fig_ane_placed_unplaced_pie = px.pie(df_ane_placed_unplaced, values='Count', names='Placed', title='Placement Status for ANESTHESIA Department', color_discrete_sequence=color_discrete_sequence)
        st.plotly_chart(fig_ane_placed_unplaced_pie, use_container_width=True)

    # Distribution of Packages Histogram
    with col2:
        # st.header("Distribution of Packages Histogram")
        query_ane_packages = "SELECT Package FROM placement_data WHERE Branch = 'ANESTHSIA'"
        ane_packages_data = fetch_data(query_ane_packages)
        df_ane_packages = pd.DataFrame(ane_packages_data, columns=['Package'])
        fig_ane_packages_hist = px.histogram(df_ane_packages, x='Package', title='Distribution of Packages for ANESTHESIA Department', color_discrete_sequence=color_discrete_sequence)
        st.plotly_chart(fig_ane_packages_hist, use_container_width=True)

    # Domain-wise Student Count Bar Chart
    with col3:
        # st.header("Domain-wise Student Count Bar Chart")
        query_domain_count = """
            SELECT Domain, COUNT(*) AS Count 
            FROM placement_data 
            WHERE Branch = 'ANESTHSIA' 
            GROUP BY Domain
        """
        domain_count_data = fetch_data(query_domain_count)
        df_domain_count = pd.DataFrame(domain_count_data, columns=['Domain', 'Count'])
        fig_domain_count_bar = px.bar(df_domain_count, x='Domain', y='Count', 
                                      title='Domain-wise Student Count for ANESTHESIA Department',
                                      labels={'Domain': 'Domain', 'Count': 'Student Count'},
                                      color='Domain', color_discrete_sequence=color_discrete_sequence)
        st.plotly_chart(fig_domain_count_bar, use_container_width=True)

    # Second row
    col4, col5, col6 = st.columns(3)

    # Package vs. CGPA Scatter Plot
    with col4:
        # st.header("Package vs. CGPA Scatter Plot")
        query_package_cgpa = """
            SELECT CGPA, Package
            FROM placement_data
            WHERE Branch = 'ANESTHSIA' AND Placed = 'Yes' AND CGPA IS NOT NULL AND Package IS NOT NULL
        """
        package_cgpa_data = fetch_data(query_package_cgpa)
        df_package_cgpa = pd.DataFrame(package_cgpa_data, columns=['CGPA', 'Package'])
        fig_package_cgpa_scatter = px.scatter(df_package_cgpa, x='CGPA', y='Package', 
                                              title='Package vs. CGPA for Placed Students in Anesthesia Department',
                                              labels={'CGPA': 'CGPA', 'Package': 'Package Amount'},
                                              trendline='ols', color_discrete_sequence=color_discrete_sequence)
        st.plotly_chart(fig_package_cgpa_scatter, use_container_width=True)

    # Company-wise Placement Count Horizontal Bar Chart
    with col5:
        # st.header("Company-wise Placement Count Horizontal Bar Chart")
        query_company_placement = """
            SELECT Company_placed, COUNT(*) AS Placement_Count
            FROM placement_data
            WHERE Branch = 'ANESTHSIA' AND Placed = 'Yes' AND Company_placed IS NOT NULL
            GROUP BY Company_placed
        """
        company_placement_data = fetch_data(query_company_placement)
        df_company_placement = pd.DataFrame(company_placement_data, columns=['Company_placed', 'Placement_Count'])
        fig_company_placement_bar_horizontal = px.bar(df_company_placement, y='Company_placed', x='Placement_Count', 
                                                       title='Company-wise Placement Count for ANESTHESIA Department',
                                                       labels={'Company_placed': 'Company', 'Placement_Count': 'Placement Count'},
                                                       color='Company_placed',
                                                       orientation='h', color_discrete_sequence=color_discrete_sequence)
        st.plotly_chart(fig_company_placement_bar_horizontal, use_container_width=True)

    # Scatter Plot of Students with Backlogs and Package
    with col6:
        # st.header("Scatter Plot of Students with Backlogs and Package")
        query_backlog_forensic_package = """
                SELECT Name, Package 
                FROM placement_data 
                WHERE Backlogs > 0 AND Branch = 'ANESTHSIA' AND Package IS NOT NULL
            """
        backlog_forensic_package_data = fetch_data(query_backlog_forensic_package)
        df_backlog_forensic_package = pd.DataFrame(backlog_forensic_package_data, columns=['Name', 'Package'])
        fig_backlog_forensic_package = px.scatter(df_backlog_forensic_package, x='Name', y='Package',
                                                  title='Packages for Anesthesia Department with Backlogs',
                                                  labels={'Name': 'Student Name', 'Package': 'Package Amount'},
                                                  hover_name='Name', color_discrete_sequence=color_discrete_sequence)
        fig_backlog_forensic_package.update_traces(marker=dict(size=12))
        fig_backlog_forensic_package.update_layout(showlegend=False)
        st.plotly_chart(fig_backlog_forensic_package, use_container_width=True)

if __name__ == "__main__":
    main()

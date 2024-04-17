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
    st.set_page_config(page_title="Placement Dashboard for Optometry Department", page_icon="", layout="wide")

    st.title("Placement Dashboard for Optometry Department")

    # Define custom colors
    custom_colors = ['violet', 'lightgreen', 'orange', 'blue', 'red','green']

    # First row
    col1, col2, col3 = st.columns(3)

    # Placed vs. Unplaced Bar Chart
    with col1:
        query_opt_placed_unplaced = "SELECT Placed, COUNT(*) AS Count FROM placement_data WHERE Branch = 'OPTOMETRY' GROUP BY Placed"
        opt_placed_unplaced_data = fetch_data(query_opt_placed_unplaced)
        df_opt_placed_unplaced = pd.DataFrame(opt_placed_unplaced_data, columns=['Placed', 'Count'])
        fig_opt_placed_unplaced_bar = px.bar(df_opt_placed_unplaced, x='Placed', y='Count', 
                                             title='Placement Status for OPTOMETRY Department', 
                                             color='Placed', color_discrete_sequence=custom_colors)
        st.plotly_chart(fig_opt_placed_unplaced_bar, use_container_width=True)

    # Distribution of CGPA Histogram
    with col2:
        query_cgpa_distribution = "SELECT CGPA FROM placement_data WHERE Branch = 'OPTOMETRY'"
        cgpa_data = fetch_data(query_cgpa_distribution)
        df_cgpa = pd.DataFrame(cgpa_data, columns=['CGPA'])
        fig_cgpa_hist = px.histogram(df_cgpa, x='CGPA', title='Distribution of CGPA for OPTOMETRY Department', 
                                      color_discrete_sequence=custom_colors)
        st.plotly_chart(fig_cgpa_hist, use_container_width=True)

    # Gender-wise Placement Pie Chart
    with col3:
        query_gender_placement = "SELECT Gender, COUNT(*) AS Count FROM placement_data WHERE Branch = 'OPTOMETRY' AND Placed = 'Yes' GROUP BY Gender"
        gender_placement_data = fetch_data(query_gender_placement)
        df_gender_placement = pd.DataFrame(gender_placement_data, columns=['Gender', 'Count'])
        fig_gender_placement_pie = px.pie(df_gender_placement, values='Count', names='Gender', 
                                           title='Gender-wise Placement for OPTOMETRY Department',
                                           color_discrete_sequence=custom_colors)
        st.plotly_chart(fig_gender_placement_pie, use_container_width=True)

    # Second row
    col4, col5, col6 = st.columns(3)

    # Company-wise Placement Count Horizontal Bar Chart
    with col4:
        query_company_placement = """
            SELECT Company_placed, COUNT(*) AS Placement_Count
            FROM placement_data
            WHERE Branch = 'OPTOMETRY' AND Placed = 'Yes' AND Company_placed IS NOT NULL
            GROUP BY Company_placed
        """
        company_placement_data = fetch_data(query_company_placement)
        df_company_placement = pd.DataFrame(company_placement_data, columns=['Company_placed', 'Placement_Count'])
        fig_company_placement_bar_horizontal = px.bar(df_company_placement, y='Company_placed', x='Placement_Count', 
                                                       title='Company-wise Placement Count for OPTOMETRY Department',
                                                       labels={'Company_placed': 'Company', 'Placement_Count': 'Placement Count'},
                                                       color='Company_placed',
                                                       orientation='h', color_discrete_sequence=custom_colors)
        st.plotly_chart(fig_company_placement_bar_horizontal, use_container_width=True)

    # Domain-wise Student Count Pie Chart
    with col5:
        query_domain_count = """
            SELECT Domain, COUNT(*) AS Count 
            FROM placement_data 
            WHERE Branch = 'OPTOMETRY' 
            GROUP BY Domain
        """
        domain_count_data = fetch_data(query_domain_count)
        df_domain_count = pd.DataFrame(domain_count_data, columns=['Domain', 'Count'])
        fig_domain_count_pie = px.pie(df_domain_count, values='Count', names='Domain', 
                                      title='Domain-wise Student Count for OPTOMETRY Department',
                                      color_discrete_sequence=custom_colors)
        st.plotly_chart(fig_domain_count_pie, use_container_width=True)

    # Package vs. CGPA Scatter Plot
    with col6:
        query_package_cgpa = """
            SELECT CGPA, Package
            FROM placement_data
            WHERE Branch = 'OPTOMETRY' AND Placed = 'Yes' AND CGPA IS NOT NULL AND Package IS NOT NULL
        """
        package_cgpa_data = fetch_data(query_package_cgpa)
        df_package_cgpa = pd.DataFrame(package_cgpa_data, columns=['CGPA', 'Package'])
        fig_package_cgpa_scatter = px.scatter(df_package_cgpa, x='CGPA', y='Package', 
                                              title='Package vs. CGPA for Placed Students in Optometry Department',
                                              labels={'CGPA': 'CGPA', 'Package': 'Package Amount'},
                                              trendline='ols', color_discrete_sequence=custom_colors)
        st.plotly_chart(fig_package_cgpa_scatter, use_container_width=True)

if __name__ == "__main__":
    main()

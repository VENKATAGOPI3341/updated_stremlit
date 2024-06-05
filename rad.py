import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

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

def main():
    st.title("Placement Dashboard for Radiology Department")
    
    # Fetch data for gender distribution of placed students
    query_gender_distribution = "SELECT Gender, COUNT(*) AS Count FROM placement_data WHERE Branch = 'RADIOLOGY' AND Placed = 'Yes' GROUP BY Gender"
    gender_distribution_data = fetch_data(query_gender_distribution)
    df_gender_distribution = pd.DataFrame(gender_distribution_data, columns=['Gender', 'Count'])
    fig_gender_distribution_pie = px.pie(df_gender_distribution, values='Count', names='Gender', title='Gender Distribution of Placed Students')

    # Fetch data for CGPA distribution of placed students
    query_cgpa_distribution = "SELECT CGPA FROM placement_data WHERE Branch = 'RADIOLOGY' AND Placed = 'Yes'"
    cgpa_distribution_data = fetch_data(query_cgpa_distribution)
    df_cgpa_distribution = pd.DataFrame(cgpa_distribution_data, columns=['CGPA'])
    fig_cgpa_distribution_hist = px.histogram(df_cgpa_distribution, x='CGPA', title='CGPA Distribution for Placed Students', color_discrete_sequence=['#FF5733'])

    # Fetch data for domain-wise placement count
    query_domain_count = "SELECT Domain, COUNT(*) AS Count FROM placement_data WHERE Branch = 'RADIOLOGY' AND Placed = 'Yes' GROUP BY Domain"
    domain_count_data = fetch_data(query_domain_count)
    df_domain_count = pd.DataFrame(domain_count_data, columns=['Domain', 'Count'])
    fig_domain_count_bar = px.bar(df_domain_count, x='Domain', y='Count', title='Domain-wise Placed Students Count', color='Domain', color_discrete_sequence=px.colors.qualitative.Pastel)

    # Fetch data for company-wise placement count
    query_company_placement = "SELECT Company_placed, COUNT(*) AS Placement_Count FROM placement_data WHERE Branch = 'RADIOLOGY' AND Placed = 'Yes' AND Company_placed IS NOT NULL GROUP BY Company_placed"
    company_placement_data = fetch_data(query_company_placement)
    df_company_placement = pd.DataFrame(company_placement_data, columns=['Company_placed', 'Placement_Count'])
    fig_company_placement_bar_horizontal = px.bar(df_company_placement, y='Company_placed', x='Placement_Count', title='Company-wise Placement Count', labels={'Company_placed': 'Company', 'Placement_Count': 'Placement Count'}, orientation='h', color_discrete_sequence=['#32a852'])

    # Fetch data for backlogs analysis
    query_backlogs_analysis = "SELECT Backlogs, COUNT(*) AS Count FROM placement_data WHERE Branch = 'RADIOLOGY' AND Placed = 'Yes' AND Backlogs > 0 GROUP BY Backlogs"
    backlogs_analysis_data = fetch_data(query_backlogs_analysis)
    df_backlogs_analysis = pd.DataFrame(backlogs_analysis_data, columns=['Backlogs', 'Count'])
    fig_backlogs_analysis_bar = px.bar(df_backlogs_analysis, x='Backlogs', y='Count', title='Backlogs Analysis for Placed Students', color_discrete_sequence=['#005eff'])

    # Fetch data for package vs. CGPA for placed students
    query_package_cgpa = "SELECT Package, CGPA FROM placement_data WHERE Branch = 'RADIOLOGY' AND Placed = 'Yes' AND Package IS NOT NULL AND CGPA IS NOT NULL"
    package_cgpa_data = fetch_data(query_package_cgpa)
    df_package_cgpa = pd.DataFrame(package_cgpa_data, columns=['Package', 'CGPA'])
    fig_package_cgpa_scatter = px.scatter(df_package_cgpa, x='CGPA', y='Package', title='Package vs. CGPA for Placed Students', labels={'CGPA': 'CGPA', 'Package': 'Package Amount'}, trendline='ols', color_discrete_sequence=['#ff0000'])

    # Organize the visualizations in two rows with three columns each
    col1, col2, col3 = st.columns(3)
    with col1:
        fig_gender_distribution_pie.update_traces(marker=dict(colors=['blue', 'green']))
        st.plotly_chart(fig_gender_distribution_pie, use_container_width=True)
    with col2:
        st.plotly_chart(fig_cgpa_distribution_hist, use_container_width=True)
    with col3:
        st.plotly_chart(fig_domain_count_bar, use_container_width=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.plotly_chart(fig_company_placement_bar_horizontal, use_container_width=True)
    with col5:
        st.plotly_chart(fig_backlogs_analysis_bar, use_container_width=True)
    with col6:
        st.plotly_chart(fig_package_cgpa_scatter, use_container_width=True)

if __name__ == "__main__":
    main()

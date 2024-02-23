# Vancouver Crime Data Analysis and Prediction 

## Contents
* **SQL Scripts**: Contains SQL scripts for database schema creation, including tables for crimes, perpetrators, and their relationships.
* **Data Warehousing**: Includes files and documentation on the setup of Druid for storing and analyzing weather-related data.
* **ETL Processes**: Scripts and workflows for extracting, transforming, and loading data into the database and data warehouse.
* **Data Visualization**: Dashboards and visualizations created with Apache Superset to explore crime data in relation to weather conditions.
* **Predictive Analytics**: Jupyter notebooks and scripts for machine learning models predicting neighborhood crime occurrences.

## Installation
* PostgreSQL for database management.
* Druid and Apache Superset for data warehousing and visualization.
* Python with libraries such as Pandas, Scikit-learn for data processing and machine learning.

## Dataset
The dataset is collected from the Vancouver Open Data Catalogue, which contains the criminal records from 2003 to 2019 counted by the Vancouver Police Department. There are 530652 criminal records in it, excluding the total number of calls or complaints made to VPD, only including the crime categories described in the attributes. Some crimes are excluded for privacy and investigation reasons.  

## Logical model  

<img src="/pic/logical.jpeg" width = "800" height = "250" alt="cmo" />  

## Physical model  

<img src="/pic/physicalmodel.jpeg" width = "800" height = "270" alt="cmo" />  

## Data model  

<img src="/pic/datamodel.jpeg" width = "700" height = "230" alt="cmo" />  

## Data Warehouse Architecture  
The project utilizes Vancouver Crime Data for data analysis, employing **Airflow** for ETL processes from **operational databases** to **Druid**-based data warehouse. It features an **OLAP server** for multi-dimensional analysis, identifying trends through a multidimensional model. **Superset** finalizes the architecture with intuitive **data visualization** and **interactive dashboards**, enhancing data exploration and insight discovery.  

<img src="/pic/dw.png" width = "600" height = "250" alt="cmo" />  

## Data Warehouse population

## Materialize Cubes

## Visualization

## 

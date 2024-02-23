import pandas as pd
import os
import psycopg2
from psycopg2 import Error

df = pd.read_csv('data.csv').iloc[:,1:].dropna()


#rename column
col_rename = {'TYPE': 'crime_type_name','HUNDRED_BLOCK': 'block_name','NEIGHBOURHOOD': 'neighbourhood_name', 'X':'latitude', 'Y': 'longitude', 'time':'crime_time','perpetrator':'perpetrator_name'}
df = df.rename(columns = col_rename)


#generate id
df['crime_id'] = [i for i in range(len(df))]
crime_type_dct_name_to_id = { name: i for i, name in enumerate(df['crime_type_name'].unique())}
df['crime_type_id'] = df['crime_type_name'].apply(lambda x: crime_type_dct_name_to_id[x])
block_dct_name_to_id = { name: i for i, name in enumerate(df['block_name'].unique())}
df['block_id'] = df['block_name'].apply(lambda x: block_dct_name_to_id[x])
neighbourhood_dct_name_to_id = { name: i for i, name in enumerate(df['neighbourhood_name'].unique())}
df['neighbourhood_id'] = df['neighbourhood_name'].apply(lambda x: neighbourhood_dct_name_to_id[x])
perpetrator_dct_name_to_id = { name: i for i, name in enumerate(df['perpetrator_name'].unique())}
df['perpetrator_id'] = df['perpetrator_name'].apply(lambda x: perpetrator_dct_name_to_id[x])
perpetrator_crime_dct_name_to_id ={ name: i for i, name in enumerate(df['perpetrator_name'].unique())}
df['perpetrator_crime_id'] = df['neighbourhood_name'].apply(lambda x: perpetrator_dct_name_to_id[x])



#split df to populate
block = df[['block_id','block_name']].drop_duplicates()
crime = df[['crime_id','crime_time','longitude','latitude','crime_type_id']]
crime_position = df[['longitude','latitude','block_id']].drop_duplicates(subset = ['longitude','latitude'])
crime_type = df[['crime_type_id','crime_type_name']].drop_duplicates()
neighbourhood = df[['neighbourhood_id','neighbourhood_name']].drop_duplicates()
neighbourhood_block_map = df[['neighbourhood_id','block_id']].drop_duplicates()
perpetrator = df[['perpetrator_id','perpetrator_name','perpetrator_age','perpetrator_gender']].drop_duplicates()
perpetrator_crime = df['perpetrator_crime_id','perpetrator_id','crime_id']].drop_duplicates()

block.to_csv('block.csv', index = False)
crime.to_csv('crime.csv', index = False)
crime_position.to_csv('crime_position.csv', index = False)
crime_type.to_csv('crime_type.csv', index = False)
neighbourhood.to_csv('neighbourhood.csv', index = False)
neighbourhood_block_map.to_csv('neighbourhood_block_map.csv', index = False)
perpetrator.to_csv('')


# Connect to an existing database
#note, embedding credentials is bad practice but for the purpo
connection = psycopg2.connect(user="druid",
password="FoolishPassword",
host="localhost",
port="5432",
database="druid")
connection.autocommit = True


# Create a cursor to perform database operations
cursor = connection.cursor()
# Print PostgreSQL details
print("PostgreSQL server information")
print(connection.get_dsn_parameters(), "\n")
# Executing a SQL query
cursor.execute("SELECT version();")
# Fetch result
record = cursor.fetchone()
print("You are connected to - ", record, "\n")
block_path = os.path.abspath("/Users/wangwinnie/ece9014/analytics/codes/block.csv")
neighbourhood_path = os.path.abspath("/Users/wangwinnie/ece9014/analytics/codes/neighbourhood.csv")
neighbourhood_block_map_path = os.path.abspath("/Users/wangwinnie/ece9014/analytics/codes/neighbourhood_block_map.csv")
crime_position_path = os.path.abspath("/Users/wangwinnie/ece9014/analytics/codes/crime_position.csv")
crime_type_path = os.path.abspath("/Users/wangwinnie/ece9014/analytics/codes/crime_type.csv")
crime_path = os.path.abspath("/Users/wangwinnie/ece9014/analytics/codes/crime.csv")



sqlstr = "COPY block FROM STDIN DELIMITER ',' CSV HEADER"
with open(block_path) as f:
    cursor.copy_expert(sqlstr, f)
    sqlstr = "COPY neighbourhood FROM STDIN DELIMITER ',' CSV HEADER"
with open(neighbourhood_path) as f:
    cursor.copy_expert(sqlstr, f)
    sqlstr = "COPY neighbourhood_block_map FROM STDIN DELIMITER ',' CSV HEADER"
with open(neighbourhood_block_map_path) as f:
    cursor.copy_expert(sqlstr, f)
    sqlstr = "COPY crime_position FROM STDIN DELIMITER ',' CSV HEADER"
with open(crime_position_path) as f:
    cursor.copy_expert(sqlstr, f)
    sqlstr = "COPY crime_type FROM STDIN DELIMITER ',' CSV HEADER"
with open(crime_type_path) as f:
    cursor.copy_expert(sqlstr, f)
    sqlstr = "COPY crime FROM STDIN DELIMITER ',' CSV HEADER"
with open(crime_path) as f:
    cursor.copy_expert(sqlstr, f)
if (connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")

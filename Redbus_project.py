
import pandas as pd
import glob
import numpy as np
import time
import os


# upload all csv file

ASTRC=pd.read_csv("C:/Users/admin/Desktop/Busproject/Assam.csv")
ASTRC
BSRTC=pd.read_csv("C:/Users/admin/Desktop/Busproject/Bihar.csv")
BSRTC
HRTC=pd.read_csv("C:/Users/admin/Desktop/Busproject/Harayana.csv")
HRTC
CTU =pd.read_csv("C:/Users/admin/Desktop/Busproject/chandigarh.csv")
CTU
JKSTC =pd.read_csv("C:/Users/admin/Desktop/Busproject/jk.csv")
JKSTC

KTC = pd.read_csv("C:/Users/admin/Desktop/Busproject/kadamba.csv")
KTC
NBSTC=pd.read_csv("C:/Users/admin/Desktop/Busproject/North_bengal.csv")
NBSTC
PEPSU=pd.read_csv("C:/Users/admin/Desktop/Busproject/Punjab.csv")
PEPSU
WBSTC=pd.read_csv("C:/Users/admin/Desktop/Busproject/westbengal.csv")
WBSTC
APSRTC=pd.read_csv("C:/Users/admin/Desktop/Busproject/Andhra.csv")
APSRTC

# concat the csv file

df=pd.concat([ASTRC,HRTC,CTU,JKSTC,KTC,NBSTC,PEPSU,WBSTC,APSRTC,BSRTC])

df.to_csv("bus_routes.csv", index=False)

#read concat csv file

df = pd.read_csv("bus_routes.csv")


id_column = pd.Series(range(1, len(df) + 1), name='id')
df = pd.concat([id_column, df], axis=1)
print(df.info())  
print(df.isnull().sum()) 

#fill unknown data
df['Bus_Name'].fillna('Unknown', inplace=True)
df['Bus_Type'].fillna('Standard', inplace=True)
df['Departing_Time'].fillna('00:00', inplace=True)
df['Duration'].fillna('Unknown', inplace=True)
df['Arrival'].fillna('Unknown', inplace=True)
df['Rating'].fillna(df['Rating'].mean(), inplace=True)
df['Fare'].fillna(df['Fare'].median(), inplace=True)
df['Seat_Available'].fillna(0, inplace=True)


print(df.info())  
print(df.isnull().sum()) 

data = df.copy()  

# Save the cleaned data to a new CSV file
data.to_csv('cleaned_bus_routes.csv', index=False)

data.columns = data.columns.str.strip()

print(df.columns)
id_column = pd.Series(range(1, len(data) + 1), name='id')
data = pd.concat([id_column, data], axis=1)

data.columns = data.columns.str.strip()
print(data.columns)
print(data.info())
import pymysql

# Database connection
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1991",
    database="redbus_project"
)
cursor = connection.cursor()

# Create table (if not exists)
create_table_query = """
CREATE TABLE IF NOT EXISTS bus_routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Route_Name VARCHAR(255),
    Route_Link VARCHAR(255),
    Bus_Name VARCHAR(255),
    Bus_Type VARCHAR(50),
    Departing_Time VARCHAR(50),
    Duration VARCHAR(50),
    Arrival VARCHAR(50),
    Rating FLOAT,
    Fare FLOAT,
    Seat_Available VARCHAR(255)
);
"""
cursor.execute(create_table_query)


# Strip column names
data.rename(columns=lambda x: x.strip(), inplace=True)

print(data.columns) 
data.columns = ['id', 'id_duplicate', 'Route_Name', 'Route_Link', 
                'Bus_Name', 'Bus_Type', 'Departing_Time', 
                'Duration', 'Arrival', 'Rating', 'Fare', 'Seat_Available']


print(data[['id', 'id_duplicate']].head())
data = data.drop(columns=['id_duplicate'])


# Insert or update rows in the database
insert_query = """
INSERT INTO bus_routes (id, Route_Name, Route_Link, Bus_Name, Bus_Type, Departing_Time, Duration, Arrival, Rating, Fare, Seat_Available)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
Route_Name=VALUES(Route_Name),
Route_Link=VALUES(Route_Link),
Bus_Name=VALUES(Bus_Name),
Bus_Type=VALUES(Bus_Type),
Departing_Time=VALUES(Departing_Time),
Duration=VALUES(Duration),
Arrival=VALUES(Arrival),
Rating=VALUES(Rating),
Fare=VALUES(Fare),
Seat_Available=VALUES(Seat_Available);
"""

data.fillna({
    'Route_Name': 'Unknown',
    'Route_Link': 'Unknown',
    'Bus_Name': 'Unknown',
    'Bus_Type': 'Unknown',
    'Departing_Time': '00:00',
    'Duration': '0h',
    'Arrival': '00:00',
    'Rating': 0.0,
    'Fare': 0.0,
    'Seat_Available': '0',
}, inplace=True)

print(data.info())

for _, row in data.iterrows():
    cursor.execute(insert_query, (
        int(row['id']),
        row['Route_Name'], 
        row['Route_Link'], 
        row['Bus_Name'], 
        row['Bus_Type'], 
        row['Departing_Time'], 
        row['Duration'], 
        row['Arrival'], 
        row['Rating'], 
        row['Fare'], 
        row['Seat_Available']
    ))

connection.commit()
cursor.close()
connection.close()

print("Data has been successfully inserted into the database!")

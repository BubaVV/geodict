#!/usr/bin/env python

import csv, os, os.path, MySQLdb, sys, zipfile
import geodict_config
from geodict_lib import *

SOURCES = []

def wipe_and_init_database(cursor):
    print('Preparing database')
    cursor.execute("""DROP DATABASE IF EXISTS geodict;""")
    cursor.execute("""CREATE DATABASE IF NOT EXISTS `geodict` DEFAULT COLLATE 'utf8mb4_unicode_ci';""")
    cursor.execute("""USE geodict;""")

def load_cities(cursor):
    print('Loading cities. Can take a while')
    cursor.execute("""CREATE TABLE IF NOT EXISTS cities (
        city VARCHAR(100),
        country CHAR(2),
        region_code CHAR(2),
        population INT DEFAULT 0,
        lat FLOAT,
        lon FLOAT,
        last_word VARCHAR(100),
        INDEX(last_word(10)));
    """)
    cursor.execute('LOAD DATA LOCAL INFILE \'%s\' INTO TABLE cities CHARACTER SET utf8mb4 FIELDS TERMINATED BY ","' %
        (geodict_config.source_folder+'cities.csv'))
    cursor.execute('ALTER TABLE cities ADD PRIMARY KEY(city, country);')

def load_countries(cursor):
    print('Loading countries')
    cursor.execute("""CREATE TABLE IF NOT EXISTS countries (
        country VARCHAR(64),
        PRIMARY KEY(country),
        country_code CHAR(2),
        lat FLOAT,
        lon FLOAT,
        last_word VARCHAR(32),
        INDEX(last_word(10)));
    """)
    
    cursor.execute('LOAD DATA LOCAL INFILE \'%s\' INTO TABLE countries CHARACTER SET utf8mb4 FIELDS TERMINATED BY ","' %
                   (geodict_config.source_folder + 'countries.csv'))
        

def load_regions(cursor):
    print('Loading regions and US states')
    cursor.execute("""CREATE TABLE IF NOT EXISTS regions (
        region VARCHAR(64),
        PRIMARY KEY(region),
        region_code CHAR(4),
        country_code CHAR(2),
        lat FLOAT,
        lon FLOAT,
        last_word VARCHAR(32),
        INDEX(last_word(10)));
    """)
    cursor.execute('LOAD DATA LOCAL INFILE \'%s\' INTO TABLE regions CHARACTER SET utf8mb4 FIELDS TERMINATED BY ","' % (geodict_config.source_folder + 'regions.csv'))

def unzip_data():
    global SOURCES
    try:
        data = zipfile.ZipFile(geodict_config.source_folder+'data.zip')
        data.extractall(path=geodict_config.source_folder)
        SOURCES = data.namelist()
        return True
    except:
        print(sys.exc_info())
        return False

def clean_data():
    for i in SOURCES:
        os.remove(os.path.join(geodict_config.source_folder, i))

cursor = get_database_connection()

unzip_data()
wipe_and_init_database(cursor)

#load_cities(cursor)
load_countries(cursor)
load_regions(cursor)
cursor.connection.commit()
clean_data()
#!/usr/bin/env python

import csv, os, os.path, MySQLdb, sys
import geodict_config
from geodict_lib import *

def wipe_and_init_database(cursor):
    cursor.execute("""DROP DATABASE IF EXISTS geodict;""")
    cursor.execute("""CREATE DATABASE IF NOT EXISTS `geodict` DEFAULT COLLATE 'utf8mb4_unicode_ci';""")
    cursor.execute("""USE geodict;""")

def load_cities(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS cities (
        city VARCHAR(100),
        country CHAR(2),
        PRIMARY KEY(city, country),
        region_code CHAR(2),
        population INT DEFAULT 0,
        lat FLOAT,
        lon FLOAT,
        last_word VARCHAR(100),
        INDEX(last_word(10)));
    """)
    cursor.execute('LOAD DATA LOCAL INFILE \'%s\' INTO TABLE cities CHARACTER SET utf8mb4 FIELDS TERMINATED BY ","' % (geodict_config.source_folder+'worldcitiespop.csv'))

def load_countries(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS countries (
        country VARCHAR(64),
        PRIMARY KEY(country),
        country_code CHAR(2),
        lat FLOAT,
        lon FLOAT,
        last_word VARCHAR(32),
        INDEX(last_word(10)));
    """)
    
    reader = csv.reader(open(geodict_config.source_folder+'countrypositions.csv', 'r'))
    country_positions = {}

    for row in reader:
        try:
            country_code = row[0]
            lat = row[1]
            lon = row[2]
        except:
            continue

        country_positions[country_code] = { 'lat': lat, 'lon': lon }
        
    reader = csv.reader(open(geodict_config.source_folder+'countrynames.csv', 'r'))

    for row in reader:
        try:
            country_code = row[0]
            country_names = row[1]
        except:
            continue    

        country_names_list = country_names.split(' | ')
        
        lat = country_positions[country_code]['lat']
        lon = country_positions[country_code]['lon']
        
        for country_name in country_names_list:
        
            country_name = country_name.strip()
            
            last_word, index, skipped = pull_word_from_end(country_name, len(country_name)-1, False)

            cursor.execute("""
                INSERT IGNORE INTO countries (country, country_code, lat, lon, last_word)
                    values (%s, %s, %s, %s, %s)
                """,
                (country_name, country_code, lat, lon, last_word))
        

def load_regions(cursor):
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

    reader = csv.reader(open(geodict_config.source_folder+'us_statepositions.csv', 'r'))
    us_state_positions = {}

    for row in reader:
        try:
            region_code = row[0]
            lat = row[1]
            lon = row[2]
        except:
            continue

        us_state_positions[region_code] = { 'lat': lat, 'lon': lon }
    
    reader = csv.reader(open(geodict_config.source_folder+'us_statenames.csv', 'r'))

    country_code = 'US'

    for row in reader:
        try:
            region_code = row[0]
            state_names = row[2]
        except:
            continue    

        state_names_list = state_names.split('|')
        
        lat = us_state_positions[region_code]['lat']
        lon = us_state_positions[region_code]['lon']
        
        for state_name in state_names_list:
    
            state_name = state_name.strip()
            
            last_word, index, skipped = pull_word_from_end(state_name, len(state_name)-1, False)
        
            cursor.execute("""
                INSERT IGNORE INTO regions (region, region_code, country_code, lat, lon, last_word)
                    values (%s, %s, %s, %s, %s, %s)
                """,
                (state_name, region_code, country_code, lat, lon, last_word))
    
cursor = get_database_connection()

wipe_and_init_database(cursor)

load_cities(cursor)
load_countries(cursor)
load_regions(cursor)


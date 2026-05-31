import logging
import os
import configparser
import mysql.connector

def setup_logger():
    log_path="logs/warehouse.log"
    os.makedirs("logs",exist_ok=True)
    logging.basicConfig(filename=log_path,
                        level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    return logging

def read_config():
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    return config

def get_database_connection ():
    try:
        config = read_config()
        conn = mysql.connector.connect(
                                        host=config["mysql"]["host"],
                                        user=config["mysql"]["user"],
                                        password=config["mysql"]["password"],
                                        database=config["mysql"]["database"]
                                    )
        return conn;
    except Exception as e:
        print(f"Connection Error {str(e)}")


    




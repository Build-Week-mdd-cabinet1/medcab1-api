import os
import csv

from dotenv import load_dotenv
import psycopg2

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

connection = psycopg2.connect(dbname=DB_NAME,
                              user=DB_USER,
                              password=DB_PASSWORD,
                              host=DB_HOST,
                              port=DB_PORT)
cursor = connection.cursor()

query = """
CREATE TABLE IF NOT EXISTS strain_data (
    id int,
    name varchar(50),
    race varchar(50),
    flavors varchar(500),
    positive varchar(500),
    negative varchar(500),
    medical varchar(500),
    rating float,
    description varchar(2000)
);
"""

csvPath = os.path.join(os.path.dirname(__file__),
                       'tab_sep_strain_data.tsv')


if __name__ == "__main__":
    cursor.execute(query)

    with open(csvPath, 'rb') as medCsv:
        next(medCsv)
        cursor.copy_from(medCsv, 'strain_data', sep="\t", null="")

    connection.commit()
    cursor.close()
    connection.close()

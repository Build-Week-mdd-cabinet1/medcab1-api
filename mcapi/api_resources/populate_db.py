import os
import csv

from dotenv import load_dotenv
import psycopg2

load_dotenv()

"""Use code below when working with a local postgres database for
development, otherwise ssl required to establish connection with
heroku hosted postgres"""


DATABASE_URL = os.getenv("DATABASE_URL")

connection = psycopg2.connect(DATABASE_URL, sslmode='require')
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

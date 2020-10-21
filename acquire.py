from env import host, username, password
import pandas as pd
import numpy as np
import os

def get_connection(db, user=username, host=host, password=password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def acquire_zillow_data():
    sql_query = '''
            SELECT * FROM properties_2017
            JOIN predictions_2017 USING(parcelid)
            LEFT JOIN airconditioningtype USING(airconditioningtypeid)
            LEFT JOIN architecturalstyletype USING(architecturalstyletypeid)
            LEFT JOIN buildingclasstype USING(buildingclasstypeid)
            LEFT JOIN heatingorsystemtype USING(heatingorsystemtypeid)
            LEFT JOIN propertylandusetype USING(propertylandusetypeid)
            LEFT JOIN storytype USING(storytypeid)
            LEFT JOIN typeconstructiontype USING(typeconstructiontypeid)
            LEFT JOIN unique_properties USING(parcelid)
            WHERE latitude IS NOT null AND longitude IS NOT null;
            '''
    filename = 'zillow.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        df = pd.read_sql(sql_query, get_connection('zillow'))
        df.to_csv(filename, index=False)
        return df
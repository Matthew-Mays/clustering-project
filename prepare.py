from acquire import acquire_zillow_data
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LassoLars
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import RFE
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

def missing_rows(df):
    missing_row_pct = (df.isnull().sum() / len(df)) * 100
    missing_row_raw = df.isnull().sum()
    missing_df = pd.DataFrame({'num_rows_missing': missing_row_raw, 'pct_rows_missing': missing_row_pct})
    return missing_df

def drop_missing_columns(df):
    prop_required_column = .6
    threshold = int(round(prop_required_column * len(df.index), 0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    return df

def drop_selected_columns(df):
    df.drop(columns=['id', 'parcelid', 'latitude', 'longitude', 'propertycountylandusecode', 'propertylandusetypeid', 'propertylandusedesc', 'propertyzoningdesc', 
    'rawcensustractandblock', 'censustractandblock', 'regionidcity', 'regionidzip', 'yearbuilt', 'transactiondate', 'assessmentyear', 'unitcnt', 
    'finishedsquarefeet12', 'calculatedbathnbr', 'fullbathcnt', 'landtaxvaluedollarcnt', 'structuretaxvaluedollarcnt', 'buildingqualitytypeid', 'id.1',
    'regionidcounty', 'heatingorsystemdesc', 'heatingorsystemtypeid'], inplace=True)
    return df

def zillow_dummies(df):
    fips_dummies = pd.get_dummies(df['fips'], drop_first=False)
    fips_dummies = fips_dummies.rename(columns={fips_dummies.columns[0] : 'fips_6037', fips_dummies.columns[1] : 'fips_6059', fips_dummies.columns[2] : 'fips_6111'})
    df = pd.concat([df, fips_dummies], axis=1)
    return df

def zillow_split(df):
    train_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_validate, test_size=.3, random_state=123)
    return train, validate, test

def zillow_scaler(train, validate, test):
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    scaler = MinMaxScaler()
    train_to_scale = train_scaled[['bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet', 'lotsizesquarefeet', 'taxvaluedollarcnt', 'taxamount', 'roomcnt']]
    validate_to_scale = validate_scaled[['bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet', 'lotsizesquarefeet', 'taxvaluedollarcnt', 'taxamount', 'roomcnt']]
    test_to_scale = test_scaled[['bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet', 'lotsizesquarefeet', 'taxvaluedollarcnt', 'taxamount', 'roomcnt']]
    train_scaled[['bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet', 'lotsizesquarefeet', 'taxvaluedollarcnt', 'taxamount', 'roomcnt']] = scaler.fit_transform(train_to_scale)
    validate_scaled[['bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet', 'lotsizesquarefeet', 'taxvaluedollarcnt', 'taxamount', 'roomcnt']] = scaler.transform(validate_to_scale)
    test_scaled[['bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet', 'lotsizesquarefeet', 'taxvaluedollarcnt', 'taxamount', 'roomcnt']] = scaler.transform(test_to_scale)
    return train_scaled, validate_scaled, test_scaled
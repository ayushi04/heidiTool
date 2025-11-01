import logging
import pandas as pd
import numpy as np


logger = logging.getLogger(__name__)


def fix_missing(file, fix_option):
    option = (fix_option or '').strip().lower()
    logger.info("Applying missing value strategy '%s'", option if option else 'skip')

    if option == 'skip':
        file.dropna(axis=0, inplace=True)
    elif option == 'mean':
        file.dropna(axis=0, inplace=True)
        file.fillna(file.mean(axis=1), axis=0, inplace=True)
    elif option == 'median':
        file.dropna(axis=0, inplace=True)
        file.fillna(file.median(axis=1), axis=0, inplace=True)
    elif option == 'max frequent':
        file.dropna(axis=0, inplace=True)
        file.fillna(file.mode(axis=0), axis=0, inplace=True)
    elif option == 'max':
        file.dropna(axis=0, inplace=True)
        file.fillna(file.max(axis=0), axis=0, inplace=True)
    elif option == 'min':
        file.dropna(axis=0, inplace=True)
        file.fillna(file.min(axis=0), axis=0, inplace=True)
    else:
        logger.warning("Unknown missing value strategy '%s'; leaving dataset unchanged", fix_option)
    return file


def clean(file_clean):
    #file_clean.apply(lambda x: x.apply(lambda y: y.strip() if type(y) == type('') else y), axis=0)
    #pattern = r'[\W+a-zA-Z]'
    #file_clean.replace(pattern, value='', regex=True, inplace=True)
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    newdf = file_clean.select_dtypes(include=numerics)  
    for c in file_clean.columns:
        if c=='id' : newdf['id']=file_clean['id']
        if not c in list(newdf.columns):
            #print('ccc',c,file_clean[c].astype('category'))
            newdf[c]=file_clean[c].astype('category')
            newdf[[c]]=newdf[[c]].apply(lambda x:x.cat.codes)   

    logger.debug("Converted non-numeric columns to categorical codes: %s", [c for c in file_clean.columns if c not in newdf.select_dtypes(include=numerics).columns])

    return newdf

def id_classLabel_check(file):
    if 'id' not in file.columns:
        logger.error("'id' column not present in input data")
        return "Please add a unique column identifier labelled with column head 'id'!!"
    if 'classLabel' not in file.columns:
        logger.error("'classLabel' column not present in input data")
        return "Please add a unique cluster identifier labelled with column head 'classLabel'!!"
    if file['id'].isnull().any():
        logger.error("Missing values detected in 'id' column")
        return "Missing values are there is 'id' column!!"
    if file['classLabel'].isnull().any():
        logger.error("Missing values detected in 'classLabel' column")
        return "Missing values are there is 'classLabel' column!!"
    if not file['id'].is_unique:
        logger.error("'id' column values are not unique")
        return "'id' column values are not unique, please assign a unique value to each identifier!!"
    logger.info("Validation for 'id' and 'classLabel' columns succeeded")
    return True

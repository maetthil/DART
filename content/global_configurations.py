# -*- coding: utf-8 -*-
import os

import numpy as np
import pandas as pd
import operator
import yaml
import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic


DATASET_PATH = '../data/'


def preprocess_datetime(df, conf_dict):
    cols = conf_dict['DateTimeColumns']
    if 'ColumnsToExclude' not in conf_dict:
        conf_dict['ColumnsToExclude'] = []
    if 'DTCategoricalColumns' not in conf_dict:
        conf_dict['DTCategoricalColumns'] = []

    for dt_col in cols:
        col = list(dt_col.keys())[0]
        old_na_symbol = pd.NaT
        if any(df[col] == '0'):
            old_na_symbol = 0
        df[col] = pd.to_datetime(df[col], format=list(dt_col.values())[0], errors='coerce')
        df[col] = df[col].fillna(pd.NaT)

        df[f'{col}_year'] = df[col].dt.year.fillna(-1).astype('Int64')
        df[f'{col}_month'] = df[col].dt.month.fillna(-1).astype('Int64')
        df[f'{col}_week_number'] = df[col].dt.weekofyear.fillna(-1).astype('Int64')
        df[f'{col}_day'] = df[col].dt.day.fillna(-1).astype('Int64')
        df[f'{col}_day_week'] = df[col].dt.day_of_week.fillna(-1).astype('Int64')
        df[f'{col}_hour'] = df[col].dt.hour.fillna(-1).astype('Int64')
        df[f'{col}_minute'] = df[col].dt.minute.fillna(-1).astype('Int64')
        df[f'{col}_second'] = df[col].dt.second.fillna(-1).astype('Int64')
        df[col] = df[col].fillna(old_na_symbol)

        new_cols = [f'{col}_year', f'{col}_month', f'{col}_week_number',
                    f'{col}_day', f'{col}_day_week', f'{col}_hour',
                    f'{col}_minute', f'{col}_second']
        for c in new_cols:
            conf_dict['DTCategoricalColumns'].append(c)
        conf_dict['ColumnsToExclude'].append(col)
    return df


def infer_column_types(df, conf_dict):
    df = df[[each for each in df.columns if 'Unnamed' not in each]]

    # Auto-Categorical
    if 'CategoricalColumns' not in conf_dict:
        conf_dict['CategoricalColumns'] = list(set(list(df.select_dtypes(exclude=[np.number]).columns)))

    # Auto-Numerical
    if 'NumericalColumns' not in conf_dict:
        conf_dict['NumericalColumns'] = list(df.select_dtypes(include=[np.number]).columns)

    df[conf_dict['NumericalColumns']] = df[conf_dict['NumericalColumns']].apply(pd.to_numeric)

    # Columns to exclude
    if 'ColumnsToExclude' in conf_dict:
        conf_dict['CategoricalColumns'] = list(set(conf_dict['CategoricalColumns'])
                                               - set(conf_dict['ColumnsToExclude']))
        conf_dict['NumericalColumns'] = list(set(conf_dict['NumericalColumns'])
                                             - set(conf_dict['ColumnsToExclude']))

    # Sort Categorical Columns
    temp_dict = {}
    for cat_var in conf_dict['CategoricalColumns']:
        temp_dict[cat_var] = len(np.unique(df[cat_var].fillna('NaN').astype('string')))
    sorted_x = sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True)
    conf_dict['CategoricalColumns'] = [x for (x, y) in sorted_x]

    numerical = conf_dict['NumericalColumns']
    categorical = conf_dict['CategoricalColumns']
    categorical_dt = []
    datetime = []
    identifiers = []

    # Datetime Feature Extraction
    if 'DateTimeColumns' in conf_dict:
        preprocess_datetime(df, conf_dict)
        categorical_dt = conf_dict['DTCategoricalColumns']
        datetime = list(map(lambda x: list(x.keys())[0], conf_dict['DateTimeColumns']))

    # Identifiers
    if 'IdentifierColumns' in conf_dict:
        conf_dict['IdentifierColumns']

    # Target
    target = conf_dict['Target']

    # df.drop(columns=conf_dict['ColumnsToExclude'], inplace=True)
    return df, numerical, categorical, categorical_dt, datetime, identifiers, target,


def mosaic_plot(data, x, y, ax):
    if x != y:
        df = data[(data[x].isin(data[x].value_counts().head(10).index.tolist())) & (
            data[y].isin(data[y].value_counts().head(10).index.tolist()))]
        df2 = pd.crosstab(df[x], df[y])
        df2 = df2 + 1e-8
    else:
        df2 = pd.DataFrame(data[x].value_counts())[:10]

    mosaic(df2.unstack(), ax=ax, statistic=False,
           labelizer=lambda x: '', label_rotation=30)
    ax.set_ylabel(x)
    ax.set_xlabel(y)
    ax.set_title('{} vs {}'.format(x, y))
    return ax


def interactive_mosaic_plot(data, x, y):
    _, ax = plt.subplots(1)
    return mosaic_plot(data, x, y, ax)


def correlation_matrix(data, numerical, method, fig, ax):
    df = data[numerical].corr(method=method)
    col_names = list(data[numerical].columns)
    m = ax.matshow(df, cmap=plt.cm.coolwarm)
    ax.grid(b=False)
    fig.colorbar(m)
    ax.set_xticklabels([' '] + col_names)
    ax.set_yticklabels([' '] + col_names)
    return ax


def get_datetime_var_names(datetime_columns, var):
    for d in datetime_columns:
        var_name = f"{d}_{var}"
        yield var_name


def read_config_file(filename):
    with open(filename, 'r') as f:
        conf_dict = yaml.safe_load(f)
    return conf_dict


def read_dataset(conf_dict, base=None):
    dataset_path = os.path.join(base, conf_dict['DataFilePath']) \
        if base else conf_dict['DataFilePath']
    ext = dataset_path.split('.')[-1]
    if ext == 'csv':
        read = pd.read_csv
    elif ext == 'parquet':
        read = pd.read_parquet
    else:
        raise NotImplementedError('Arquivo não suportado')
    return read(dataset_path)

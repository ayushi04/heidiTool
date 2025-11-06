import pandas as pd


def get_dataframe_for_bitvector(df_matrix, df_dataset, bitvector):
    df_subset = df_matrix[df_matrix['bitvector']==bitvector]
    subspace = list(df_subset['subspace'])[0]
    row_points_id = set(df_subset['row_point'])
    col_points_id = set(df_subset['col_point'])
    row_points = df_dataset[df_dataset['id'].isin(row_points_id)]
    col_points = df_dataset[df_dataset['id'].isin(col_points_id)]
    df_combined = pd.concat([row_points, col_points])

    print('No of row_points: {}, col_points:{} in subspace : {}, bitvector: {}'.format(len(row_points), len(col_points), subspace, bitvector))
    return df_combined, subspace
def apply_to_dataframes(dfs, func, col_name):
    for df in dfs:
        df[col_name] = func(df)
    return dfs

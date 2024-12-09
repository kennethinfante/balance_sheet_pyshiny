import pandas as pd

# helper functions
def try_loc(df, column, values_to_search:list):
    if values_to_search:
        return df.loc[df[column].isin(values_to_search)]
    else:
        return df

def sort_val(df, by:list, ascending:list):
    return df.sort_values(by=by, ascending=ascending)

# new function because df.pivot does not have the aggfunc
def pivot_val(df, values:list, index:list, columns:list, aggfunc:str, margins:bool=False):
    try:
        return pd.pivot_table(df, values, index, columns, aggfunc, margins)
    except Exception as error:
        print('Error producing pivot table: ' + repr(error))


def pivot_style(cols_index:list):
    return [
        {
            "location": "body",
            "cols": cols_index,
            "style": {
                "text-align":"right"
            }
        }
    ]
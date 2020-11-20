import pandas as pd
import sklearn

def columnranker(df, column, columnname):
    df[column] = df[column].astype('float')
    df = df.sort_values(column)
    ranked_list = []
    dataframelength = len(df)
    print(dataframelength)
    current_row = 0
    for index, row in df.iterrows():
        current_row += 1
        #print(row['c1'], row['c2'])
        ranked_list.append(current_row/dataframelength)
        # print(current_row/dataframelength)
    df[columnname] = ranked_list
    return df


def infoadapter(df, infocolumn):
    bayes_list = []
    for item in list(df[infocolumn]):
        # print(item)
        if not isinstance(item, float):
            for value in item.split(';'):
                # print(value)
                # print(value.split('=')[0])
                if value.split('=')[0] == 'BayesDel_nsfp33a_noAF':
                    bayes_list.append(value.split('=')[1])
        else:
            bayes_list.append('.')
    df['BayesDel_noAF_score'] = bayes_list
    return df


def predictions(model, dataframe, columns):
    # load model,

    # specify dataframe columns

    #model.predict(data)

    # rejoin predict column with other columns

    return dataframe


test_set_update = infoadapter(test_set, 'INFO')
test_set_update_2 = columnranker(test_set_update, '..1', 'VEST4_rankscore')
outputdf = columnranker(test_set_update_2, 'BayesDel_noAF_score', 'BayesDel_noAF_rankscore')
outputdf = outputdf.rename(columns={".": "ClinPred_score"})

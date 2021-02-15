import pandas as pd
from sklearn.preprocessing import StandardScaler
# from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import argparse

parser = argparse.ArgumentParser(description='inputstuff')
parser.add_argument('inputfile',
                    help='The input file for annotation')
parser.add_argument('analysis_type',
                    help='Type of analysis to run')
parser.add_argument('outputfile',
                    help='Where to save the output')
args = parser.parse_args()


# this is currently vulnerable to low sample numbers.
vest4_range = []
bayes_range = []


def columnranker(df, column, columnname):
    df[column] = df[column].astype('float')
    df = df.sort_values(column)
    ranked_list = []
    dataframelength = len(df)
    #print(dataframelength)
    # prob change this to like range from start to end, this is some slow stuff
    if columnname == "VEST4_rankscore":
        for value in df[column]:
            # straight waste of computing
            if value < 1:
                value *= 1000
            ranked_list.append(value / 1000)
    elif columnname == "BayesDel_noAF_rankscore" or columnname == "BayesDel_addAF_rankscore":
        for value in df[column]:
            ranked_list.append((value + 1.29334) / (0.75731+1.29334))

    #current_row = 0
    #for index, row in df.iterrows():
    #    current_row += 1
    #    #print(row['c1'], row['c2'])
    #    ranked_list.append(current_row/dataframelength)
    df[columnname] = ranked_list
    return df


def infoadapter(df, infocolumn, searchterm, columnname):
    bayes_list = []
    for item in list(df[infocolumn]):
        # print(item)
        if not isinstance(item, float):
            for value in item.split(';'):
                # print(value)
                # print(value.split('=')[0])
                if value.split('=')[0] == searchterm:
                    bayes_list.append(value.split('=')[1])
        else:
            bayes_list.append('.')
    df[columnname] = bayes_list
    return df


def normalize(X):
    scaler = StandardScaler()
    scaler = scaler.fit(X)
    X = scaler.transform(X)
    return X


def predictions(model, dataframe, columns):
    # load model,
    loaded_model = pickle.load(open(model, 'rb'))
    # specify dataframe columns
    #print(dataframe[columns])
    dataframe['Prediction'] = loaded_model.predict_proba(normalize(np.array(dataframe[columns])))
    print(dataframe['Prediction'])
    return dataframe


full_annotation_clf = "models/full_annotation_model.sav"
vest_clf = "models/vest_model.sav"
clinpred_clf = "models/clinpred_model.sav"
non_coding_clf = "models/non_coding_model.sav"
info_columns_full_annotation = ['ClinPred_score', 'VEST4_rankscore', 'BayesDel_noAF_rankscore', 'BayesDel_noAF_score']
info_columns_full_vest = ['VEST4_rankscore', 'BayesDel_noAF_rankscore', 'BayesDel_noAF_score']
info_columns_full_clinpred = ['ClinPred_score', 'BayesDel_noAF_rankscore', 'BayesDel_noAF_score']
info_columns_full_non_coding = ['NC_SCORE', 'BayesDel_noAF_rankscore', 'BayesDel_noAF_score']

df = pd.read_csv(args.inputfile, delim_whitespace=True, header=0)
#print(df)
df = df.dropna()
df = infoadapter(df, 'INFO', 'BayesDel_nsfp33a_noAF', 'BayesDel_noAF_score')
#df = infoadapter(df, 'INFO', 'MaxAF', 'BayesDel_addAF_score')
df = columnranker(df, 'BayesDel_noAF_score', 'BayesDel_noAF_rankscore')
#df = columnranker(df, 'BayesDel_addAF_score', 'BayesDel_addAF_rankscore')

if args.analysis_type == "full":
    df = columnranker(df, 'VEST4', 'VEST4_rankscore')
    #df = df.rename(columns={".": "ClinPred_score"})
    output = predictions(full_annotation_clf, df, info_columns_full_annotation)
elif args.analysis_type == "vest":
    df = columnranker(df, 'VEST4', 'VEST4_rankscore')
    output = predictions(vest_clf, df, info_columns_full_vest)
elif args.analysis_type == "clinpred":
    #f = df.rename(columns={".": "ClinPred_score"})
    output = predictions(clinpred_clf, df, info_columns_full_clinpred)
elif args.analysis_type == "non_coding":
    output = predictions(non_coding_clf, df, info_columns_full_non_coding)

output.to_csv(args.outputfile, index=False, sep='\t')



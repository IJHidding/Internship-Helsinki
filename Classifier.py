
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import regex as re
import pickle

# fixing the columns with weird entries split by ';' or ':' by just returning the first number found
# this approach will work for repeated values, but
# will not necessarily work when used on a string with multiple useful values
# unsure how to fix that expect leave the whole column out or try to combine those values.


def value_fix(value):
    value_list = []
    for item in value:
        if ':' in str(item) or ';' in str(item):
            print(item)
            if re.search(r'(\w+|[+])', item):
                value_list.append(re.search(r'(\w+|[+])', item).group())
            else:
                value_list.append(np.NaN)
        else:
            value_list.append(item)
    return value_list


def encode_df(dataframe):
    le = LabelEncoder()
    for column in dataframe.columns:
        dataframe[column] = le.fit_transform(dataframe[column].astype(str))
    return dataframe


import pandas as pd
import numpy as np

#test_set = pd.read_csv('/Users/iwanhidding/PycharmProjects/Internship-Helsinki/full_file_annotated.vcf',
#                       skiprows=67, sep='\t', skipfooter=1)


def normalize(X):
    scaler = StandardScaler()
    scaler = scaler.fit(X)
    X = scaler.transform(X)
    return X


def create_classifier(dataframe, classifier_model, target, info_columns):
    #print(dataframe)
    for column in info_columns:
        #print(column)
        #print(dataframe[column])
        dataframe = dataframe[pd.to_numeric(dataframe[column], errors='coerce').notnull()]
    #dataframe = dataframe[pd.to_numeric(dataframe[info_columns], errors='coerce').notnull()]
    y = np.array(dataframe[target])
    #print(dataframe[info_columns])
    X = normalize(np.array(dataframe[info_columns]))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.9, random_state=42)
    clf = classifier_model
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    confusion_matrix_score = confusion_matrix(y_test, y_pred)
    #print(confusion_matrix_score)
    print(classification_report(y_test, y_pred))
    return clf


def label_fix(col):
    if col == "Pathogenic":
        return 1
    elif col == "Benign":
        return 0
    elif col == "Benign/Likely_benign":
        return 0
    elif col == "Pathogenic/Likely_pathogenic":
        return 1
    elif col == "Conflicting_interpretations_of_pathogenicity":
        return np.NaN
    elif col == "Uncertain_significance":
        return np.NaN
    else:
        return np.NaN


target = 'clinvar_hgvs'
info_columns_full_annotation = ['ClinPred_score', 'VEST4_rankscore', 'BayesDel_noAF_rankscore', 'BayesDel_noAF_score']
info_columns_full_vest = ['VEST4_rankscore', 'BayesDel_noAF_rankscore', 'BayesDel_noAF_score']
info_columns_full_clinpred = ['ClinPred_score', 'BayesDel_noAF_rankscore', 'BayesDel_noAF_score']
info_columns_full_non_coding = ['NC_SCORE', 'BayesDel_noAF_rankscore', 'BayesDel_noAF_score']
df = pd.read_csv("/Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/nc_realoutput.txt", sep='\t')
#print(df)
df['clinvar_hgvs'] = df['clinvar_hgvs'].apply(label_fix)
#print(df['clinvar_hgvs'])
df = df[df['clinvar_hgvs'].notna()]
#print(df)
full_annotation_clf = create_classifier(df, RandomForestClassifier(), target, info_columns_full_annotation)
vest_clf = create_classifier(df, RandomForestClassifier(), target, info_columns_full_vest)
clinpred_clf = create_classifier(df, RandomForestClassifier(), target, info_columns_full_clinpred)
non_coding_clf = create_classifier(df, RandomForestClassifier(), target, info_columns_full_non_coding)
pickle.dump(full_annotation_clf, open('models/full_annotation_model.sav', 'wb'))
pickle.dump(vest_clf, open('models/vest_model.sav', 'wb'))
pickle.dump(clinpred_clf, open('models/clinpred_model.sav', 'wb'))
pickle.dump(non_coding_clf, open('models/non_coding_model.sav', 'wb'))

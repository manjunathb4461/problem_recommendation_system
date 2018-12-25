# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 11:23:42 2018

@author: Hrishikesh S

Please import Phase3.spydata with file as the values generated are very huge in file
size. Use Spyder IDE.
"""
# cd "Desktop/Third Year/Data Analytics/Project Ideas/dataset/train"
import pandas as pd
import numpy as np
import math
from scipy.spatial.distance import cosine

#np.seterr(divide='ignore', invalid='ignore')

"""reading all files"""
user_data = pd.read_csv("user_data.csv")
user_data.head()

train_submissions = pd.read_csv("train_submissions.csv")
train_submissions.head()

problem_data = pd.read_csv("problem_data.csv")
problem_data.head()

"""all columns"""
print(user_data.columns)
print(train_submissions.columns)
print(problem_data.columns)

"""central tendencies of users"""
print(user_data['rating'].mean())
print(user_data['rating'].median())
print(user_data['rating'].mode())

all_users = user_data['user_id']

def rmse(y,y_pred):
    y = [(x-y_pred)**2 for x in y]
    mse = np.mean(y)
    return math.sqrt(mse)

def convert(data):
    rows = data.user_id.unique()
    cols = data.problem_id.unique()
    #print(len(rows), len(cols))
    data = data[['user_id', 'problem_id', 'attempts_range']]
    idict = dict(zip(cols, range(len(cols))))
    udict = dict(zip(rows, range(len(rows))))
    data.user_id = [ udict[i] for i in data.user_id ] 
    data['problem_id'] = [ idict[i] for i in data['problem_id'] ]
    nmat = data.as_matrix()
    return nmat, len(rows), len(cols)

def loc(mat, n_rows, n_cols):
    naive = np.zeros((n_rows, n_cols))
    print('naive shape', naive.shape)
    for row in mat:
        naive[int(row[0]), int(row[1])] = row[2]
    amean1 = np.mean(naive[naive!=0])
    umean1 = sum(naive.T) / sum((naive!=0).T)
    imean1 = sum(naive) / sum((naive!=0))
    return naive, amean1, umean1, imean1

def cos(mat, a, b):
    if a == b:
        return 1
    aval = mat.T[a].nonzero()
    bval = mat.T[b].nonzero()
    corated = np.intersect1d(aval, bval)
    if len(corated) == 0:
        return 0
    avec = np.take(mat.T[a], corated)
    bvec = np.take(mat.T[b], corated)
    val = 1 - cosine(avec, bvec)
    if np.isnan(val):
        return 0
    return val

def usersimilar(mat):
    # *Calculate amean, umean and imean as before
    n = mat.shape[1]
    sim_mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            sim_mat[i][j] = cos(mat, i, j)
    return sim_mat

def kmostsimilarusers(sim_mat, k):
    ksimilar = []
    for ii, i in enumerate(sim_mat):
        mi = i.argsort()
        mi = np.delete(mi, np.where(mi==ii))
        ksimilar.append(mi[-(k):])
    return ksimilar

def cos_inverse(mat, a, b):
    if a == b:
        return 1
    aval = mat.T[a].nonzero()
    bval = mat.T[b].nonzero()
    corated = np.intersect1d(aval, bval)
    if len(corated) == 0:
        return 0
    avec = np.take(mat.T[a], corated)
    bvec = np.take(mat.T[b], corated)
    val = cosine(avec, bvec)
    if np.isnan(val):
        return 0
    return val

def itemssimilar(mat):
    # *Calculate amean, umean and imean as before
    n = mat.shape[1]
    sim_mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            sim_mat[i][j] = cos_inverse(mat, i, j)
    return sim_mat
    
complete_user_data = pd.merge(user_data, train_submissions, 
                              on="user_id", how="outer")

train_matrix, train_rows, train_cols = convert(complete_user_data)
print(train_matrix, train_rows, train_cols)

train_matrix = train_matrix[~np.isnan(train_matrix).any(axis=1)]

train_naive, train_amean1, train_umean1, train_imean1 = loc(train_matrix, train_rows, train_cols)

train_usim_matrix_cosine = usersimilar(train_naive.T)

k = int(input())
train_ksimilar_cosine = kmostsimilarusers(train_usim_matrix_cosine, k)

#train_udisim_matrix_cosine = userdissimilar(train_naive.T) 
#train_kdisimilar_cosine = kmostsimilarusers(train_udisim_matrix_cosine, k)

#number of problems user wants
number_of_problems = int(input())
recommended_problem = []
for i in range(len(train_ksimilar_cosine)):
    for j in range(k):
        sim_user = all_users[train_ksimilar_cosine[i][j]]
        curr_user = all_users[i]
        sim_problem = complete_user_data[complete_user_data['user_id'] == sim_user]['problem_id']
        curr_problem = complete_user_data[complete_user_data['user_id'] == curr_user]['problem_id']
        r = [item for item in sim_problem if item not in curr_problem]
        recommended_problem.append(r[0:number_of_problems])

train_itemsum_matrix_cosine = itemssimilar(train_naive.T)
train_ksimilaritem_cosine = kmostsimilarusers(train_itemsum_matrix_cosine, k)

#recommendation based on problems
recommended_problem_item = []
train_ksimilaritem_cosine = np.array(train_ksimilaritem_cosine)
all_problems = problem_data['problem_id']
for i in range(len(train_ksimilaritem_cosine)):
    curr_problem = all_problems[i]
    recommended_problem_item.append(all_problems[train_ksimilaritem_cosine[i]])
    
userid = input("What is your user id number?\n")
userid = "user_"+ userid
user_index = np.where(all_users == userid)[0][0]
print("Based on user similarity : ", recommended_problem[user_index])
print("Based on item similarity : ", recommended_problem_item[user_index].tolist())
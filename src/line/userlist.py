# -*- coding: utf-8 -*-
import pickle

with open('user_list.pkl', 'rb') as f:
    user_list = pickle.load(f)

print("load_userlist")
print(user_list)

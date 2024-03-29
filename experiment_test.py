import sys
import collections
import pandas as pd
import tensorflow as tf

sys.path.append('..')
from model import Model

#set high and low values for 4 factor, 2 level, full factorial
a_low = 10**(-4)
a_high = 10**(-3)
b_low = 10**(-5)
b_high = 10**(-4)
c_low = 0.4
c_high = 0.8
d_low = 0.4
d_high = 0.8

#list the recipes per the levels, full factorial
null = [a_low, b_low, c_low, d_low]
a = [a_high, b_low, c_low, d_low]
b = [a_low, b_high, c_low, d_low]
ab = [a_high, b_high, c_low, d_low]
c = [a_low, b_low, c_high, d_low]
ac = [a_high, b_low, c_high, d_low]
bc = [a_low, b_high, c_high, d_low]
abc = [a_high, b_high, c_high, d_low]
d = [a_low, b_low, c_low, d_high]
ad = [a_high, b_low, c_low, d_high]
bd = [a_low, b_high, c_low, d_high]
abd = [a_high, b_high, c_low, d_high]
cd = [a_low, b_low, c_high, d_high]
acd = [a_high, b_low, c_high, d_high]
bcd = [a_low, b_high, c_high, d_high]
abcd = [a_high, b_high, c_high, d_high]


#flatten output list from each run {val_loss, val_acc, total_time} 
def flatten(x):
    if isinstance(x, collections.Iterable):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]

# This handles the experiment and adds results to a list
def experiment(recipe_list):
    all_results_rep = []
    #iterate over
    for item in recipe_list:
        model_recipe = Model(test = True, learning_rate_1 = item[0], learning_rate_2 = item[1], dropout_rate_1 = item[2], dropout_rate_2 = item[3])
        one_result = model_recipe.runexample()
        all_results_rep.append(flatten(one_result))
        tf.keras.backend.clear_session()
    return all_results_rep

## input a list of replications and name as string a output a single csv file
def csv_out(input_list, name):
    df_final = pd.DataFrame()
    for i in range(len(input_list)):
        df = pd.DataFrame(input_list[i])
        df_final = pd.concat([df_final, df])
    #output csv
    df_final.to_csv(name + '.csv', index=False)
    return df_final


# define which recipes you will run for each
recipe_list_rep1 = [null, a, b, ab, c, ac, bc, abc, d, ad, bd, abd, cd, acd, bcd, abcd]


# define the list which will hold all data for each replication
rep1_listout = experiment(recipe_list_rep1)


# list of results output if more than one
# result_list = [rep1_listout, rep2_listout, rep3_listout]

# create csv
csv_out(rep1_listout, "3rep_test_true")

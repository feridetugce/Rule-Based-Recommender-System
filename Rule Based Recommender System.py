###########################################################
#   How to calculate potential customer return with rule-based classification
###########################################################

################### Business Problem ######################

#   A game company wants to create a level-based customer definition (Persona) by using some features of current customers and new segments according to 
#   these new customer definitions. With these new segments, the company aims to calculate and forecast the potential return of these customers.
#   E.g., they want to forecast how much they can earn from 30 years old female android user from Canada.

#################### DataSet Story ########################

#   Persona.csv DataSet includes the price of some products and the demographics of the customers who buy those products.
#   The DataSet involves the records that come up in any sales. Which means the table is not deduplicated. 
#   In other words, a customer with specific demographics may have more than one transaction.


################# Variables ################################

#   PRICE = Customer Spending
#   SOURCE = Type of device that the customer is connected to
#   SEX = Customer’s Gender
#   COUNTRY = Customer’s Country
#   AGE= Customer’s Age

################## Before #################################

#    PRICE   SOURCE   SEX COUNTRY   AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# After ####################################

#       customers_level_based        PRICE   SEGMENT
# 0  BRA_ANDROID_FEMALE_0_18    1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23   1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857        A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667        C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667        C

##############################################################

#   Assignment # 1 
#   Apply the steps

#  1. Read the persona.csv file and show general information about the dataset

import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv("persona.csv")

def info_df(dataframe, head=5):
    print("############### Shape ################")
    print(dataframe.shape)
    print("########### Types ###############")
    print(dataframe.dtypes)
    print("########### Head ###############")
    print (dataframe.head(head))
    print ("########### Tail ###############" )
    print ( dataframe.tail(head))
    print ( "########### NA ###############" )
    print ( dataframe.isnull().sum())
    print ( "########### Quantiles ###############" )
    print ( dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T )

info_df(df)

#   2. How many unique SOURCE are there? What are their frequencies?

df["SOURCE"].nunique()
df["SOURCE"].value_counts()

#   3. How many unique PRICE are there?

df["PRICE"].nunique()

#   4. How many sales were made from each PRICE?

df["PRICE"].value_counts()

#   5. How many sales were made from each COUNTRY?

df["COUNTRY"].value_counts()

#   6. How much was earned from sales by country?

df.groupby("COUNTRY").agg({"PRICE": "sum"})

# OR

df.groupby("COUNTRY")["PRICE"].agg("sum")

#   7. What are the sales numbers according to SOURCE?

df.groupby("SOURCE").agg({"PRICE": "count"})

# OR

df["SOURCE"].value_counts()

#   8. What is the average PRICE by COUNTRY?

df.groupby("COUNTRY").agg({"PRICE": "mean"})

#   9. What is the average PRICE by SOURCE?

df.groupby("SOURCE").agg({"PRICE": "mean"})

#   10. What are the PRICE averages in the COUNTRY-SOURCE breakdown?

df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})


#   Assignment # 2

#   What is the average earning in COUNTRY, SOURCE, SEX, AGE breakdowns?

df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"})


#   Assignment # 3

#   Sort the output by PRICE
#   To better see the output in the previous question, apply the sort_values method in descending order of PRICE.
#   Save the output as agg_df

df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
    
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
 
 
#   Assignment # 4

#   Convert the names in the index to variable names.
#   All variables except PRICE in the output of the third question are index names. Convert these names to variable names

agg_df = agg_df.reset_index()


#   Assignment # 5

#   Convert AGE variable to categorical variable and add it to agg_df.
#   Convert the numeric variable age to a categorical variable. Construct the intervals convincingly.
#   For example: ‘0_18’, ‘19_23’, ‘24_30’, ‘31_40’, ‘41_70’

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0,18,23,30,40,70], right=True, labels =["0_18", "19_23", "24_30", "31_40", "41_70"])
                           

#   Assignment # 6

#   Identify new level-based customers (personas).
#   Define new level-based customers (personas) and add them as variables to the dataset. Name of new variable to add: customers_level_based.
#   You need to create the customers_level_based variable by combining the observations from the output of the previous question.

agg_df["customers_level_based"] = [(agg_df.COUNTRY[i] + "_" + agg_df.SOURCE[i] + "_" + agg_df.SEX[i] + "_" + str(agg_df.AGE_CAT[i])).upper() for i in agg_df.index]

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df = agg_df.reset_index()


#   Assignment # 7

#   Segment new customers. 
#   Divide new customers (E.g. USA_ANDROID_MALE_0_18) into 4 segments according to PRICE.
#   Add the segments as a variable to agg_df as "SEGMENT".
#   Describe segments (group by SEGMENT and get price mean, max, sum).

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"],4,["D","C","B","A"])
agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "sum"]})


#   Assignment # 8

#   Classify new customers and forecast how much revenue they can generate.
#   E.g. which segment does 33 years old ANDROID user Turkish woman belong to? And how much income is expected to earn on average?

new_user ="TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user ]

##############################################################   



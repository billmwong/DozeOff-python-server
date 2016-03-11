import pandas as pd
import numpy as np
import os
from flask import Flask


app = Flask(__name__)

b = pd.read_csv('brfss2014_short.csv')

# Get rid of special codes like "did not answer" or "don't know"
b = b[b.children != 89]
b = b[b.children != 99]
b = b[b.sleptim1 != 77]
b = b[b.sleptim1 != 99]
b = b[b.marital != 9]
b = b[b.employ1 != 9]
b = b[b.income2 != 77]
b = b[b.income2 != 99]
b = b[b.weight2 != 9999]
b = b[b.useequip != 7]
b = b[b.useequip != 9]
b = b[b['x.ageg5yr'] != 14]

def getAgeCat(age):
    """
    Returns the age category number to use in the dataset given
    an actual integer age.
    """
    if age <= 24: return 1
    if age <= 29: return 2
    if age <= 34: return 3
    if age <= 39: return 4
    if age <= 44: return 5
    if age <= 49: return 6
    if age <= 54: return 7
    if age <= 59: return 8
    if age <= 64: return 9
    if age <= 69: return 10
    if age <= 74: return 11
    if age <= 79: return 12
    return 13

# Employment Code:
# 1: Employed for wages
# 2: Self-employed
# 3: Out of work for 1 year or more
# 4: Out of work for less than 1 year
# 5: A homemaker
# 6: A student
# 7: Retired
# 8: Unable to work
# 9: Refused

def getSleep(age, sex, married, children, employment):
    """
    Returns the average sleep that a person with given
    demographic parameters gets per night.
    age: int
    sex: int where 1 is male and 2 is female
    married: boolean whether they're married
    children: boolean whether they have children
    employment: int describing emplyment according to above code
    """
    df = b.copy()
    df = df[df['sex'] == sex]
    df = df[df['x.ageg5yr'] == getAgeCat(age)]
    if married == 1:
        df = df[df['marital'] == 1]
    else:
        df = df[df['marital'] != 1]
    if children == 1:
        df = df[df['children'] != 88]
    else:
        df = df[df['children'] == 88]
    df = df[df['employ1'] == employment]
    
    print "number in this demographic:",len(df)
    return df['sleptim1'].mean()
# getSleep(23,1, False, False, 1)



@app.route("/")
def hello():
	return "Hello World!"

@app.route("/api/<int:age>/<int:sex>/<int:married>/<int:children>/<int:employment>")
def showi(age, sex):
	avgsleep = getSleep(age, sex, married, children, employment)
	return str(avgsleep)

@app.route("/percentile/<float:hour>")
def getpercentile(hour):
    if hour < 4:
        return 5.27/4*hour
    elif hour < 5:
        return 5.27 + (12.88-5.27) * (hour - 4)
    elif hour < 6:
        return 12.88 + (34.82-12.88) * (hour - 5)
    elif hour < 7:  
        return 34.82 + (58.82 - 34.82) * (hour - 6)
    elif hour < 8:
        return 58.82 + (87.75 - 58.82) * (hour - 7)
    elif hour < 9:
        return 87.75 + (92.54 - 87.75) * (hour - 8)
    elif hour < 10:
        return 92.54 + (95.62 - 92.54) * (hour - 9)
    elif hour > 10:
        return 99.6


if __name__ == "__main__":
	# app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
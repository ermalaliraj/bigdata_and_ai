# Machine Learning - Dummy Variables & One Hot Encoding

Build a predictor function to predict price of a home:
- 3400 square feet area, in west windsor
- 2800 square feet area in robbindville

```
                town  area   price
0   monroe township  2600  550000
1   monroe township  3000  565000
2   monroe township  3200  610000
3   monroe township  3600  680000
4   monroe township  4000  725000
5      west windsor  2600  585000
6      west windsor  2800  615000
7      west windsor  3300  650000
8      west windsor  3600  710000
9       robinsville  2600  575000
10      robinsville  2900  600000
11      robinsville  3100  620000
12      robinsville  3600  695000
```

### Topics
- Categorical variables
    - Nominal, do not have order relationship. Male/Female, different colors etc
    - Ordinal, do have some sort of order relationship. Satisfied/Neutral/Dissatisfied, High/medium/low, etc
- One Hot Encoding, using sklearn OneHotEncod
    - create a new column for each category and assign 1/0
- Dummy Variables, using pandas get_dummies

### Linear equation 
- Assign numbers to the township will not work, it will assume are order numbers and interpret them as: 
monroe township < west windsor < robinsville
or 
monroe township + west windsor = robinsville


### Exercise
Below the car sell prices for 3 different models. First plot data points on a scatter plot chart to see if 
linear regression cna be applied. Il yes, then build a model that can answer the following questions:
- Predict price of a Mercedez benz that is 4 yr old mileage 45000
- Predict price of a BMW X5 benz that is 7 yr old mileage 86000
- Tell the score (accuracy) of the model

```
                 Car Model  Mileage  Sell Price($)  Age(yrs)
0                  BMW X5    69000          18000         6
1                  BMW X5    35000          34000         3
2                  BMW X5    57000          26100         5
3                  BMW X5    22500          40000         2
4                  BMW X5    46000          31500         4
5                 Audi A5    59000          29400         5
6                 Audi A5    52000          32000         5
7                 Audi A5    72000          19300         6
8                 Audi A5    91000          12000         8
9   Mercedez Benz C class    67000          22000         6
10  Mercedez Benz C class    83000          20000         7
11  Mercedez Benz C class    79000          21000         7
12  Mercedez Benz C class    59000          33000         5
```



# See
- [Youtube Tutorial](https://www.youtube.com/watch?v=9yl6-HEY7_s)
- [Git Hub Tutorial](https://github.com/codebasics/py/tree/master/ML)
###
- [Back to Bid Data & AI](https://github.com/ermalaliraj/bigdata_and_ai)


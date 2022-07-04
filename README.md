# Sales Forecast API for a Drug Store Chain  [![gcash donation][1]][2] [![paypal donation][3]][4]

[![license][5]][6] [![python version][7]][8] [![pywebio version][9]][10] [![scikit version][11]][12] [![build][13]][14] 
 
Rossmann is Germany's second-largest drug store chain. We have been provided with historical sales data for 1,115 Rossmann stores. The task is to forecast the "Sales" column. The goal of this project would be (1) to create a model that would forecast the **sales** by using only these fields as inputs: `Store`, `DayOfWeek`, `Date`, `Customers`, `Open`, `Promo`, `StateHoliday` and `SchoolHoliday` and (2) to create and deploy an API that can serve prediction by receiving a JSON file via POST.

![Drug](https://images.unsplash.com/photo-1631549916768-4119b2e5f926?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1179&q=80)


### Files
Here are some files that may be important to those who would like to check the code or to those who would want to replicate the project.
* [app.py](https://github.com/mcabanlit/drug-store-chain/blob/main/app.py) - This python file contains almost all of our code for deployment.
* [drug-store-sales-prediction.ipynb](https://github.com/mcabanlit/drug-store-chain/blob/main/drug-store-sales-prediction.ipynb) - This notebook contains our data preprocessing, estimator testing, and hyperparameter optimization.
* [miniconda_requirements.txt](https://github.com/mcabanlit/drug-store-chain/blob/main/miniconda_requirements.txt) - This .txt file contains all the libraries that were used in the miniconda environment. 
* [requirements.txt](https://github.com/mcabanlit/drug-store-chain/blob/main/requirements.txt) - This .txt file contains all the necessary libraries that were used for the deployment of the API to Heroku.
* [sales_prediction_small.pkl](https://github.com/mcabanlit/drug-store-chain/blob/main/sales_prediction_small.pkl) - This is our exported `RandomForestRegressor` model.


### Dataset
For this project, we are given two sets of data, which are as follows:
* [train.csv](https://github.com/mcabanlit/drug-store-chain/blob/main/data/train.csv) - contains sales data on a daily frequency
* [store.csv](https://github.com/mcabanlit/drug-store-chain/blob/main/data/store.csv) - contains store information

After enriching our datasets and merging these two csvs, we tried to remove the outliers of the dataset using the three sigma limits method. 
![image](https://user-images.githubusercontent.com/102983286/177042424-33d99b12-6c76-458c-a4ef-cc0bf6c28d2d.png)


### Models
In this regression problem, we tried to find an optimal estimator that could produced better accuracy. The models that we have used in the notebook were compared according to their R-squared, Mean Absolute Error and Root Mean Squared Error.

![image](https://user-images.githubusercontent.com/102983286/177042627-13214ea4-d956-4264-97c4-23d8e6586ca3.png)

The models that we have used are as follows:
| Estimator                 | Training MAE | Valid MAE  | Training RMSE | Valid RMSE  | TrainingR^2 | ValidR^2 |
|---------------------------|--------------|------------|---------------|-------------|-------------|----------|
| [GradientBoostingRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html) | 621.526969   | 646.191632 | 867.44368     | 917.094263  | 0.937831    | 0.930204 |
| [ElasticNet](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html)                | 890.032279   | 921.517618 | 1235.419808   | 1289.533631 | 0.873897    | 0.862003 |
| [LinearBayesianRidge](https://scikit-learn.org/stable/modules/linear_model.html)       | 847.36449    | 851.449988 | 1164.614338   | 1184.581484 | 0.887938    | 0.883551 |
| [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)          | 847.367452   | 851.450242 | 1164.614335   | 1184.577635 | 0.887938    | 0.883552 |
| [RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)     | 494.02249    | 525.218697 | 736.846054    | 791.106196  | 0.955141    | 0.948063 |

The `RandomForestRegressor` produced the best results among all the models listed above given default parameters. So I went ahead and performed hyperparameter tuning on the model.


### Usage
When visiting the [deployed Heroku website](https://drug-store-chain.herokuapp.com/), users could only see instructions on how to use the API which will also be listed in this section.

#### Postman
The first way of testing the API would be to use [Postman](https://www.postman.com/). You may copy the JSON code snippet below and paste it in postman with the same configuration on the image following the code block.

```JSON
{
"Store":315,
"DayOfWeek":6,
"Date":"2014-07-10",
"Customers":465,
"Open":0,
"Promo":0,
"StateHoliday":"0",
"SchoolHoliday":1
}
```

![image](https://github.com/mcabanlit/drug-store-chain/blob/main/assets/banner.png)

#### Requests
Another way to access the API is by using the requests library in Python.
```python
import requests

r = requests.post('https://drug-store-chain.herokuapp.com/predict', json={
                      "Store":1111,
                      "DayOfWeek":4,
                      "Date":"2014-07-10",
                      "Customers":410,
                      "Open":1,
                      "Promo":0,
                      "StateHoliday":"0",
                      "SchoolHoliday":1
                 })
                 
print(r.text)
```
If ran, the code snippet above would return something like the one below:
![image](https://user-images.githubusercontent.com/102983286/177044006-64b12ff7-975c-405d-bd48-904a664f5d15.png)


### Issues
I am very keen on learning, however there were a few issues that I have encountered in the process that I did not have the time and the resources to address them. This will be areas of improvement when revisiting this repository.

#### Continuous Integration (CI) and Continuous Delivery
I was not able to perform this part of the task because I am very new to web development and I don't have the time and the resources to be able to learn and apply this on my current task. However, it is something that I aspire to learn and practice in the future.

#### Containerized Deployment
I have tried creating a Dockerfile for this application but I kept on getting conflicts with my existing requirements, so I will have to learn how to dockerize my app further in the future.

#### Ideal Model
I wasn't able to use the ideal model with the tuned hyperparameters and was retrained using the whole dataset because of the file size constrains. I was able to us LFS in GIT but I still exceeded the limit, so I had to recreate another model with the best hyperparameters but were using only a small portion of the dataset instead. The file size is significantly smaller compared to my initial ideal model.
![image](https://user-images.githubusercontent.com/102983286/177044622-f510abf7-dcf2-447b-8d61-cd0c2f08b523.png)


### Requirements
Here are the main requirements that I have used in order to produce the output:
* `PyWebIO>=1.6.1`
* `Flask>=2.1.2`
* `scikit-learn>-1.0.2`


### References
Here are a few of the references that I used in order to build the API:
* [How to Containerize a Flask application using Docker? | P-1](https://www.youtube.com/watch?v=jZB6OaHvPEQ)
* [Build a Rest API using Flask - P4- Python Flask tutorials](https://www.youtube.com/watch?v=8L_otSDvmR0)
* [Sklearn Regression Models](https://www.simplilearn.com/tutorials/scikit-learn-tutorial/sklearn-regression-models)
* [How to Deploy Flask API on Heroku?](https://geekyhumans.com/how-to-deploy-flask-api-on-heroku/)
* [API in 11 mins! Create and Deploy a Python Web API using Flask and Heroku](https://www.youtube.com/watch?v=m5TKQF7WJzc)

[1]: https://img.shields.io/badge/donate-gcash-green
[2]: https://drive.google.com/file/d/1JeMx5_S7VBBT-3xO7mV9YOMfESeV3eKa/view

[3]: https://img.shields.io/badge/donate-paypal-blue
[4]: https://www.paypal.com/paypalme/mcabanlitph

[5]: https://img.shields.io/badge/license-GNUGPLv3-blue.svg
[6]: https://github.com/mcabanlit/heart-disease/blob/main/LICENSE.md

[7]: https://img.shields.io/badge/python-3.10-blue
[8]: https://www.python.org/

[9]: https://img.shields.io/badge/pywebio-1.6.1-dark
[10]: https://pywebio.readthedocs.io/en/latest/

[11]: https://img.shields.io/badge/scikit--learn-1.0.2-orange
[12]: https://scikit-learn.org

[13]: https://img.shields.io/badge/build-passing-green
[14]: https://drug-store-chain.herokuapp.com/

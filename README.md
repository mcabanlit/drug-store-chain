# Sales Forecast API for a Drug Store Chain  [![gcash donation][1]][2] [![paypal donation][3]][4]

[![license][5]][6] [![python version][7]][8] [![pywebio version][9]][10] [![scikit version][11]][12] [![build][13]][14] 
 
Rossmann is Germany's second-largest drug store chain. We have been provided with historical sales data for 1,115 Rossmann stores. The task is to forecast the "Sales" column. The goal of this project would be (1) to create a model that would forecast the **sales** by using only these fields as inputs: `Store`, `DayOfWeek`, `Date`, `Customers`, `Open`, `Promo`, `StateHoliday` and `SchoolHoliday` and (2) to create and deploy an API that can serve prediction by receiving a JSON file via POST.

![Drug](https://images.unsplash.com/photo-1631549916768-4119b2e5f926?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1179&q=80)


### Files
Here are some files that may be important to those who would like to check the code or to thouse who would want to replicate the project.
* [app.py](https://github.com/mcabanlit/drug-store-chain/blob/main/app.py) - Contains
* [drug-store-sales-prediction.ipynb](https://github.com/mcabanlit/drug-store-chain/blob/main/drug-store-sales-prediction.ipynb) - Cheka
* [miniconda_requirements.txt](https://github.com/mcabanlit/drug-store-chain/blob/main/miniconda_requirements.txt) - Cheka
* [requirements.txt](https://github.com/mcabanlit/drug-store-chain/blob/main/requirements.txt) - Cheka 2
* [sales_prediction_small.pkl](https://github.com/mcabanlit/drug-store-chain/blob/main/sales_prediction_small.pkl) - Chesmes

### Dataset
For this project, we are given two sets of data, which are as follows:
* [train.csv](https://github.com/mcabanlit/drug-store-chain/blob/main/data/train.csv) - contains sales data on a daily frequency
* [store.csv](https://github.com/mcabanlit/drug-store-chain/blob/main/data/store.csv) - contains store information

### Models

### Usage

### Issues

### Requirements
* `PyWebIO>=1.6.1`
* `Flask>=2.1.2`
* `scikit-learn>-1.0.2`


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

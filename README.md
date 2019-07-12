# IPEDS Colleges Database

## Purpose
I am interested in the topic of higher education, and interested in knowing more about different institutions in terms of their characteristics, the student-faculty ratio, and enrollment percentage, etc. For this project, I am looking to build a Django app to demonstrate data of more than 5000 higher educational institutions in the US. 

## Dataset
This project is based on the 2016 survey data from IPEDS data center. The database for my Django app mainly includes the following data sets:

- __Institution__
  - this data set contains the information of each higher educational institution, including institution name, location (city and state), student-faculty ratio and percentage of admission.

- __Graduation number by race__
  - this data set listed the number of graduation by race

- __Academic domain__
  - this data set listed the academic domains with the number of programs offered in relevant domain

- __Academic Library__
  - this data set contain information about the academic libraries of institutions, including the type of collections and collection number in total.


## Data model

The data model that I designed looks as below:
![data model](https://github.com/yuanlii/MySQL-IPEDS-colleges/blob/master/static/img/data_model.png)


## Package Dependencies
This project is based on python3.6 and Django2.1.2

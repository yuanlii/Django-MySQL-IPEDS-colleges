# College Comparison Database

## Purpose
I am interested in the topic of higher education, and would like to know more about different institutions in terms of characteristics, organizations, enrollment rate, financial aid, etc. Fortunately, IPEDS data center -- which is the National Center for Education Statistics -- would provide people with open data sources covering almost every aspects of higher education institutions, so I am looking forward to utilize those public data to build a database and create a Django app as well to demonstrate those interesting information.

## Data set
IPEDS data center would conduct survey and release the survey results on a yearly basis, which would include a large number of datasets. After revieiwing the available data sets, I think it would be better to narrow down my project data to include the following contents:

[Institutions info]:
include the fundamental information about the institutions (only limited in the US), e.g:institution names, alias, geological location, zip code, etc.

[Comparison peers]: 
include the groups of institutions that are perceived as peers by our target institutions, e.g: name, location, etc.

[Fall enrollment]: 
include information about the fall enrollment rate in 2016
- Distance education 
- Faculty-student ratio 

[Admissions/Test Scores]: 
contain information about the admission criteria and test scores for higher educational institutions in the US in 2016

[Academic Library]: 
contain information about the academic libraries status among all the institutions, for example, the physical collection number, digital collection number, database percentage, and digital media percentage, etc.

## Data model

see static/img folder

## Package Dependencies

This project is based on python3.6 and Django2.1.2

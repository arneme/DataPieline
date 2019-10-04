# Data Pipeline project
This README file includes a summary of the Data Pipeline project, instructions on how to install Apache Airflow locally on your own computer (Mac OS X) and how to run the Airflow Python script on your local installation of Airflow. The Airflow script will initiate tasks to retrieve data from AWS S3 into Redshift and controlling transformation jobs in your AWS Redshift cluster).

## Table of Contents

1. [Summary of the Data Pipeline project](#summary)
2. [Install Airflow on local computer](#local_airflow)
3. [How to run the Airflow script on locally installed Airflow](#run)
4. [Notes](#notes)

## <a name="summary"></a>Summary of the Data Pipeline project
The underlying purpose of this project is to provide (the fictional company)Sparkify the necessary tool to retrieve vital, business oriented information about their service (music streaming). Their current main focus is to be able to, easily and fast, retrieve information about which songs users are listening to, most popular songs and artist etc. They do have information about this stored in logfiles already but it is not easy to search or aggregate data from these logfiles. 

In the Data Lake Pipeline project we have been asked to transform data from the logfiles together with meta data about songs (also stored in files) into a business oriented (star) database design that will allow Sparkify to meet their business need related to for example finding out which songs their users are listening to and when, the most popular songs and artists etc.

In the Data Pipeline project we will use Apache Airflow (installed locally on your computer) to control and schedule Redshift and S3 tasks that creates a business oriented star schema in Redshift from the log and song files. I.e. we will create artist, song, user, time dimension tables and a songplay fact table in Redshift. Airflow will be used to monitor and control (and schedule) a data pipeline reading data from S3 into Redshift and transforming the data into star schema oriented tables.

## <a name="local_airflow"></a>Install Airflow on your local computer
According to : https://airflow.apache.org/installation.html, Airflow installation on Unix and OS X is in principle simple as issuing:

*_pip install airflow_*

in a command window on you local Unix or Mac OS X computer. This will however only install a minimal version of Airflow without the necessary hooks needed for this project. To get the necessary hooks you will need to issue the following command (but install mysql first):

pip install apache-airflow[async,devel,crypto,hdfs,hive,password,postgres,s3]

On my Mac OS X computer this resulted in an error (saying that mysql was missing). I therefore installed MySQL and started MySQL like this:

*_brew install mysql_*
*_brew services start mysql_*

### Copy the project template files to your local Airflow directory
Download and unzip the project files from Udacity and move the resulting dags and plugins directory to your local _~/airflow_ folder (Airflow will create a _~/airflow_ folder during installation).

In the repository you will find a script called _start.sh_. To start Airflow on your local computer: run this script

_./start.sh_

It will start the Airflow webserver listening on port 80 on your local machine (change the port number if you want). In a browser window, go to http://localhost, this should bring up the Airflow web based GUI.

## <a name="run"></a>How to run the Airflow scripts

### Setup a Redshift Cluster using AWS Console
The Airflow python script _data\_pipeline.py_ is a script designed to run in Airflow and the script includes tasks that will run on Redshift. It is therefore necessary to have a live Redshift cluster up and running before the _data\_pipeline.py_ script can be run in Airflow. The next paragraphs describes the steps used in order to setup a Redshift cluster for this project.

#### Step 1


#### Setup Redshift Cluster


### Run _data\_pipeline.py_ in Airflow

## <a name="notes"></a>Notes
The _etl.py_ script assumes that a bucket called s3://data-lake-sparkify exists (this is where it will store the parquet files). Before you run the script you should create a bucket for the parquet files and change the name in the _etl.py_ file accordingly.

Since the etl.py script is uploaded to the master node there is no use for the dl.cfg file and it has not been included in the github repo as part of the submission.



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

***pip install airflow***

in a command window on you local Unix or Mac OS X computer. This will however only install a minimal version of Airflow without the necessary hooks needed for this project. To get the necessary hooks you will need to issue the following command (but install mysql first):

***pip install apache-airflow\[async,devel,crypto,hdfs,hive,password,postgres,s3\]***

On my Mac OS X computer this resulted in an error (saying that mysql was missing). I therefore installed MySQL and started MySQL like this:

***brew install mysql***

***brew services start mysql***

When airflow has been properly installed you will need to initialize the airflow dataabse by running this command:

airflow initdb

### Copy the project template files to your local Airflow directory
Download and unzip the project files from Udacity and move the resulting dags and plugins directory to your local _~/airflow_ folder (Airflow will create a _~/airflow_ folder during installation).

In the repository you will find a script called _start\_airflow.sh_. The script is a slightly modified version of the _start.sh_ script used by Udacity in their Data Pipeline Airflow Exercise VMs. To start Airflow on your local computer: run this script

***./start_airflow.sh***

It will start the Airflow webserver listening on port 80 on your local machine (change the port number if you want). In a browser window, go to http://localhost, this should bring up the Airflow web based GUI.

## <a name="run"></a>How to run the Airflow scripts

### Setup a Redshift Cluster using AWS Console
The Airflow python script _data\_pipeline.py_ is a script designed to run in Airflow and the script includes tasks that will run on Redshift. It is therefore necessary to have a live Redshift cluster up and running before the _data\_pipeline.py_ script can be executed in Airflow. The next paragraphs describes the steps used in order to setup a Redshift cluster for this project.

#### Setup Redshift Cluster
It is  necessary to setup the Redshift cluster that will be used by the airflow script in order for the script to run without errors. This can be done either in the AWS Console or programatically. I did it in the AWS Console using the Quick Deploy option (4 nodes, dc2.large), set user and password as wanted (this will be added to the airflow connection setup). **It is also important to edit the default security group (that quick launch adds to the cluster) to allow access from the IP address the airflow script is run on**. It is a good idea to run the cluster in region us-west-2 since the S3 bucket with data is in the same region (to minimise network traffic).

When creating the Redshift cluster I attached a role that allows the Redshift cluster to access S3 (read). This is necessary in order for the COPY SQL statements to work.

### Run _data\_pipeline.py_ in Airflow
Prerequisites:
1. Airflow is installed on your local computer (see above)
2. Copy the git repo *data_pipeline.py* to *~/airflow/dags*
3. You have a Redshift cluster up and running (see above) that allows inbound traffic from where you run the airflow script
4. You have started Airflow (using the ***./start_airflow.sh***)
5. You have added your AWS credentials and Redshiift connection settings in Airflow (se below)

#### Add AWS IaM credentials to Airflow
In order to run AWS commands in Airflow tasks you will have to add your AWS credentials to Airflow. This can be done from the Airflow web GUI:
1. Select Admin->Connection and click on the Create tab
2. Add *aws_credentials* in the **Conn Id** field
3. Add *Amazon Web Services* in the **Conn Type** field
4. Add your *AWS_ACCESS_KEY_ID* in the **Login field**
5. Add your *AWS_SECRET_ACCESS_KEY* in the **Password** 

#### Set redshift connection settings in Airflow
For Airflow scripts to be able to access your Redshift cluster it is necessary to add the Redshift cluster settings in Airflow. This can also be done using the Airflow web GUI:
1. Select Admin->Connection
2. Identify (or create one if not present) the redshift connection and click on it
3. Add *redshift* in the **Conn Id** field
4. Add *Postgres* in the **Conn Type** field
5. Add *public* in the **Schema** field (or something else if you want to create your own schema). Note however that if you change to a different schema you will have to create the schema first and change all the SQL statements to address tables in the new schema)
6. Set your clusters host name to the Endpoint of your cluster (without port), this can be found on the Clusters page in the Redshift dashboard in the AWS console)
7. Set **Login** field to your cluster login user and set **Password** field to your cluster login user password
8. Add *5439* in the **Port** field

#### Finally run the script
In the Airflow web based GUI:
1. In the DAGs list, identify the ***Data-Pipeline*** DAG
2. Click on the on/off slider to turn the DAG "on"

You can now check the results by using the Graph or Tree view in Airflow to check the execution of the tasks in the ***Data-Pipeline*** DAG.

## <a name="notes"></a>Notes
### Debugging tasks
Even though the Airflow web GUI is great it is also worth looking at the Airflow CLI. For example, if you want to test a single task you can run:

*airflow test Sparkify-Data-Pipeline Stage_events 2019-01-01*

To run the Stage_events task directly without running the whole *Sparkify-Data-Pipeline* DAG. You will then see all the log entries from Airflow directly in your command window and this is really great when debugging tasks (a lot faster and you will see error messages directly)

I have also added a dag parameter called debug. Setting the debug parameter results in that the redshift SQL will be printet in the log but not executed. This was a great tool when testing and debugging.

### Using the provided template
The template file does not include separate create tasks so I have included creating the tables in the Stage and Load operators (although I think it would have been a good idea to separate them. Ref: properly scoped tasks minimize dependencies and are often more easily parallelized :-))

The provided template separates operators for Staging, LoadFact and LoadDimension. During development of this project I realized that this is strictly not necessary when my sql statements file is structured as it is. It would in prinsiple have bben enough with one MyRedshiftOperator that could be fully capable of doing the operations without duplicating the code. The color setting could just have been a parameter in the task definitions in the dag file.



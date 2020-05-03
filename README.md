# parallelSVM
Spring 2020 CS626 Final Project by Michael Dingess Tanner Coffman

# Setup

Install pip with:

`sudo yum -y install pip`

Instal the MapReduce package with:

`sudo pip install mrjob`

# Execution

Use the Makefile to put the adult dataset data in the hdfs:

`make putFullData`

Use the Makefile to run the system on the dataset

`make run`

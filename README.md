# parallelSVM
Spring 2020 CS626 Final Project by Michael Dingess Tanner Coffman


# Setup with Anaconda

 With anaconda installed, run the following commands to create and activate the necessary environment for this application.

	conda create -n p27parallelsvm python=2.7

	source activate p27parallelsvm

	conda install -c conda-forge mrjob

	conda install numpy

 Confirm [y] any new packages that will be installed.

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

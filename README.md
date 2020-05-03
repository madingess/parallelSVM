# parallelSVM
Spring 2020 CS626 Final Project by Michael Dingess Tanner Coffman


# Install Anaconda2

 Installation for anaconda2 via cli as of 05/03/2020:

	wget -c https://repo.anaconda.com/archive/Anaconda2-2019.10-Linux-x86_64.sh

	bash Anaconda2-2019.10-Linux-x86_64.sh

 Read and agree to the license agreement. Confirm the default location and initial configuration.
	

# Setup with Anaconda

 With anaconda installed, run the following commands to create and activate the necessary environment for this application.

 For non-cloudera users:

	conda create -n p27parallelsvm python=2.7

	source activate p27parallelsvm

	conda install -c conda-forge mrjob

	conda install numpy

 Confirm [y] any new packages that will be installed.

 For Cloudera Quickstart users: (assuming you installed anaconda2 in the default location)

	/home/cloudera/anaconda2/bin/conda create -n p27parallelsvm python=2.7

	/home/cloudera/anaconda2/bin/activate p27parallelsvm

	/home/cloudera/anaconda2/bin/conda install -c conda-forge mrjob

	/home/cloudera/anaconda2/bin/conda install numpy

 Confirm [y] any new packages that will be installed.

# Setup

Install pip with:

`sudo yum -y install pip`

Instal the MapReduce package with:

`sudo pip install mrjob`


# Execution

 Activate the python2.7 environment if you haven't already:

	source activate p27parallelsvm

 Use the Makefile to put the adult dataset data in the hdfs:

	make putFullData

 Use the Makefile to run the system on the dataset:

	make run

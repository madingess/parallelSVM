run: 
	python2 src/main.py inputs/adult.data
#	python2 src/main.py inputs/test1.data outputs/
#	python2 src/main.py /user/cloudera/parallelSVM/input/ /user/cloudera/parallelSVM/output/


# It is unknown to me whether the input is supposed to come from the local fs or the
#  hdfs. The application seems to only work when invoking from the local fs. As
#  such, the commands below are not necessary.

putTestData: mkdirs
	hadoop fs -put inputs/test1.data /user/cloudera/parallelSVM/input

putFullData: mkdirs
	hadoop fs -put inputs/adult.data /user/cloudera/parallelSVM/input

mkdirs:
	hadoop fs -rm -f -r /user/cloudera/parallelSVM/input
	hadoop fs -rm -f -r /user/cloudera/parallelSVM/output
	hadoop fs -mkdir -p /user/cloudera/parallelSVM/
	hadoop fs -mkdir /user/cloudera/parallelSVM/input/
	hadoop fs -mkdir /user/cloudera/parallelSVM/output/

showResult:
	hadoop fs -cat /user/cloudera/parallelSVM/output/*


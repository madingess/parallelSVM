run: jar
	hadoop fs -rm -f -r  /user/cloudera/parallelSVM/output
	hadoop jar parallelSVM.jar org.myorg.ParallelSVM /user/cloudera/parallelSVM/input /user/cloudera/parallelSVM/output

compile: build/org/myorg/ParallelSVM.class

jar: parallelSVM.jar

parallelSVM.jar: build/org/myorg/ParallelSVM.class
	jar -cvf parallelSVM.jar -C build/ .

build/org/myorg/ParallelSVM.class: ParallelSVM.java
	mkdir -p build
	javac -cp /usr/lib/hadoop/*:/usr/lib/hadoop-mapreduce/* ParallelSVM.java -d build -Xlint

clean:
	rm -rf build parallelSVM.jar 

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


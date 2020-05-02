package org.myorg;

import java.io.IOException;
import java.util.regex.Pattern;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;

import org.apache.log4j.Logger;

public class ParallelSVM extends Configured implements Tool {

  private static final Logger LOG = Logger.getLogger(ParallelSVM.class);

  public static void main(String[] args) throws Exception {
    int res = ToolRunner.run(new ParallelSVM(), args);
    System.exit(res);
  }

  public int run(String[] args) throws Exception {
    Job job = Job.getInstance(getConf(), "parallelSVM");
    job.setJarByClass(this.getClass());
    // Use TextInputFormat, the default unless job.setInputFormatClass is used
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    job.setMapperClass(Map.class);
    job.setReducerClass(Reduce.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);
    job.setMapOutputKeyClass(IntWritable.class);
    job.setMapOutputValueClass(DoubleWritable.class);

    // Wait for completion; return completion value at the end of the method
    Boolean ret = job.waitForCompletion(true);
    return ret ? 0 : 1;
  }


  public static class Map extends Mapper<LongWritable, Text, IntWritable, DoubleWritable> {

    /* 
     * THIS IS CURRENTLY JUST A COPY OF MY HW2 Part1.java file 
     *
     * TODO: 
     *       Delete current Mapper logic
     *       Implemente parallelSVM Mapper logic
     *       May need to change MapOutput Key/Value Class in main
     */

    private final static IntWritable male = new IntWritable(1);
    private final static IntWritable female = new IntWritable(2);
    private static final Pattern WORD_BOUNDARY = Pattern.compile("\\s*,\\s*");

    public void map(LongWritable offset, Text lineText, Context context) 
        throws IOException, InterruptedException {
      String line = lineText.toString();

      // Parse the line as:
      //    pid  gender  race  height  weight  asthma  hypertension
      // Split should give array of seven string
      String[] linesplit = WORD_BOUNDARY.split(line);

      LOG.info("HERE BE SPLIT LINE");
      LOG.info(String.valueOf(linesplit.length));
      LOG.info(linesplit[0]);
      LOG.info(linesplit[1]);
      LOG.info(linesplit[2]);
      LOG.info(linesplit[3]);
      
      if (linesplit.length != 7)
        throw new IOException("Line Parsing Failed.");
      
      // Check that we are not operating on the header line of the csv
      //   and that the gender is not null
      //   and that the height is not null
      if(linesplit[0].compareTo("pid") != 0 && 
         linesplit[1].compareTo("NULL") != 0) {
   
        String gender = linesplit[1];
        DoubleWritable height;
        if (linesplit[3].compareTo("NULL") == 0)
          height = new DoubleWritable((Double) 0.0);
        else
          height = new DoubleWritable(Double.parseDouble(linesplit[3]));

        if (gender.compareTo("1") == 0)    // if male
          context.write(male, height);
        else                               // else female
          context.write(female, height);
      }
    }
  }


  public static class Reduce extends Reducer<IntWritable, DoubleWritable, Text, Text> {

    /* 
     * THIS IS CURRENTLY JUST A COPY OF MY HW2 Part1.java file 
     *
     * TODO: 
     *       Delete current Reducer logic
     *       Implemente parallelSVM Reducer logic
     *       May need to change Output Key/Value Class in main
     */

    private final static IntWritable male = new IntWritable(1);
    private final static IntWritable female = new IntWritable(2);
    private final static Text maleText = new Text("male");
    private final static Text femaleText = new Text("female");

    @Override
    public void reduce(IntWritable gender, Iterable<DoubleWritable> heights, Context context)
        throws IOException, InterruptedException {

      int genderCount = 0;
      double maxHeight = 0.0;
      for (DoubleWritable height : heights) {
        genderCount += 1;
        if (height.get() > maxHeight) {
          maxHeight = height.get();
        }
      }

      Text outputGenderHeight = new Text(String.valueOf(genderCount) + " " + String.valueOf(maxHeight));

      // Write to context
      if (gender.equals(male)) 
        context.write(maleText, outputGenderHeight);
      else 
        context.write(femaleText, outputGenderHeight);
    }
  }
}

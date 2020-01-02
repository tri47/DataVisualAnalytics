package edu.gatech.cse6242;
import java.io.IOException;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q1 {

  public static class emailmapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        public void map (LongWritable key, Text value, Context context) throws IOException, InterruptedException {
	    
	    String line = value.toString();
	    String[] columns = line.split("\t");
            int weight = Integer.parseInt(columns[2]);
	    context.write(new Text(columns[1]), new IntWritable(weight));
	}
    }


   public static class emailreducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        public void  reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
	    int sum = 0;
	    for (IntWritable count : values) {
		sum += count.get();
	    }
	   
	    context.write(key, new IntWritable(sum));
	}
    }


  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    
   Job job = Job.getInstance(conf, "Q1");
    job.setJarByClass(Q1.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
   job.setMapperClass(emailmapper.class);
    job.setReducerClass(emailreducer.class);    

    /* TODO: Needs to be implemented */
    job.setMapOutputKeyClass(Text.class);
    job.setMapOutputValueClass(IntWritable.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);

 


   


    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}

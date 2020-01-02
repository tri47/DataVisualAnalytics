package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4 {


  public static class diffmapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        public void map (LongWritable key, Text value, Context context) throws IOException, InterruptedException {
	    
	    String line = value.toString();
	    String[] columns = line.split("\t");
	    context.write(new Text(columns[0]), new IntWritable(1));
	    context.write(new Text(columns[1]), new IntWritable(-1));
	}
    }


  public static class histmapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        public void map (LongWritable key, Text value, Context context) throws IOException, InterruptedException {
	    
	    String line = value.toString();
	    String[] columns = line.split("\t");
	    context.write(new Text(columns[1]), new IntWritable(1));
	}
    }


   public static class diffreducer extends Reducer<Text, IntWritable, Text, IntWritable> {
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
    Job job1 = Job.getInstance(conf, "Q4 1");
    Path out = new Path(args[1]);
    Path temp_path = new Path("temp_job_big");
    job1.setJarByClass(Q4.class);
    job1.setMapperClass(diffmapper.class);
    job1.setReducerClass(diffreducer.class);    
    job1.setOutputKeyClass(Text.class);
    job1.setOutputValueClass(IntWritable.class);

   
    FileInputFormat.addInputPath(job1, new Path(args[0]));
    FileOutputFormat.setOutputPath(job1, temp_path);
    job1.waitForCompletion(true);


    Job job2 = Job.getInstance(conf, "Q4 2");


    job2.setJarByClass(Q4.class);
    job2.setMapperClass(histmapper.class);
    job2.setReducerClass(diffreducer.class);    
    job2.setOutputKeyClass(Text.class);
    job2.setOutputValueClass(IntWritable.class);
 
    FileInputFormat.addInputPath(job2, temp_path);
    
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));
    
   

    job2.waitForCompletion(true); 
    	temp_path.getFileSystem(conf).delete(temp_path,true); 
    
   /* System.exit(job2.waitForCompletion(true) ? 0 : 1); */
  }
}

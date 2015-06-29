#!/bin/bash

hbase org.apache.hadoop.hbase.mapreduce.ImportTsv '-Dimporttsv.separator=,' -Dimporttsv.columns=HBASE_ROW_KEY,f:name,f:count rsvp_graph /user/meetup_output_hive/000000_0


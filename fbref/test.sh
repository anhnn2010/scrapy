#!/bin/bash

cat result.csv | awk -F, '{print $1}' | sed '/Name/d' | sort -u > test_result
cat fbref.log | grep 'Scraped from' | awk -F/ '{print $NF}' | sed 's/-Match-Logs>//g' | sed 's/-/ /g' | sort -u > test_log

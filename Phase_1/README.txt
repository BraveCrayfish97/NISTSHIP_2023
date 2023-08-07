ORDER OF EXECUTION
1. DataFormatter2018.py- for some of the runs in 2018, the data has spaces between first character and the rest of run name which needs to be corrected by this script
2. TRECVID_Ranker.py


REQUIRED ARGS
DataFormatter2018.py - NO ARGS, however, there is a 'folder' variable in file that must point to the 2018 Metric Ranking Data
TRECVID_Ranker.py - MetricRankingDataFolder


OUTPUT FOLDER FORMAT
tv(year)_Output_Data


OUTPUT FORMAT - tv(year).FinalRankings.txt
"RUN_NAME      SCORE" - the SCORE is the sum of the ranking for that given run across all the metrics

OUTPUT FORMAT - tv(year).(METRIC)vsFINAL.png
Each point represents one run
X-Value is the FinalRanking of that run
Y-Value is the (METRIC)Ranking of that run
R-squared value in top left of graph


 - for some of the runs in 2018, the data has spaces between first character and the rest of run name which needs to be corrected by this script
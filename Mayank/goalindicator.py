import pandas as pd
import math
excelpath = "/Volumes/Mayank HDD/Fraunhofer Project/Semeval/Semeval3.csv"
df = pd.read_csv(excelpath, index_col=0)



for row in range(0, len(df)):

    if pd.isnull(df['2nd_Action'][row]) is False:
        if df['2nd_Action_start'][row] < df['1st_spatial_indicator_start_word_index'][row]:
            df.at[row, 'goal_indicator_start_word'] = df['1st_spatial_indicator_start_word'][row]
            df.at[row, 'goal_indicator_start_word_index'] = df['1st_spatial_indicator_start_word_index'][row]
            df.at[row, 'goal_indicator_end_word'] = df['1st_spatial_indicator_end_word'][row]
            df.at[row, 'goal_indicator_end_word_index'] = df['1st_spatial_indicator_end_word_index'][row]

        else:
            df.at[row, 'goal_indicator_start_word'] = df['2nd_spatial_indicator_start_word'][row]
            df.at[row, 'goal_indicator_start_word_index'] = df['2nd_spatial_indicator_start_word_index'][row]
            df.at[row, 'goal_indicator_end_word'] = df['2nd_spatial_indicator_end_word'][row]
            df.at[row, 'goal_indicator_end_word_index'] = df['2nd_spatial_indicator_end_word_index'][row]
    else:
        continue
df.to_csv('/Volumes/Mayank HDD/Fraunhofer Project/Semeval/Semeval4.csv')

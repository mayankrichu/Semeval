import nltk
from classifywords import sepwords
import spacy
nlp = spacy.load("en_core_web_sm", disable =['ner', 'parser', 'textcat'])
import pandas as pd
import re
import xlrd
import math


def check_indicator(sentence, line_num):

    count = 0
    indicator = 1
    doc = nlp(sentence)
    temp_word = ""
    colors = [df['1_Color'][line_num], df['2_Color'][line_num],
                           df['3_Color'][line_num], df['4_Color'][line_num], df['5_Color'][line_num]]

    trajectors = [df['1_Trajector'][line_num], df['2_Trajector'][line_num],
                           df['3_Trajector'][line_num]]

    directions = ["right", "left", "center", "back"]

    entitities = colors + trajectors + directions
    entitities = [item for item in entitities if not(pd.isnull(item)) == True]

    for idx, word in enumerate(doc):
        word_pos = word.pos_
        word_tag = word.tag_
        word = (word.text).lower()

        end = 0

        if (word_tag == 'IN' or word_tag == 'WDT') and count == 0:
            count += 1
            df.at[line_num, f'{indicator}_indicator_start_word'] = word
            df.at[line_num, f'{indicator}_indicator_start_word_index'] = idx
            start = idx

        elif word in entitities and count == 1:

            if doc[idx-1].text.lower() == "the" or doc[idx-1].text.lower() == "single"\
                    or doc[idx-1].text.lower() == "double":
                if doc[idx-1].text.lower() == "single" or doc[idx-1].text.lower() == "double":
                    df.at[line_num, 'cardinality'] = doc[idx-1].text.lower()
                    df.at[line_num, 'cardinality_start_index'] = idx-1
                    df.at[line_num, 'cardinality_end_index'] = idx


                else:
                    df.at[line_num, f'{indicator}_indicator_end_word'] = doc[idx-2].text.lower()
                    df.at[line_num, f'{indicator}_indicator_end_word_index'] = idx-1
                    end = idx-1
            else:
                df.at[line_num, f'{indicator}_indicator_end_word'] = doc[idx - 1].text.lower()
                df.at[line_num, f'{indicator}_indicator_end_word_index'] = idx
                end = idx

            count = 0
            df.at[line_num, f"{indicator}_indicator_words"] = doc[start:end].text.lower()

            indicator += 1


    #print(start)
    #print(end)
    #print(indicator)



if __name__ == "__main__":
    #path for the semeval data
    path = "semeval-2014-task6/train_data/commands.txt"
    #loading the Semeval1.csv file
    excelpath = "/Volumes/Mayank HDD/Fraunhofer Project/Semeval/Semeval1.csv"
    df = pd.read_csv(excelpath, index_col=0) #new unwanted column won't be created
    file = open(path)
    lines = file.readlines()
    count = 0
    mydict = {}
    mylist = []
    #df = pd.DataFrame()
    for line_num in range(0, len(lines)):
      line = lines[line_num]
      line = line.strip()
      pattern = r'[0-9]'
      sentence = re.sub(pattern, '', line)
      sentence = sentence.strip()
      check_indicator(sentence, line_num)
    #storing it to Semeval2 file
    df.to_csv('/Volumes/Mayank HDD/Fraunhofer Project/Semeval/Semeval2.csv')
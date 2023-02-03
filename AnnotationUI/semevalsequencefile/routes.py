from flask import Blueprint, render_template, request, jsonify, redirect, url_for, jsonify
import json
import pandas as pd
from Mayank.AnnotationUI.variables import semeval_file_path, annotated_file_path, True_annotated_file_path, False_annotated_file_path


semevalsequencefile = Blueprint('semevalsequencefile', __name__)

#display the generated annotated data from the json file

colors = {
    "Action" : "red",
    "Trajector" : "blue",
    "Color" : "green"
}

@semevalsequencefile.route('/', methods=['GET', 'POST'])
def Semevalsequencefile():
    #read the file
    print("here")
    return render_template('semevalsequencefile.html')

@semevalsequencefile.route('/SemevalsequencefileSubmit', methods =['POST'])
def SemevalsequencefileSubmit():
    if request.method == 'POST':
        global sequencenumber
        try:
            sequencenumber = request.form['text']
        except:
            print("exception occured")
        color = []
        entity = []
        df = pd.read_csv(semeval_file_path, index_col=0)
        df_row = df.loc[int(sequencenumber)]
        for idx, word in enumerate(df_row['sentence'].split()):
            try:
                if word == df_row['1_Action']:
                    entity.append(word)
                    color.append("Green")
                elif word == df_row['2_Action']:
                    entity.append(word)
                    color.append("Green")
                elif word == df_row['1_Trajector'] :
                    entity.append(word)
                    color.append("Blue")
                elif word == df_row['2_Trajector'] :
                    entity.append(word)
                    color.append("Blue")
                elif word == df_row['3_Trajector'] :
                    entity.append(word)
                    color.append("Blue")
                elif word == df_row['1_Color'] :
                    entity.append(word)
                    color.append("red")
                elif word == df_row['2_Color'] :
                    entity.append(word)
                    color.append("red")
                elif word == df_row['3_Color'] :
                    entity.append(word)
                    color.append("red")
                elif word == df_row['4_Color'] :
                    entity.append(word)
                    color.append("red")
                elif word == df_row['5_Color'] :
                    entity.append(word)
                    color.append("red")
                elif word == df_row['6_Color'] :
                    entity.append(word)
                    color.append("red")
                elif (word in df_row['1_indicator_words'].split()):
                    entity.append(word)
                    color.append("grey")
                elif (word in df_row['2_indicator_words'].split()):
                    entity.append(word)
                    color.append("grey")
                else:
                    entity.append(word)
                    color.append("black")

            except:
                continue

        filepath = f"{annotated_file_path}{sequencenumber}.json"

        with open(filepath) as json_file:
            data = json.load(json_file)
        print(data)
    return render_template('semevalidentification.html', data= data, entities_json = data['entities'], relations_json = data['relations'], sequencenumber=sequencenumber, entities = entity, colors =color, sentence = df_row['sentence'].split())






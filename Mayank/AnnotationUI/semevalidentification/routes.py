from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from Mayank.AnnotationUI.variables import semeval_file_path, annotated_file_path, True_annotated_file_path, False_annotated_file_path
import json
import pandas as pd
#semeval_file_path = "/Volumes/Mayank HDD/Fraunhofer Project/Semeval/Semeval2.csv"
semevalidentification = Blueprint('semevalidentification', __name__)


#display the generated annotated data from the json file

@semevalidentification.route('/Semevalidentification',methods=['GET', 'POST'])
def Semevalidentification(filepath):
    #read the file
    return render_template('semevalidentification.html', data = json.dumps(data, indent=4))

@semevalidentification.route('/SemevalidentificationSubmit',methods=['GET', 'POST'])
def SemevalidentificationSubmit():
    #read the file
    if request.method == 'POST':
        option = request.form['options']
        df = pd.read_csv(semeval_file_path, index_col=0)
        df = df.reset_index(drop=True)

        sequencenumber = int(request.form['sequencenumber'])
        sequencenumber += 1
        color = []
        entity = []
        df = pd.read_csv(semeval_file_path, index_col=0)
        df_row = df.loc[int(sequencenumber)]
        for idx, word in enumerate(re.split("[,.\s]", df_row['sentence'])):
            word = word.lower()
            try:
                first_indicator_words = df_row['1_indicator_words'].split()
            except:
                first_indicator_words =  ""
            try:
                second_indicator_words = df_row['2_indicator_words'].split()
            except:
                second_indicator_words = ""
            if word == df_row['1_Action']:
                entity.append(word)
                color.append("Green")
            elif word == df_row['2_Action']:
                entity.append(word)
                color.append("Green")
            elif word == df_row['1_Trajector']:
                entity.append(word)
                color.append("Blue")
            elif word == df_row['2_Trajector']:
                entity.append(word)
                color.append("Blue")
            elif word == df_row['3_Trajector']:
                entity.append(word)
                color.append("Blue")
            elif word == df_row['1_Color']:
                entity.append(word)
                color.append("red")
            elif word == df_row['2_Color']:
                entity.append(word)
                color.append("red")
            elif word == df_row['3_Color']:
                entity.append(word)
                color.append("red")
            elif word == df_row['4_Color']:
                entity.append(word)
                color.append("red")
            elif word == df_row['5_Color']:
                entity.append(word)
                color.append("red")
            elif word == df_row['6_Color']:
                entity.append(word)
                color.append("red")
            elif (word in first_indicator_words):
                entity.append(word)
                color.append("grey")
            elif (word in second_indicator_words):
                entity.append(word)
                color.append("grey")
            else:
                entity.append(word)
                color.append("black")

        print(entity)
        print(color)

        df.at[sequencenumber, 'Accurate'] = option
        filepath = f"{annotated_file_path}{sequencenumber}.json"
        with open(filepath) as json_file:
            data = json.load(json_file)
        if option == "True":
            with open(f"{True_annotated_file_path}{sequencenumber}.json", "w") as f:
                json.dump(data, f)
        if option == "False":
            with open(f"{False_annotated_file_path}{sequencenumber}.json", "w") as f:
                json.dump(data, f)
    return render_template('semevalidentification.html', data = data, option = option, sequencenumber=sequencenumber, entities = entity, colors =color, sentence = df_row['sentence'].split(), entities_json = data['entities'], relations_json = data['relations'])


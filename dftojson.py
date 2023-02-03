import pandas as pd
import math
#load from the Semeval2.csv file
excelpath = "/Volumes/Mayank HDD/Fraunhofer Project/Semeval/Semeval2.csv"
df = pd.read_csv(excelpath, index_col=0)
import json

def check_indicator_type(indicator_index, row):

    if pd.isnull(df['2_Action'][row]) is True:
        if df['1_indicator_start_word_index'][row] == indicator_index and pd.isnull(df['2_indicator_start_word_index'][row]) is True:
            if df['1_Action'][row] not in ["pick", "take", "grab", "hold"] and df['1_indicator_start_word'][row] != "from":
                return "Goal Indicator"
            else:
                return "Spatial Indicator"
        elif df['1_indicator_start_word_index'][row] == indicator_index and pd.isnull(df['2_indicator_start_word_index'][row]) is False:
            return "Spatial Indicator"
        else:
           return "Goal Indicator"
    else:
        if df['1_indicator_start_word_index'][row] == indicator_index and df['2_Action_start'][row] < indicator_index\
                and pd.isnull(df['2_indicator_start_word'][row]) is True:
            return "Goal Indicator"

        elif df['1_indicator_start_word_index'][row] == indicator_index and df['2_Action_start'][row] < indicator_index \
                and pd.isnull(df['2_indicator_start_word_index'][row]) is False:
            return "Spatial Indicator"

        elif df['2_indicator_start_word_index'][row] == indicator_index and df['2_Action_start'][row] < indicator_index\
                and pd.isnull(df['3_indicator_start_word_index'][row]) is False:
            return "Spatial Indicator"

        elif df['2_indicator_start_word_index'][row] == indicator_index and df['2_Action_start'][row] < indicator_index\
                and pd.isnull(df['3_indicator_start_word_index'][row]) is True:
            return "Goal Indicator"

        elif df['3_indicator_start_word_index'][row] == indicator_index:
            return "Goal Indicator"
        else:
            return "Spatial Indicator"



for row in range(0, len(df)):
    dict = {}
    entities_list = []
    indicators_list = []
    if pd.isnull(df['1_Action'][row]) is False:
        entities_list.append( {
                "start" : int(df['1_Action_start'][row]),
                "end" : int(df['1_Action_end'][row]),
                "type": "Action"
            })
    if pd.isnull(df['2_Action'][row]) is False:
        entities_list.append( {
                "start" : int(df['2_Action_start'][row]),
                "end" : int(df['2_Action_end'][row]),
                "type": "Action"
            })

    if pd.isnull(df['1_Color'][row]) is False:
        entities_list.append({
            "start": int(df['1_Color_start'][row]),
            "end": int(df['1_Color_end'][row]),
            "type": "Color"
        })

    if pd.isnull(df['2_Color'][row]) is False:
        entities_list.append({
            "start": int(df['2_Color_start'][row]),
            "end": int(df['2_Color_end'][row]),
            "type": "Color"
        })

    if pd.isnull(df['3_Color'][row]) is False:
        entities_list.append({
            "start": int(df['3_Color_start'][row]),
            "end": int(df['3_Color_end'][row]),
            "type": "Color"
        })

    if pd.isnull(df['4_Color'][row]) is False:
        entities_list.append({
            "start": int(df['4_Color_start'][row]),
            "end": int(df['4_Color_end'][row]),
            "type": "Color"
        })

    if pd.isnull(df['1_Trajector'][row]) is False:
        entities_list.append({
            "start": int(df['1_Trajector_start'][row]),
            "end": int(df['1_Trajector_end'][row]),
            "type": "Trajector"
        })
    if pd.isnull(df['2_Trajector'][row]) is False:
        entities_list.append({
            "start": int(df['2_Trajector_start'][row]),
            "end": int(df['2_Trajector_end'][row]),
            "type": "Trajector"
        })
    if pd.isnull(df['3_Trajector'][row]) is False:
        entities_list.append({
            "start": int(df['3_Trajector_start'][row]),
            "end": int(df['3_Trajector_end'][row]),
            "type": "Trajector"
        })

    if pd.isnull(df['cardinality'][row]) is False:
        entities_list.append({
            "start": int(df['cardinality_start_index'][row]),
            "end": int(df['cardinality_end_index'][row]),
            "type": "Cardinal"
        })

    try:
        if pd.isnull(df['1_indicator_start_word'][row]) is False:
            indicator_type = check_indicator_type(int(df['1_indicator_start_word_index'][row]), row)
            entities_list.append({
            "start": int(df['1_indicator_start_word_index'][row]),
            "end": int(df['1_indicator_end_word_index'][row]),
            "type": f"{indicator_type}"
        })

        if pd.isnull(df['2_indicator_start_word'][row]) is False:
            indicator_type = check_indicator_type(int(df['2_indicator_start_word_index'][row]), row)
            entities_list.append({
            "start": int(df['2_indicator_start_word_index'][row]),
            "end": int(df['2_indicator_end_word_index'][row]),
            "type": f"{indicator_type}"
        })

        if pd.isnull(df['3_indicator_start_word'][row]) is False:
            indicator_type = check_indicator_type(int(df['3_indicator_start_word_index'][row]), row)
            entities_list.append({
            "start": int(df['3_indicator_start_word_index'][row]),
            "end": int(df['3_indicator_end_word_index'][row]),
            "type": f"{indicator_type}"
        })

    except:
        print(f"Please check {row}")


    dict = {"sentence" : df['sentence'][row], "entities" : entities_list}
    relations = []
    action_count = 0
    second_action_index = 0
    trajector_count = 0
    for idx, entity in enumerate(dict['entities']):

        if entity["type"] == "Action" and action_count == 0:
            action_count += 1
            first_action_index = idx

        elif entity["type"] == "Trajector" and trajector_count == 0 :
            trajector_count+=1
            first_trajector_index = idx

        elif entity["type"] == "Action" and action_count == 1:
            action_count+=1
            second_action_index = idx


        elif entity["type"] == "Goal Indicator" and action_count == 2:
            relations.append( {
                "type": "Transition",
                "head": f"{second_action_index}",
                "tail" : f"{idx}"

            })
        elif entity["type"] == "Goal Indicator" and action_count == 1:
            relations.append({
                "type": "Transition",
                "head": f"{first_action_index}",
                "tail": f"{idx}"

            })
        elif entity["type"] == "Spatial Indicator" and trajector_count ==1 :

            relations.append({
                "type": "Spatial",
                "head": f"{first_trajector_index}",
                "tail" : f"{idx}"

            })

    dict['relations'] = relations

    with open(f'/Volumes/Mayank HDD/Fraunhofer Project/Semeval/Semeval_Annotated/{row}.json', 'w+') as f:
        json.dump(dict, f)

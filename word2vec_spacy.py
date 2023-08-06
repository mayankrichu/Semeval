from classifywords import sepwords
import re
import pandas as pd
import xlwt
import nltk
import spacy
import matplotlib.colors as mcl

nlp = spacy.load("en_core_web_lg")
# Category -> words

data = {
  'Trajector': ['block','pyramid','prism','cube', 'brick', 'board', 'boards', 'planks', 'slat'],
  'Colors': ['yellow', 'red', 'green', 'magenta'],
  'Action': ['pick','place', 'drop', 'remove', 'Hold', 'put'],


}
# Words -> category
data_embeddings = {}

categories = {word: key for key, words in data.items() for word in words}

for category, elements in data.items():
    for element in elements:
        data_embeddings[element] = nlp(element).vector


# Processing the query
def process(query):
  query_embed = nlp(query).vector
  scores = {}
  for word, embed in data_embeddings.items():
    category = categories[word]
    dist = query_embed.dot(embed)
    dist /= len(data[category])
    scores[category] = scores.get(category, 0) + dist
  return scores

def maxscore(wordscore):

    maxkeyvalue = max(zip(wordscore.values(), wordscore.keys()))[1]
    maxkey = max(zip(wordscore.values(), wordscore.keys()))[0]

    return maxkeyvalue, maxkey


def check_action_color_trajector(text, index):
    text = text.lower()

    colors_count = 0
    action_count = 0
    trajector_count = 0
    doc = nlp(text)

    for idx, token in enumerate(doc):

        token_pos = token.pos_
        token_tag = token.tag_
        token_is_stop = token.is_stop
        token = (token.text).lower()
        #print(token,token_pos,token_tag)

        if token in ['of', 'is', 'corner', 'beside', 'on', 'the', 'left', 'placed'] :
           continue

        #if token in ['which', 'that']

        try:
            wordscore = process(token)
            entity = maxscore(wordscore)[0]
            entityvalue = maxscore(wordscore)[1]

            '''
            color
            '''
            if entity == 'Colors' and token in mcl.CSS4_COLORS:

                colors_count+=1
                start = idx
                end = idx+1
                df.at[index, f'{colors_count}_Color'] = token
                df.at[index, f'{colors_count}_Color_start'] = start
                df.at[index, f'{colors_count}_Color_end'] = end


            #Trjector
            elif entity == 'Trajector' and token_pos == "NOUN" :
                trajector_count +=1
                df.at[index, f'{trajector_count}_Trajector'] = token
                start = idx
                end = idx + 1
                df.at[index, f'{trajector_count}_Trajector_start'] = start
                df.at[index, f'{trajector_count}_Trajector_end'] = end


            elif entity == 'Action' and token_pos == "VERB" and (token_tag == 'VB' or token_tag =='VBD') or token == "place":

                action_count += 1
                start = idx
                end = idx + 1
                df.at[index, f'{action_count}_Action'] = token
                df.at[index, f'{action_count}_Action_start'] = start
                df.at[index, f'{action_count}_Action_end'] = end



        except:
            print("Errror")


def tokenizeworddf(seperatewords, i):
    '''
    tokenize word in seperate cell
    :param seperatewords:
    :param i:
    :return:
    '''
    for idx, j in enumerate(seperatewords):
        df.at[i, f'*{idx}*'] = j

print(process("Move"))
print(process("put"))
print(process("turquoise"))

if __name__ == "__main__":
    #path for the semeval data
    path = "semeval-2014-task6/train_data/commands.txt"
    file = open(path)
    lines = file.readlines()
    count = 0
    mydict = {}
    mylist = []
    df = pd.DataFrame()
    df = df.reset_index(drop=True)
    for i in range(0, len(lines)):
      line = lines[i]
      line = line.strip()
      pattern = r'[0-9]'
      new_text = re.sub(pattern, '', line)
      new_text = new_text.strip()
      #seperatewords = sepwords(new_text)
      df.at[i, 'sentence'] = new_text
      check_action_color_trajector(new_text, i)
    df = df.reset_index(drop=True)
    #path for the output
    df.to_csv('/Volumes/Mayank HDD/Fraunhofer Project/Semeval/Semeval1.csv')

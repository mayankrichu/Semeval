import numpy as np
from classifywords import sepwords
import re
import pandas as pd
# Category -> words

data = {
  'Trajector': ['block','pyramid','prism','cube', 'brick'],
  'Colors': ['yellow', 'red', 'green', 'magenta'],
  'Action': ['pick','place', 'drop', 'remove', 'Hold'],

}
# Words -> category


categories = {word: key for key, words in data.items() for word in words}


# Load the whole embedding matrix
embeddings_index = {}
with open('/Volumes/Mayank HDD/Fraunhofer Project/Semeval/glove.6B.100d.txt') as f:
  for line in f:
    values = line.split()
    word = values[0]
    embed = np.array(values[1:], dtype=np.float32)
    embeddings_index[word] = embed
print('Loaded %s word vectors.' % len(embeddings_index))
# Embeddings for available words
data_embeddings = {key: value for key, value in embeddings_index.items() if key in categories.keys()}

# Processing the query
def process(query):
  query_embed = embeddings_index[query]
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

    return maxkeyvalue,maxkey

def parsetokenizelist(tokenizelist, index):
    colors_count = 0
    for idx, token in enumerate(tokenizelist):
        token = token.lower()

        try:
            wordscore = process(token)
            entity = maxscore(wordscore)[0]
            entityvalue = maxscore(wordscore)[1]
            if entity == 'Colors' and colors_count == 0:
                df.at[index, 'color'] = token
                colors_count+=1
                start = idx
                end = idx+1
                df.at[index, 'color_start'] = start
                df.at[index, 'color_end'] = end

            elif entity == 'Colors' and colors_count==1:
                df.at[index, 'color2nd'] = token
                colors_count += 1
                start = idx
                end = idx + 1
                df.at[index, 'color2nd_start'] = start
                df.at[index, 'color2nd_end'] = end

            elif entity == 'Colors' and colors_count==2:
                df.at[index, 'color3rd'] = token
                colors_count += 1
                start = idx
                end = idx + 1
                df.at[index, 'color3rd_start'] = start
                df.at[index, 'color3rd_end'] = end

            elif entity == 'Colors' and colors_count == 3:
                df.at[index, 'color4th'] = token
                colors_count += 1
                start = idx
                end = idx + 1
                df.at[index, 'color4th_start'] = start
                df.at[index, 'color4th_end'] = end

            elif entity == 'Trajector':
                df.at[index, 'Trajector'] = token
                start = idx
                end = idx + 1
                df.at[index, 'Trajector_start'] = start
                df.at[index, 'Trajector_end'] = end

            else:
                continue
        except:
            print("Errror")



# Testing
print(process('on'))
print(process('place'))
print(process('two'))
print(process('prism'))



if __name__ == "__main__":
    path = "semeval-2014-task6/train_data/commands.txt"
    file = open(path)
    lines = file.readlines()
    count = 0
    mydict = {}
    mylist = []
    df = pd.DataFrame()
    for i in range(0, len(lines)):
      line = lines[i]
      line = line.strip()
      pattern = r'[0-9]'
      new_text = re.sub(pattern, '', line)
      new_text = new_text.strip()
      seperatewords = sepwords(new_text)
      df.at[i, 'sentence'] = new_text
      parsetokenizelist(seperatewords, i)
    print(df.head())

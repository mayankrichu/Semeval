# Semeval

Annotatig the sentences into Action, Trajector, Color, indicators, relations:

1. get the file location for the "semeval-2014-task6/train_data/commands.txt".
2. Replace the link in the program code in word2vec_spacy.py and indicator_identification.py
3. Replace the link for the output file with your requirement. word2vec_spacy.py, indicator_indification.py and dftojson.py consists of the location 
of the output file

Flow of the program

1. Run word2vec_spacy.py
2. indicator_identification.py
3. dftojson.py

Verification of the annotated data

Go to the AnnotationUI folder

1. Go to the variables.py and change the location of the respective variables based on your desired location.
2. semeval_file_path ---- The output file from the above steps
3. annotated_file_path --- The annotated seperate json file
4. True_annotated_file_path --- The folder for the correct annotated files
5. False_annotated_file_path --- The folder for the incorrect annotated files

Run the run.py file to start

The Error Detection uses the concept of Average Perceptron to correct the homophone confusion. The whole process is divided into two parts.

Part I: Preprocessing:
The first part, uses a POS tagged training data to learn the Perceptron and creates a Model file.
The POS Tagger created in Assignment2 is used for this purpose.
The format used to train the perceptron is:

CurrentWord Prev2:PreviousWord2 Prev1:PreviousWord1 Prev1Tag:POSTagOfPreviousWord1 Next1:NextWord1 Next2:NextWord2

Here, the CurrentWord can be any of {it's, its, you're, your, they're, their, loose, lose, to, too}
Using these features, the Average Perceptron is trained and the Model file is created which is used in the second part.

Command to run the 'preprocessing.py':
python3 preprocessing.py POSTaggedTrainingData ModelFile

Part II: Correct the Grammar:
The second part uses the model file created in Part I to make the grammatical corrections. For every occurance of a word from the list of 10 words,
we calculate the sum of weights of the previous 2 words, next 2 words and the POS tag of the previous word. The class with maximum weight is predicted to be the 
correct word.

Command to run 'correctgrammar.py':
python3 correctgrammar.py ModelFile < InputFile > OutputFile

The reasoning behind using previous words, next words and the POS tag of the previous word is that these features are useful in determining the context and 
grammar of the current word. Very often, the current word from our list is determined using the Part of Speech of the previous word.

Training Data Source:
Wikipedia dump. The original dump was 4GB+. I used 500MB of it.
This data was then POS Tagged using the Average Perceptron POS Tagger created in Assignment 2.

Third-Party Software used:
No third party software was used. The POS Tagger that is used here is the one that I created in Assignment 2.

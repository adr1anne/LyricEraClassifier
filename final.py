#
# 
#
# TextModel project!
# Lyric analysis
# Name: Adrianne Baik
#

from porter import create_stem
import math

class TextModel:
    def __init__(self):
        self.text = ""
        self.cleanedtext = ""
        self.words = {}
        self.wordlengths = {}
        self.stems = {}
        self.sentencelengths = {}
        self.firstperson = {}
        self.profanity = {}

    def __repr__(self):
        s = f'Words:\n{str(self.words)}\n\n'
        s += f'Word lengths:\n{str(self.wordlengths)}\n\n'
        s += f'Stems:\n{str(self.stems)}\n\n'
        s += f'Sentence lengths:\n{str(self.sentencelengths)}\n\n'
        s += f'First person pronouns:\n{str(self.firstperson)}\n\n'
        s += f'Profanity count:\n{str(self.profanity)}\n\n'
        s += '+'*55 + '\n'
        s += f'Text[:42]    {self.text[:42]}\n'
        s += f'Cleaned[:42] {self.cleanedtext[:42]}\n'
        s += '+'*55 + '\n\n'
        return s

    def addRawText(self, text):
        self.text += text 
        self.cleanedtext += self.cleanString(self.text) 

    def addFileText(self, filename):
        with open(filename, 'r', encoding='latin1') as f:
            text = f.read()
        self.addRawText(text)

    def makeSentenceLengths(self):
        """Creates the dictionary of sentence lengths
               should use self.text, because it needs the punctuation!
        """
        punctuation = '?.!'
        words = self.text.split()
        counter = 0
        # Loop through  words to count sentence lengths
        for word in words:
            counter += 1
            # Check if  word ends with punctuation 
            last_letter = word[-1]
            if last_letter in punctuation:
                # Update  count in self. dictionary
                if counter in self.sentencelengths:
                    self.sentencelengths[counter] += 1
                else:
                    self.sentencelengths[counter] = 1
                counter = 0  # Reset the word counter for the next sentence


    def cleanString(self, s):
        """Returns the string s, but
           with only ASCII characters, only lowercase, and no punctuation.
        """
        import string
         # Remove non-ASCII characters
        s = s.encode("ascii", "ignore")
        s = s.decode()

        # convert to lowercase
        s = s.lower()

        # remove punctuation
        for punctuation_mark in string.punctuation:
            s = s.replace(punctuation_mark, '')
        return s

    def makeWordLengths(self):
        """Creates the dictionary of word lengths
               should use self.cleanedtext, because it needs the punctuation!
        """
        words = self.cleanedtext.split()
        counter=0
        for word in words:
            counter+=1
            length = len(word)
            if length in self.wordlengths:
                self.wordlengths[length] += 1
            else:
                self.wordlengths[length] = 1

               
    def makeWords(self):
        """frequency dictionary of words
        """
        words = self.cleanedtext.split()
        wordfreq = {}

        for word in words:
            cleanword = self.cleanString(word)
            if cleanword in wordfreq:
                wordfreq[cleanword] +=1
            else:
                wordfreq[cleanword] =1 

        self.words = wordfreq


    def makeStems(self):
        """ frequency dictionary of word stems
        """
        words = self.cleanedtext.split()
        cleanword = [self.cleanString(word) for word in words]
        stemfreq = {}

        stems = [create_stem(word) for word in cleanword]
        for stem in stems:
            if stem in stemfreq:
                stemfreq[stem] += 1
            else:
                stemfreq[stem] = 1 
        self.stems = stemfreq

    def makeFirstPerson(self):
        """dictionary of how many first person pronouns are found
        """
        fp_pronouns = {'i', 'me', 'we','my', 'mine', 'us', 'ive', 'weve', 'im', 'ill', 'well', 'were'}
        words = self.cleanedtext.split()
        firstpersonfreq = {}
        
        for word in words:
            if word in fp_pronouns:
                if word in firstpersonfreq:
                    firstpersonfreq[word] += 1
                else:
                    firstpersonfreq[word] = 1
              
        self.firstperson = firstpersonfreq  

    def makeProfanity(self):
         """  dictionary of "profanity"
        """
         with open('profanity_wordlist.txt', 'r') as file:
             profanity = {word.strip().lower() for word in file}
  
         words = self.cleanedtext.split()
         profanityfreq={}

         for word in words:
               if word in profanity:
                   if word in profanityfreq:
                       profanityfreq[word]+=1
                   else:
                       profanityfreq[word]=1
                    
         self.profanity = profanityfreq

    def normalizeDictionary(self,d):
        """accept any single one of the model dictionaries d and return a 
        normalized version, i.e., one in which the values add up to 1.0. """
        total = 0
        for k in d:
            total+=d[k]

        nd = {}
        for k in d:
            nd[k] = d[k]/total
        return nd
           

    def smallestValue(self,nd1,nd2, nd3):
        """accept any 2 model dictionary and return the 
        smallest positive (non-zero) value across them both"""
        merge = nd1 | nd2 | nd3
        smallestvalue = min(merge.values())
        return smallestvalue
        	
    
    def compareDictionaries(self,d,nd1,nd2, nd3):
        """compute 1. log probability that the dictionary d arose from
        distribution of data in normalized deictionary nd1 and
        2. log probability that the dictionary d arose from distribution of 
        data in normalized dictionary nd2 
        also, should return both of thes eprobabilities"""
        
        nd1 = self.normalizeDictionary(nd1)
        nd2 = self.normalizeDictionary(nd2)
        nd3 = self.normalizeDictionary(nd3)

        # Find half the smallest value in nd1 and nd2
        epsilon = self.smallestValue(nd1, nd2,nd3)/2

        lp1 = 0.0
        lp2 = 0.0
        lp3 = 0.0
        
        for k, value in d.items():
            if k in nd1:
                lp1 += value * math.log(nd1[k])
            else:
                lp1 += value * math.log(epsilon)

        for k, value in d.items():
            if k in nd2:
                lp2 += value * math.log(nd2[k])
            else:
                lp2 += value * math.log(epsilon)
        for k, value in d.items():
            if k in nd3:
                lp3 += value * math.log(nd3[k])
            else:
                lp3 += value * math.log(epsilon)

        
        return lp1, lp2, lp3
 
    
    def createAllDictionaries(self):
         """Create out all five of self's
           dictionaries in full.
        """
         self.makeSentenceLengths()
         self.makeWords()
         self.makeStems()
         self.makeWordLengths()
         self.makeFirstPerson()
         self.makeProfanity()
    
    def compareTextWithTwoModels(self,model1,model2,model3):
        """run compareDictionaries for each of the feature dicts in self
        against corresponding normalized dict in model1 nand model2"""
        nd1 = self.normalizeDictionary(model1.words)
        nd2 = self.normalizeDictionary(model2.words)
        nd3 = self.normalizeDictionary(model3.words)
        LogProbs1 = self.compareDictionaries(self.words, nd1, nd2, nd3)
        print("LogProbs1 is", LogProbs1)
        LogProbsModel1 = LogProbs1[0]
        LogProbsModel2 = LogProbs1[1]
        LogProbsModel3 = LogProbs1[2]

        # Print comparative results
    
        if LogProbsModel1 > max(LogProbsModel2,LogProbsModel3):
            winner = "Golden and Post-Golden Age"
        elif LogProbsModel2 > max(LogProbsModel1, LogProbsModel3):
            winner = "Pre-Contemporary"
        elif LogProbsModel3 > max(LogProbsModel1,LogProbsModel2):
            winner = "Contemporary"
        else:
            winner = "It's a tie"

        print(" Results:")
        print(f"Golden and Post-Golden Age Log-Probabilities: {LogProbsModel1}")
        print(f"Pre-Contemporary Log-Probabilities: {LogProbsModel2}")
        print(f"Contemporary Log-Probabilities: {LogProbsModel3}")
        print(f"The era of music is {winner}")

TM = TextModel()
TM.addFileText("unknownsong2.txt")

# Create all of the dictionaries
TM.makeSentenceLengths()
TM.makeWordLengths()
TM.makeWords()
TM.makeStems()
TM.makeFirstPerson()
TM.makeProfanity()

# Let's see all of the dictionaries!
print("The text model has these dictionaries:")
print(TM)

print(" +++++++++++ Model1 +++++++++++ ")
TM1 = TextModel()
TM1.addFileText("golden.txt")
TM1.createAllDictionaries()  # provided in hw description
print(TM1)

print(" +++++++++++ Model1 +++++++++++ ")
TM2 = TextModel()
TM2.addFileText("precontemporary.txt")
TM2.createAllDictionaries()  # provided in hw description
print(TM2)

print(" +++++++++++ Model3 +++++++++++ ")
TM3 = TextModel()
TM3.addFileText("contemporary.txt")
TM3.createAllDictionaries()  # provided in hw description
print(TM3)

print(" +++++++++++ Unknown text +++++++++++ ")
TM_Unk = TextModel()
TM_Unk.addFileText("unknownsong2.txt")
TM_Unk.createAllDictionaries()  # provided in hw description
print(TM_Unk)


# The main comparison method
TM_Unk.compareTextWithTwoModels(TM1, TM2,TM3)
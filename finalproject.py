#
# finalproject.py (Final Project)
#
# Part I (Building an initial text model)
#

# Helper Function 1
import math

def clean_text(txt):
    """ Takes a string of text 'txt' as a parameter and returns a list containing the words in
    'txt' after it has been "cleaned". """
    symbols_to_begone = ['.',',','?','!',';',':','"']
    for symbol in symbols_to_begone:
        txt = txt.replace(symbol, '')
    txt = txt.lower()
    txt = txt.split(' ')
    return txt

# Helper Function 2

def stem(s):
    """ Accepts a string as a parameter, then returns the stem of s. """
    if len(s) > 3:
        
        # Check Suffixes
        
        if 'tion' in s or 'sion' in s:
            if 'tion' in s:
                s = s[0:len(s) -  4]
                s = s + 'te'
            elif 'sion' in s:
                s = s[0:len(s) - 4]
                s = s + 'de'
        elif 'ing' in s:
            s = s[0:len(s) - 3]
            if s[-1] == 'y':
                s = s[0:len(s) - 1]
                s = s + 'i'
                
            # Error Checking for Double Consonants
            
            elif s[-2] == s[-1]:
                s = s[0:len(s) - 1]
            
            else:
                s = s + 'e'
                s = stem(s)
        elif s[-1] == 'y':
            s = s[0:len(s) - 1]
            s = s + 'i'
        elif s[-2:] == 'es':
            s = s[0:len(s) - 2]
        elif s[-1] == 's' or s[-1] == 'e':
            if s[-1] == 's':
                s = s[0:len(s) - 1]
                s = stem(s)
            elif s[-1] == 'e':
                s = s[0:len(s) - 1]
        elif 'ness' in s or 'eous' in s or 'ious' in s or 'less' in s or 'ment' \
        in s or 'able' in s or 'ible' in s:
            s = s[0:len(s) - 4]
        elif 'ive'in s or 'ous' in s or 'ful' in s or 'est' in s or 'ial' in s:
            if 'ial' in s:
                s = s[0:len(s) - 3]
                s = s + 'y'
            elif 'ful' in s:
                if s[-3:] == 'ful':
                    s = s[0:len(s) - 3]
                else:
                    s = s
            elif 'est' in s:
                if s[-3:] == 'est':
                    s = s[0:len(s) - 3]
                    
                    # Error Checking For Double Consonants
                    
                    if s[-2] == s[-1]:
                        s = s[0:len(s) - 1]
                else:
                    s = s
            else:
                s = s[0:len(s) - 3]
        elif s[-2:] == 'er' or s[-2:] == 'ed':
            s = s[0:len(s) - 2]
            
            # Error Checking For Double Consonants
            
            if s[-2] == s[-1]:
                s = s[0:len(s) - 1]
        
        # Check Prefixes
        
        if 'inter' in s or 'super' in s or 'trans' in s or 'under' in s:
            s = s[5:]
        elif 'anti' in s or 'fore' in s or 'over' in s or 'semi' in s:
            s = s[4:]
        elif 'dis' in s or 'mid' in s or 'mis' in s or 'non' in s or 'pre' in s \
        or 'sub' in s:
            if s[0:3] in ('dis', 'mid', 'mis', 'non', 'pre', 'sub'):
                s = s[3:]
        elif 'de' in s or 'en' in s or 'em' in s or 'in' in s or 'im' in s or \
        'il' in s or 'ir' in s or 'un' in s:
            if s[0:2] in ('de', 'en', 'em', 'in', 'im', 'il', 'ir', 'un'):
                s = s[2:]
            else:
                s = s
    
    return s

# Helper Function 3

def compare_dictionaries(d1, d2):
    """ Takes two feature dictionaries as inputs, then computes and returns their
    log similarity score """
    score = 0
    total = sum(d1[item] for item in d1)
    for item in d2:
        if item in d1:
            score = score + d2[item]*math.log(d1[item]/total)
        elif item not in d1:
            score = score + d2[item]*math.log(0.5/total)
    
    return score

# TextModel Class

class TextModel:
    """ A data type for Text Model """
    
    # Constructor 
    
    def __init__(self, model_name):
        """ Constructs a new TextModel object by accepting a string 'model_name' as 
        a parameter and initializing the following three attributes: name, words, word_lengths. """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.sentence_punct_occur = {}
    
    # Method 1
    
    def __repr__(self):
        """ Returns a string that includes the name of the model as well as the sizes of the
        dictionaries for each feature of the text. """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of types of punctuation: ' + str(len(self.sentence_punct_occur)) + '\n'
        
        return s
    
    # Method 2
    
    def add_string(self, s):
        """ Analyzes the string txt and adds its pieces to all of the dictionaries in this
        text model. """
        word_count = 1
        for c in s:
            if c == ' ':
                word_count += 1
            elif c in '.!?':
                if word_count not in self.sentence_lengths:
                    self.sentence_lengths[word_count] = 1
                elif word_count in self.sentence_lengths:
                    self.sentence_lengths[word_count] += 1
                word_count = 0
        
        for c in s:
            if c in '.!?,;:-[]{}()"*' or c in "'":
                if c not in self.sentence_punct_occur:
                    self.sentence_punct_occur[c] = 1
                if c in self.sentence_punct_occur:
                    self.sentence_punct_occur[c] += 1
            
        
        word_list = clean_text(s)
        
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            elif w in self.words:
                self.words[w] += 1
        
        for w in word_list:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            elif len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
        
        for w in word_list:
            s_word = stem(w)
            if s_word not in self.stems:
                self.stems[s_word] = 1
            elif s_word in self.stems:
                self.stems[s_word] += 1
        
        
            
    
    # Method 3
    
    def add_file(self, filename):
        """ Adds all of the text in the file identified by 'filename' to the model.
        Does not explicitly return a value. """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        file_string = f.read()
        self.add_string(file_string)
    
    # Part II (Saving and retrieving a text model)
    
    # Method 1
    
    def save_model(self):
        """ Saves the TextModel object 'self' by writing its various feature dictionaries to files.
        There will be one file written for each feature dictionary. """
        filename = self.name + '_' + 'words'
        filename2 = self.name + '_' + 'word_lengths'
        filename3 = self.name + '_' + 'stems'
        filename4 = self.name + '_' + 'sentence_lengths'
        filename5 = self.name + '_' + 'sentence_punct_occur'
        d = self.words
        d2 = self.word_lengths
        d3 = self.stems
        d4 = self.sentence_lengths
        d5 = self.sentence_punct_occur
        f = open(filename, 'w')
        f.write(str(d))
        f.close()
        f = open(filename2, 'w')
        f.write(str(d2))
        f.close()
        f = open(filename3, 'w')
        f.write(str(d3))
        f.close()
        f = open(filename4, 'w')
        f.write(str(d4))
        f.close()
        f = open(filename5, 'w')
        f.write(str(d5))
        f.close()
        
    # Method 2
    
    def read_model(self):
        """ Reads the stored dictionaries for the called TextModel object from their files and
        assigns them to attributes of the called TextModel. """
        filename = self.name + '_' + 'words'
        filename2 = self.name + '_' + 'word_lengths'
        filename3 = self.name + '_' + 'stems'
        filename4 = self.name + '_' + 'sentence_lengths'
        filename5 = self.name + '_' + 'sentence_punct_occur'
        f = open(filename, 'r')
        words_str = f.read()
        f.close()
        f = open(filename2, 'r')
        word_lengths_str = f.read()
        f.close()
        f = open(filename3, 'r')
        word_stems_str = f.read()
        f.close()
        f = open(filename4, 'r')
        word_sentence_lengths_str = f.read()
        f.close()
        f = open(filename5, 'r')
        word_sentence_punct_occur_str = f.read()
        f.close()
        
        self.words = dict(eval(words_str))
        self.word_lengths = dict(eval(word_lengths_str))
        self.stems = dict(eval(word_stems_str))
        self.sentence_lengths = dict(eval(word_sentence_lengths_str))
        self.sentence_punct_occur = dict(eval(word_sentence_punct_occur_str))
    
    # Part IV
    
    # Method 1
    
    def similarity_scores(self, other):
        """ Computes and returns a list of log similarity scores measuring the similarity of self
        and other - one score for each type of feature (words, word lengths, stems, sentence lengths,
        and punctuation type occurrences) """
        word_score = compare_dictionaries(other.words, self.words)
        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        sentence_length_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        sentence_punctuation_score = compare_dictionaries(other.sentence_punct_occur, self.sentence_punct_occur)
        
        score_list = [word_score, word_length_score, stem_score, sentence_length_score, sentence_punctuation_score]
        return score_list
    
    # Method 2
    
    def classify(self, source1, source2):
        """ Compares the called TextModel object (self) to two other 'source' TextModel objects (source1 and source2)
        and determines which of these other TextModels is the more likely source of the called TextModel """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name + ': ' + str(scores1))
        print('scores for ' + source2.name + ': ' + str(scores2))
        counter = 0
        scores1_points = 0
        scores2_points = 0
        while counter != len(scores1):
            if scores1[counter] > scores2[counter]:
                scores1_points += 1
            elif scores2[counter] > scores1[counter]:
                scores2_points += 1
            counter += 1
        if scores1_points > scores2_points:
            print(self.name + ' is more likely to have come from '  + source1.name)
        elif scores2_points > scores1_points:
            print(self.name + ' is more likely to have come from ' + source2.name)

# Test Function 1

def test():
    """ Tests TextModel """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')
    
    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')
    
    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

# Main Test Function

def run_tests():
    """ Tests texts against source models to see which is the likely source """
    source1 = TextModel('rowling')
    source1.add_file('rowling_source_text_pt1.txt')
    source1.add_file('rowling_source_text_pt2.txt')
    
    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare_source_text_pt1.txt')
    source2.add_file('shakespeare_source_text_pt2.txt')
    
    new1 = TextModel('mystery1')
    new1.add_file('mystery_source_text_1.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('mystery2')
    new2.add_file('mystery_source_text_2.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('mystery3')
    new3.add_file('mystery_source_text_3.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('mystery4')
    new4.add_file('mystery_source_text_4.txt')
    new4.classify(source1, source2)
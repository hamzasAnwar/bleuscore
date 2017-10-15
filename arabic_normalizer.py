# coding: utf-8
# script for Arabic text normalization and tokenization  

import string
import collections 
import argparse
import codecs
import sys
import itertools
from nltk import word_tokenize

parser = argparse.ArgumentParser(description='Normalize and tokenize Arabic text.')
parser.add_argument('-corpus', type=str, help='Path to the Arabic Corpus', required=True)
parser.add_argument('-output', type=str, help='Path to the output file', required=True)

args = parser.parse_args()


# sample of Arabic script
sample = 'يُولَدُ جَمِيعُ ٱلنَّاسِ أَحْرَارًا مُتَسَاوِينَ فِي ٱلْكَرَامَةِ وَٱلْحُقُوقِ. وَقَدْ وُهِبُوا عَقْلًا وَضَمِيرًا وَعَلَيْهِمْ أَنْ يُعَامِلَ بَعْضُهُمْ بَعْضًا بِرُوحِ ٱلْإِخَاءِ'

# normalization table
norm_table = collections.defaultdict(lambda:None)

# main Arabic characters to keep
ABJAD = 'ي و ه ن م ل ك ق ف غ ع ظ ط ض ص ش س ز ر ذ د خ ح ج ث ت ب ا ء'.split()

# add main Arabic Arabic characters to keep
norm_table.update(dict(zip(map(ord, ABJAD), ABJAD)))


# add all ASCII chars to table, keep then as they are 
# i.e., English text should be kept untouched 
norm_table.update(dict(zip(map(ord, string.printable), string.printable)))


# transform Indic and Farsi digits to Arabic numerals 
AR_NUMS = '0 1 2 3 4 5 6 7 8 9'.split() 

# Farsi digits  ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
FA_NUMS = '۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹'.split() 

# Indic-Arabic digits ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
IN_NUMS = '٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩'.split() 


# update table with digits
norm_table.update(dict(zip(map(ord, IN_NUMS), AR_NUMS)))
norm_table.update(dict(zip(map(ord, FA_NUMS), AR_NUMS)))


# normalize Arabic spelling variations of Ya, Alef Maksura, Hamzas, and Ta marbuta 
YA    = ['ى', 'ي']
ALEF  = ['آ','ٱ' ,'أ', 'إ', 'ا']
TA    = ['ة', 'ه']
HAMZA = ['ؤ', 'ئ', 'ء']

# mao these chars ['ى', 'آ', 'أ', 'إ', 'ة', 'ؤ', 'ئ']
VARS = YA[:-1] + ALEF[:-1] + TA[:-1] + HAMZA[:-1] 

# to these chars ['ي', 'ا', 'ا', 'ا', 'ه', 'ء', 'ء']
REPS = YA[1:] + ALEF[4:]*4 + TA[1:] + HAMZA[2:]*2 

# update table
norm_table.update(dict(zip(map(ord, VARS), REPS)))


# transform Arabic punctuations into English so English tokenizers can be used
AR_PUNK = ['،', '؍', '؛', '؟', '٪', '٫', '٬', '…', '“', '”',  '‛',  '’', '_',  '`']
EN_PUNK = [',', '-', ';', '?', '%', '.', ',', '‥', '"', '"', '\'', '\'', '-', '\'']


# update table with punctuations
norm_table.update(dict(zip(map(ord, AR_PUNK), EN_PUNK)))

# add all possible Unicode whitespace to the table (just in case) 
norm_table.update({
    ord(' '): ' ',
    ord('\N{NO-BREAK SPACE}'): ' ',
    ord('\N{EN SPACE}'): ' ',
    ord('\N{EM SPACE}'): ' ',
    ord('\N{THREE-PER-EM SPACE}'): ' ',
    ord('\N{FOUR-PER-EM SPACE}'): ' ',
    ord('\N{SIX-PER-EM SPACE}'): ' ',
    ord('\N{FIGURE SPACE}'): ' ',
    ord('\N{PUNCTUATION SPACE}'): ' ',
    ord('\N{THIN SPACE}'): ' ',
    ord('\N{HAIR SPACE}'): ' ',
    ord('\N{ZERO WIDTH SPACE}'): ' ',
    ord('\N{NARROW NO-BREAK SPACE}'): ' ',
    ord('\N{MEDIUM MATHEMATICAL SPACE}'): ' ',
    ord('\N{IDEOGRAPHIC SPACE}'): ' ',
    ord('\N{IDEOGRAPHIC HALF FILL SPACE}'): ' ',
    ord('\N{ZERO WIDTH NO-BREAK SPACE}'): ' ',
    ord('\N{TAG SPACE}'): ' ',
    })

# >>> print(sample.translate(norm_table,))
# normalized 'يولد جميع الناس احرارا متساوين في الكرامه والحقوق. وقد وهبوا عقلا وضميرا وعليهم ان يعامل بعضهم بعضا بروح الاخاء'

# create list for tokenized text 
tokenized = []

# read corpus 
with codecs.open(args.corpus, 'r', encoding='utf-8') as f_i:
    #for line in f_i:
    text = f_i.read()
    normalized = text.translate(norm_table,)
        #tokens = word_tokenize(normalized)
        #tokenized.append(normalized)

# write to output file
with codecs.open(args.output, 'w', encoding='utf-8') as f_o:
    #for sent in tokenized:
    f_o.write(normalized)

# coding: utf-8
# script for Arabic text transliteration into Roman characters 
# supports 3 widely used transliteration schemes:
# (1) Buckwalter-base (original scheme), (2) Buckwalter-safe (XML-friendly),
# and (3) Habash-Soudi-Buckwalter (more readable and similar to IPA).

import string
import argparse
import codecs
import sys
from collections import defaultdict


parser = argparse.ArgumentParser(description='Transliterate Arabic text into Roman characters')
parser.add_argument('-input', type=str, help='Path to the Arabic text', required=True)
#parser.add_argument('-output', type=str, help='Path to the output file', required=True)
parser.add_argument('-scheme', help='Transliteration scheme',  
                    choices=['base', 'safe', 'hsb'], default = 'safe', nargs = '?')

args = parser.parse_args()

# initialize with mappings that are consistent across .. 
# all translitration schemes: Buckwalter (base and safe) and HSB 

transliteration_map = defaultdict(lambda:None)

transliteration_map.update({
    # letters 
    ord('ء'): "'", # hamza  
    ord('آ'): '|', # Alef Madda above
    ord('أ'): '>', # Alef hamza above 
    ord('ؤ'): '&', # Waw hamza above
    ord('إ'): '<', # Alef hamza below
    ord('ئ'): '}', # Yeh hamza above
    ord('ا'): 'A', # Alef
    ord('ب'): 'b', # Baa
    ord('ة'): 'p', # Teh Marbuta U+0629
    ord('ت'): 't', # Taa
    ord('ث'): 'v', # Theh U+062B
    ord('ج'): 'j', # Jeem
    ord('ح'): 'H', # Hah
    ord('خ'): 'x', # Khah
    ord('د'): 'd', #
    ord('ذ'): '*', # Thal U+0630
    ord('ر'): 'r', #
    ord('ز'): 'z', #
    ord('س'): 's', # 
    ord('ش'): '$', # 
    ord('ص'): 'S', #
    ord('ض'): 'D', #
    ord('ط'): 'T', #
    ord('ظ'): 'Z', #
    ord('ع'): 'E', # 
    ord('غ'): 'g', #
    ord('ف'): 'f', #
    ord('ق'): 'q', #
    ord('ك'): 'k', #
    ord('ل'): 'l', # 
    ord('م'): 'm', #
    ord('ن'): 'n', #
    ord('ه'): 'h', #
    ord('و'): 'w', #
    ord('ى'): 'Y', # Alef Maksura
    ord('ي'): 'y', #  
    
    # borrowed letters 
    ord('چ'): 'J', # Tcheh
    ord('پ'): 'P', # Peh
    ord('گ'): 'G', # 
    ord('ڤ'): 'V', #
    
    # diacritcs 
    ord('َ'): 'a',  #
    ord('ُ'): 'u',  #
    ord('ِ'): 'i',  #
    ord('ّ'): '~',  # shadda
    ord('ْ'): 'o',  # sukun
    ord('ً'): 'F',  # Fathatan
    ord('ٌ'): 'N',  # Dammatan 
    ord('ٍ'): 'K',  # Kasratan
    ord('ٱ'): '{', # Alef wasla
    ord('ٰ'): '`',  # dagger alef

    # punctuation and math
    ord('ـ'): '_',      #
    ord('،'): ',',      #
    ord(u"\u00AD"): '-',# soft hyphen, invisble in Arabic script! U+00AD
    ord('؛'): ';',      # Arabic semi-colon U+061B
    ord('؟'): '?',      # U+061F
    ord('؍'): '-',      # Arabic date separator U+060D
    ord('٪'): '%',      # Arabic percent sign U+066A
    ord('٫'): '.',      # Arabic decimal separator (U+066B)
    ord('٬'): ',',      # Arabic thousands separator U+066C
    ord('…'): '‥',      # horizontal ellipsis U+2026
    
    # Indic-Arabic digits  
    ord('١'): '1', #
    ord('٢'): '2', #
    ord('٣'): '3', #
    ord('٤'): '4', #
    ord('٥'): '5', #  
    ord('٦'): '6', #
    ord('٧'): '7', #
    ord('٨'): '8', #
    ord('٩'): '9', #
    ord('٠'): '0', #  
    
    # Persian-style digits
    ord('۱'): '1', #
    ord('۲'): '2', #
    ord('۳'): '3', #
    ord('۴'): '4', #
    ord('۵'): '5', #  
    ord('۶'): '6', #
    ord('۷'): '7', #
    ord('۸'): '8', #
    ord('۹'): '9', #
    ord('۰'): '0', #  
})

# add all ASCII chars to table, keep them as they are 
# i.e., English text should be kept untouched 
transliteration_map.update(dict(zip(map(ord, string.printable), string.printable)))

# mappings that are unique in Buckwalter safe 
# NOTE: this scheme is good for XML and web services, but not human-readable  
if args.scheme == 'safe':
    transliteration_map.update({
        # letters 
        ord('ء'): 'C', # hamza  
        ord('آ'): 'M', # Alef Madda above
        ord('أ'): 'O', # Alef hamza above 
        ord('ؤ'): 'W', # Waw hamza above
        ord('إ'): 'I', # Alef hamza below
        ord('ئ'): 'Q', # Yeh hamza above
        ord('ذ'): 'V', # Thal U+0630
        ord('ش'): 'c', #
        
        # diacritcs 
        ord('ً'): 'F',  # Fathatan
        ord('ٌ'): 'N',  # Dammatan 
        ord('ٍ'): 'K',  # Kasratanٌ
        ord('ْ'): 'o',  # sukun
        ord('َ'): 'a',  #
        ord('ُ'): 'u',  #
        ord('ِ'): 'i',  #
        ord('ْ'): 'o',  # sukun
        ord('ٱ'): 'L', # Alef wasla
        ord('ٰ'): 'e',  # dagger alef 
        
        # borrowed letter
        ord('ڤ'): 'B'    
    })

# make modifications nesseccary for Habash-Soudi-Buckwalter
# NOTE: this scheme is human-readable, but not good for XML and web services  
elif args.scheme == 'hsb':
    transliteration_map.update({
        # letters 
        ord('آ'): 'Ā', # Alef Madda above
        ord('أ'): 'Â', # Alef hamza above 
        ord('ؤ'): 'ŵ', # Waw hamza above
        ord('إ'): 'Ǎ', # Alef hamza below
        ord('ئ'): 'ŷ', # Yeh hamza above
        ord('ة'): 'ħ', # Teh Marbuta U+0629
        ord('ث'): 'θ', # Theh U+062B
        ord('ذ'): 'ð', # Thal U+0630
        ord('ش'): 'š', #
        ord('ع'): 'ς', # 
        ord('غ'): 'γ', #
        ord('ظ'): 'Ď', #
        ord('ى'): 'ý', # Alef Maksura
        
        # dicritcs        
        ord('َ'): 'a',  #
        ord('ُ'): 'u',  #
        ord('ِ'): 'i',  #
        ord('ْ'): '.',  # sukun
        ord('ً'): 'ã',  # Fathatan
        ord('ٌ'): 'ũ',  # Dammatan 
        ord('ٍ'): 'ĩ',  # Kasratan
        ord('ٱ'): 'Ä', # Alef wasla
        ord('ٰ'): 'ā',  # dagger alef 
        
        # borrowed letters 
        ord('چ'): 'c', # Tcheh
        ord('پ'): 'p', # Peh
        ord('گ'): 'g', # 
        ord('ڤ'): 'v'  #
    })  



# read Arabic
with codecs.open(args.input, 'r', encoding='utf-8') as f:
    arabic_text = f.read()

# write transliterated
#with codecs.open(args.output, 'w', encoding='utf-8') as f:    
romanized_text = arabic_text.translate(transliteration_map,)
sys.stdout.write(romanized_text)       

import ntpath
import sys
import codecs
import os
import math
import operator
import functools


def fetch_data(cand, ref):
    references = []
    if '.eng' in ref:
        reference_file = codecs.open(ref, 'r', 'utf-8')
        references.append(reference_file.readlines())
    else:
        for root, dirs, files in os.walk(ref):
            for f in files:
                reference_file = codecs.open(os.path.join(root, f), 'r', 'utf-8')
                references.append(reference_file.readlines())
    candidate_file = codecs.open(cand, 'r', 'utf-8')
    candidate = candidate_file.readlines()
    return candidate, references


def count_ngram(candidate, references, n):
    clipped_count = 0
    count = 0
    r = 0
    c = 0
    for si in range(len(candidate)):
        # Calculate precision for each sentence
        ref_counts = []
        ref_lengths = []
        # Build dictionary of ngram counts
        for reference in references:
            ref_sentence = reference[si]
            ngram_d = {}
            words = ref_sentence.strip().split()
            ref_lengths.append(len(words))
            limits = len(words) - n + 1
            # loop through the sentance consider the ngram length
            for i in range(limits):
                ngram = ' '.join(words[i:i+n]).lower()
                if ngram in ngram_d.keys():
                    ngram_d[ngram] += 1
                else:
                    ngram_d[ngram] = 1
            ref_counts.append(ngram_d)
        # candidate
        cand_sentence = candidate[si]
        cand_dict = {}
        words = cand_sentence.strip().split()
        limits = len(words) - n + 1
        for i in range(0, limits):
            ngram = ' '.join(words[i:i + n]).lower()
            if ngram in cand_dict:
                cand_dict[ngram] += 1
            else:
                cand_dict[ngram] = 1
        clipped_count += clip_count(cand_dict, ref_counts)
        count += limits
        r += best_length_match(ref_lengths, len(words))
        c += len(words)
    if clipped_count == 0:
        pr = 0
    else:
        pr = float(clipped_count) / count
    bp = brevity_penalty(c, r)
    return pr, bp


def clip_count(cand_d, ref_ds):
    """Count the clip count for each ngram considering all references"""
    count = 0
    for m in cand_d.keys():
        m_w = cand_d[m]
        m_max = 0
        for ref in ref_ds:
            if m in ref:
                m_max = max(m_max, ref[m])
        m_w = min(m_w, m_max)
        count += m_w
    return count


def best_length_match(ref_l, cand_l):
    """Find the closest length of reference to that of candidate"""
    least_diff = abs(cand_l-ref_l[0])
    best = ref_l[0]
    for ref in ref_l:
        if abs(cand_l-ref) < least_diff:
            least_diff = abs(cand_l-ref)
            best = ref
    return best


def brevity_penalty(c, r):
    if c > r:
        bp = 1
    else:
        bp = math.exp(1-(float(r)/c))
    return bp


def geometric_mean(precisions):
    return (functools.reduce(operator.mul, precisions)) ** (1.0 / len(precisions))


def BLEU(candidate, references):
    precisions = []
    for i in range(4):
        pr, bp = count_ngram(candidate, references, i+1)
        precisions.append(pr)
    bleu = geometric_mean(precisions) * bp
    return bleu

def normalizer(referencesDir):
    for root, dirs, files in os.walk(referencesDir):
        for f in files:
            reference_file = codecs.open(os.path.join(root, f), 'r', 'utf-8')
            filename=ntpath.basename(reference_file.name)
            #python arabic_normalizer.py -corpus outputtest.eng -outputoutputtest.txt
            normalizerCommand='arabic_normalizer.py -corpus '+os.path.join(referencesDir,filename)+' -output '+os.path.join(os.path.split(referencesDir)[0],'normalized',filename)
            print(normalizerCommand)
            os.system(normalizerCommand)

def tokenizerReplace(referencesDir):
    for root, dirs, files in os.walk(referencesDir):
        for f in files:
            reference_file = codecs.open(os.path.join(root, f), 'r', 'utf-8')
            filename=ntpath.basename(reference_file.name)
            #python arabic_normalizer.py -corpus outputtest.eng -outputoutputtest.txt
            tokenizerCommand='perl '+os.path.join('tokenizer','replace-unicode-punctuation.perl')+' < '+os.path.join(referencesDir,filename)+' > '+os.path.join(os.path.split(referencesDir)[0],'punctuated',filename)
            print(tokenizerCommand)
            os.system(tokenizerCommand)

def normalizePunctuation(referencesDir):
    for root, dirs, files in os.walk(referencesDir):
        for f in files:
            reference_file = codecs.open(os.path.join(root, f), 'r', 'utf-8')
            filename=ntpath.basename(reference_file.name)
            #python arabic_normalizer.py -corpus outputtest.eng -outputoutputtest.txt
            tokenizerCommand='perl '+os.path.join('tokenizer','normalize-punctuation.perl')+' < '+os.path.join(referencesDir,filename)+' > '+os.path.join(os.path.split(referencesDir)[0],'normalized_punctuated',filename)
            print(tokenizerCommand)
            os.system(tokenizerCommand)

def removeNonPrint(referencesDir):
    for root, dirs, files in os.walk(referencesDir):
        for f in files:
            reference_file = codecs.open(os.path.join(root, f), 'r', 'utf-8')
            filename=ntpath.basename(reference_file.name)
            #python arabic_normalizer.py -corpus outputtest.eng -outputoutputtest.txt
            nonPrintCommand='perl '+os.path.join('tokenizer','remove-non-printing-char.perl')+' < '+os.path.join(referencesDir,filename)+' > '+os.path.join(os.path.split(referencesDir)[0],'non_print',filename)
            print(nonPrintCommand)
            os.system(nonPrintCommand)

def tokenization(referencesDir):
    for root, dirs, files in os.walk(referencesDir):
        for f in files:
            reference_file = codecs.open(os.path.join(root, f), 'r', 'utf-8')
            filename=ntpath.basename(reference_file.name)
            #python arabic_normalizer.py -corpus outputtest.eng -outputoutputtest.txt
            nonPrintCommand='perl '+os.path.join('tokenizer','tokenizer.perl -l en -no-escape -threads 4')+' < '+os.path.join(referencesDir,filename)+' > '+os.path.join(os.path.split(referencesDir)[0],'tokenized',filename)
            print(nonPrintCommand)
            os.system(nonPrintCommand)

def transliterate(referencesDir):
    for root, dirs, files in os.walk(referencesDir):
        for f in files:
            reference_file = codecs.open(os.path.join(root, f), 'r', 'utf-8')
            filename=ntpath.basename(reference_file.name)
            #python arabic_normalizer.py -corpus outputtest.eng -outputoutputtest.txt
            nonPrintCommand='transliterate.py -scheme hsb -input '+os.path.join(referencesDir,filename)+' > '+os.path.join(os.path.split(referencesDir)[0],'output',filename)
            print(nonPrintCommand)
            os.system(nonPrintCommand)



def preprocess_references(referencesDir):
    #rest temp folders
    removeFiles(os.path.join(referencesDir,'normalized'))
    removeFiles(os.path.join(referencesDir,'punctuated'))
    removeFiles(os.path.join(referencesDir,'normalized_punctuated'))
    removeFiles(os.path.join(referencesDir,'non_print'))
    removeFiles(os.path.join(referencesDir,'tokenized'))
    removeFiles(os.path.join(referencesDir,'output'))

    normalizer(os.path.join(referencesDir,'raw'))
    tokenizerReplace(os.path.join(referencesDir,'normalized'))
    normalizePunctuation(os.path.join(referencesDir,'punctuated'))
    removeNonPrint(os.path.join(referencesDir, 'normalized_punctuated'))
    tokenization(os.path.join(referencesDir, 'non_print'))
    transliterate(os.path.join(referencesDir, 'tokenized'))


def removeFiles(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    preprocess_references(sys.argv[2])
    candidate, references = fetch_data(sys.argv[1], os.path.join(sys.argv[2],'output'))
    bleu = BLEU(candidate, references)
    print (bleu)

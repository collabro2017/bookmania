from sys import argv
import pickle
import re
from itertools import islice
from nltk.tag.stanford import StanfordPOSTagger
import os
from tqdm import tqdm


class Va3ToPos:

    def __init__(self, translation_id):
        # Specify paths to Stanford taggers
        STANFORD_POS_TAGGER_LOCATION = os.environ['STANFORD_POS']
        english_modelfile = '{}/models/english-bidirectional-distsim.tagger'.format(STANFORD_POS_TAGGER_LOCATION)
        spanish_modelfile = '{}/models/spanish-distsim.tagger'.format(STANFORD_POS_TAGGER_LOCATION)
        jarfile = '{}/stanford-postagger-3.7.0.jar'.format(STANFORD_POS_TAGGER_LOCATION)

        # Set Translation ID
        self.translation_id = translation_id

        # Initialize taggers
        self.en_tagger = StanfordPOSTagger(model_filename=english_modelfile, path_to_jar=jarfile)
        self.es_tagger = StanfordPOSTagger(model_filename=spanish_modelfile, path_to_jar=jarfile)

        # Store the string literals from the VA3 files
        self.va3l1 = []
        self.va3l2 = []

        # Store tokenized plaintext sentences
        self.l1_tok_sent = []
        self.l2_tok_sent = []

        # Store the alignments as lists of lists of ints
        self.l1_alignments = []
        self.l2_alignments = []

        # Stor the POS tags as lists of strings
        self.l1_pos_tags = []
        self.l2_pos_tags = []

    def read_va3(self, l1filename, l2filename):

        # VA3 file is structured in lines of 3, the 3rd line being the allignment
        with open(l1filename) as f:
            while True:
                next_3 = list(islice(f, 3))
                if not next_3:
                    break
                self.va3l1.append(next_3[2].strip())

        with open(l2filename) as f:
            while True:
                next_3 = list(islice(f, 3))
                if not next_3:
                    break
                self.va3l2.append(next_3[2].strip())

    def read_alignments(self):

        # Extracts the list of alignments from plaintext. Stores them as list of ints.
        for sent in self.va3l1:
            align_toks = re.findall(r'(.*?) \(\{([\d ]+)\}\)', sent)
            self.l1_tok_sent.append([elem[0].strip() for elem in align_toks])
            self.l1_alignments.append(([elem[1].split() for elem in align_toks]))

        for sent in self.va3l2:
            align_toks = re.findall(r'(.*?) \(\{([\d ]+)\}\)', sent)
            self.l2_tok_sent.append([elem[0].strip() for elem in align_toks])
            self.l2_alignments.append(([elem[1].split() for elem in align_toks]))

    def pos_tag(self):
        print("====================================")
        print("Part of Speech Tagging ")
        print("====================================")
        total_lines = len(self.l1_tok_sent)
        for i in range(total_lines):

            print(str(i + 1) + " / " + str(total_lines))

            l1_sent = self.l1_tok_sent[i]
            self.l1_pos_tags.append([elem[1] for elem in self.en_tagger.tag(l1_sent)])

            l2_sent = self.l2_tok_sent[i]
            self.l2_pos_tags.append([elem[1] for elem in self.es_tagger.tag(l2_sent)])

    def combine_pos_alignments(self):
        result = []
        for i in range(len(self.l1_pos_tags)):
            en = ([(self.l1_tok_sent[i][j], self.l1_alignments[i][j], self.l1_pos_tags[i][j]) for j in range(len(self.l1_tok_sent[i]))])
            es = ([(self.l2_tok_sent[i][j], self.l2_alignments[i][j], self.l2_pos_tags[i][j]) for j in range(len(self.l2_tok_sent[i]))])
            result.append([en, es])

        # For the purposes of demonstration, print to console
        for n in range(len(result)):
            print(result[n][0])
            print(result[n][1])
            print("\n")

        filename = "/tmp/translations_blends_{}.p".format(self.translation_id)
        pickle.dump(result, open(filename, "wb"))

translation_id = argv[1]
l1_file = argv[2]
l2_file = argv[3]

pos_tagger = Va3ToPos(translation_id=translation_id)
pos_tagger.read_va3(l1_file, l2_file)
pos_tagger.read_alignments()
pos_tagger.pos_tag()
pos_tagger.combine_pos_alignments()



















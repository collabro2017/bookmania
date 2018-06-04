import pickle
import re
from sys import argv
import time
import random
from collections import OrderedDict


class ChunkBlender:

    def __init__(self, inputname, outputpath):
        self.sents = pickle.load(open(inputname, 'rb'))
        self.outpath = outputpath
        self.output_blends = []


    """
    Helper function to determine whether chunks are aligned with each other.
    """
    def is_overlap(self, source, target):
        overlap = False

        # For each word in the source chunk
        for src_word in source:
            src_lang = (src_word[2][:2] == "l1")
            src_index = str(src_word[2][2:])

            # For each word in teh target chunk
            for tgt_word in target:
                tgt_lang = (tgt_word[2][:2] == "l1")
                tgt_index = str(tgt_word[2][2:])

                # If the source points to the target
                for algn in src_word[1]:
                    if (str(algn) == tgt_index) & (tgt_lang != src_lang):
                        overlap = True

                # If the target points to the source
                for algn in tgt_word[1]:
                    if (str(algn) == src_index) & (tgt_lang != src_lang):
                        overlap = True

        return overlap

    """
    Recursive function to coagulate allignment chunks.
    """
    def reduce_chunks(self, chunks):
        # Base case is when start len is the same as the end length
        start_len = len(chunks)
        result = []

        for i in range(len(chunks)):
            appended = False
            curr = chunks[i]
            for chunk in result:
                if self.is_overlap(curr, chunk):
                    for c in curr:
                        chunk.append(c)
                    appended = True
            if appended == False:
                result.append(curr)

        # If we haven't added any new chunks, then return. Otherwise, recurse.
        if (start_len == len(result)):
            return result
        else:
            return self.reduce_chunks(result)

    """
    Wrapper function to produce a set of chunks for a given sentence
    """
    def chunk_sent(self, sent):
        l1_sent = sent[0]
        l2_sent = sent[1]

        # Seed the chunk array with all the individual words.
        chunks = [[w] for w in l1_sent] + [[w] for w in l2_sent]

        # Reverse sort so we always seed the reducing algorithm with the largest chunk
        chunked_sent = self.reduce_chunks(sorted(chunks, key=len, reverse=True))

        # Delete the duplicates while preserving order
        result = []
        for chk in chunked_sent:
            result.append([ii for n,ii in enumerate(chk) if ii not in chk[:n]])

        return result

    """
    Helper funcion: Given word and a chunk list, determines quintile of blend level
    """
    def get_blend_lvl(self, chunks, search_word):
        for i in range(len(chunks)):
            for word in chunks[i]:
                if word == search_word:
                    return(int(float(i)/float(len(chunks)) * 5 + 1))
        return 1

    """
    Turns a sentence and a list of chunks into a series of blends, one per chunk
    """
    def pos_chunkify(self, l1_sent, l2_sent, chunks):

        #Start by translating the smallest chunk, go to the largest
        chunks = sorted(chunks, key=len)

        # Associate each chunk with a blend-level

        result = ""
        for word in l1_sent[1:]:

            word_blend = "[" + word[0] + '|'
            blnd_lvl = self.get_blend_lvl(chunks, word)

            # All the words it aligns with
            for algn in word[1]:
                if (int(algn) < len(l2_sent)):
                    word_blend += l2_sent[int(algn)][0] + " "

            #And last, the blend-level
            word_blend += "|" + str(blnd_lvl) + "]"

            #Replace hanging spaces
            result += word_blend.replace(' |', '|')

        self.output_blends.append(result)

    """
    Wrapper function for chunking and blending
    """
    def chunk_blend(self):

        for sent in self.sents:
            l1_sent = sent[0]
            l2_sent = sent[1]

            # Add unique indicators for each of the words
            l1_uniq = [(l1_sent[i][0], l1_sent[i][1], "l1"+str(i)) for i in range(len(l1_sent))]
            l2_uniq = [(l2_sent[i][0], l2_sent[i][1], "l2"+str(i)) for i in range(len(l2_sent))]


            # Create a set of chunks from a sentences.
            chunks = self.chunk_sent([l1_uniq, l2_uniq])

            # Turn those chunks into blends
            self.pos_chunkify(l1_uniq, l2_uniq, chunks)

        pickle.dump(self.output_blends, open(self.outpath, "wb"))

myBlender = ChunkBlender(argv[1], argv[2])
myBlender.chunk_blend()

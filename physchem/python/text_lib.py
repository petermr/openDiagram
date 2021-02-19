
import numpy as np
import matplotlib.pyplot as plt
import nltk, unicodedata
import os
import re
import glob
from file_lib import AmiPath, Globber
from collections import namedtuple
from bs4 import BeautifulSoup
from collections import Counter

import xml.etree.ElementTree as ET
import re


NFKD = "NFKD"

"""tags
b i em strong 
table 
fig 

"""
TAGS = {
    "\n": "",
    "</sup>": "",
    "</sub>": "",
    "</xref>": "",
}

TAG_REGEXES = {
    " +<": "<",
    "<xref[^>]*>": "@",
    " *<sup>": "^",
    " *<sub>": "_",
}

PUNCT = "!@#$%^&*+{}[]:;'|<>,.?/~`\"\\"

LIION_PROJ = os.path.abspath(os.path.normpath(os.path.join("../liion")))
PY_DIAG = "../../python/diagrams"

CCT_PROJ = os.path.abspath(os.path.normpath(os.path.join(PY_DIAG, "satish/cct")))

STOPWORDS_EN = nltk.corpus.stopwords.words("english")
STOPWORDS_PUB = {
'figure','permission','reproduced','copyright', 'authors', 'society',"university",'table',
    "manuscript", "published", "declare", "conflict", "research", "diagram", "images", "version"
}
OIL186 = "/Users/pm286/projects/CEVOpen/searches/oil186" # pmr only

class ProjectCorpus():

    def __init__(self, cwd, tree_glob="./*/"):
        self.cwd = cwd
        self.tree_glob = tree_glob
        self.words = []

    def read_analyze_child_documents(self):
#        self.files = self.glob_corpus_files()
        self.files = glob.glob(os.path.join(self.cwd, self.tree_glob))
        print("glob", self.cwd, self.tree_glob, str(len(self.files)), self.files)
        for file in self.files:
            document = Document(file) #level of tree
            document.create_analyze_sections()
            words = [w for w in document.words if len(w) > 2]
            words = [w for w in words if w.lower() not in STOPWORDS_EN ]
            words = [w for w in words if w.lower() not in STOPWORDS_PUB]
            words = [w for w in words if not w.isnumeric()]

            self.words.extend(words)
        c = Counter(self.words)
        print("Common", c.most_common(50))

    def glob_corpus_files(self, glob_path, recurse=True):
        ami_path = AmiPath();
        ami_path.recurse = recurse
        files = ami_path.get_globbed_files()
        return files

    @staticmethod
    def test(project):
        print("start test", project)
        assert (os.path.exists(project))
        project = ProjectCorpus(project)
        project.read_analyze_child_documents()
        print("end test")

    @staticmethod
    def test_oil():
        print("start test", OIL186)
        assert (os.path.exists(OIL186))
        project = ProjectCorpus(OIL186)
        project.read_analyze_child_documents()
        print("end test")

    def __str__(self):
        return " ".join(map(str, self.sentences))

class Document():
    """ a standalone hierarchical document
    level of Tree or below
    may contain a subset of the conventional document"""

    def __init__(self, file="f"):
        self.sections = None
        self.file = file
        self.words = []

    def create_analyze_sections(self):
        sections_file = os.path.abspath(os.path.join(self.file, "sections"))
        if not os.path.exists(sections_file):
            print("PLEASE CREATE sections with ami sections, will add pyami later")
            return
        terminal_files = glob.glob(os.path.join(sections_file, "**/*.xml"))
        for terminal_file in terminal_files:
            terminal_page = TerminalPage(terminal_file)
            terminal_page.analyze_file_contents()
            self.words.extend(terminal_page.get_words())



class TerminalPage():
    """the xml sub-document with text
    Currently either <title> or <p>

    Will often get annotated with sentence markers
    """
    def __init__(self, file):
        self.file = file
        self.words = []


    def analyze_file_contents(self):
        """read a file as an ami-section of larger document """
        with open(self.file, "r") as f:
            self.text = f.read()
        # assumes this has been chunked to sections
#        print("t", len(self.text), self.text[:50])
        self.read_para()

    def read_para(self):
        self.text = self.flatten_text(self.text)
        self.sentences = [Sentence(s) for s in (nltk.sent_tokenize(self.text))]
#        self.sentences = Sentence.merge_false_sentence_breaks(self.sentences)
        Sentence.write_sentence_file(self.file[:-4] + ".txt", self.sentences)

    @staticmethod
    def flatten_text(text):
        """removes xml tags , diacritics, """
        text = TextUtil.strip_xml_tags(text)
        text = TextUtil.remove_para_tags(text)
        text = unicodedata.normalize(NFKD, text)
        text = TextUtil.flatten_non_ascii(text)
        return text

    @staticmethod
    def remove_stopwords(words, stopwords=nltk.corpus.stopwords.words("english")):
        return [word for word in words if word.lower() not in stopwords]

    
    def get_words(self):
        for sentence in self.sentences:
            self.words.extend(sentence.words)
        return self.words

class Sentence():

    def __init__(self, string):
        self.string = string
        self.words = nltk.word_tokenize(string)
        self.words = Sentence.remove_punct(self.words)

    @staticmethod
    def merge_false_sentence_breaks(sentences):
        # this was for rogue periods, etc.
        sent0 = []
        for i, sent in enumerate(sentences):
            pass

    @staticmethod
    def remove_punct(tokens):
        """removes tokens consisting of punctuation in present `PUNCT`

        tokens: list of words
        returns: words diminished by deleted punctuation

        """
        tokens = [token for token in tokens if not token in PUNCT]
        return tokens

    @staticmethod
    def write_sentence_file(file, sentences):
        """writes numbered sentences"""
        with open(file, "w") as f:
            for i, sentence in enumerate(sentences):
                f.write(str(i) + ": " + sentence.string + "\n")


    def __str__(self):
        return " ".join(map(str, self.words))

class TextUtil():

    @staticmethod
    def strip_xml_tags(text):
        soup = BeautifulSoup(text, "xml")
        stripped_text = soup.get_text()
        return stripped_text

    @staticmethod
    def clean_line_ends(text):
        return re.sub[r'[\r|\n|\r\n]+', '\n', text]

    @staticmethod
    def join_xml_texts(xml_string):
        """remove all tags in XML

        replace all tags by spaces. We may later wish to exclude some names tags (e.g. <sup>)
        xml_string: XML in serialized form
        return flattened string with spaces replacing tags
        """
        #remove tags
        untagged_text = str.join(" ", list(ET.fromstring(xml_string).itertext()))
        return untagged_text

    @staticmethod
    def remove_para_tags(text):
        """remove certain tags within paras lexically.
        Works on flat text

        Messy. At present tags are in TAGS and TAG_REGEXES
        """
        for key in TAGS:
            text = text.replace(key, TAGS[key])
        for regex in TAG_REGEXES:
            text = re.sub(regex, TAG_REGEXES[regex], text)
        return text

    @staticmethod
    def flatten_non_ascii(text):
        """remove diacritics and other 'non-ascii' characters

        Messy.

        """
        text = text.encode("ascii", "ignore").decode("utf-8", "ignore")
        return text

    @staticmethod
    def remove_non_alphanumeric(text, remove_digits=False):
        """
        Remove nonalphanumeric characters

        remove_digits: remove digits 0-9
        """
        pattern = r'[^A-Za-z0-9\s]' if not remove_digits else r'[A-Za-z\s]'
        text = re.sub(pattern, '', text)
        return text


def main():
    print("started text_lib")
    ProjectCorpus.test(CCT_PROJ)
#    ProjectCorpus.test(LIION_PROJ)
#    ProjectCorpus.test_oil()
    print("finished text_lib")

if __name__ == "__main__":
    main()
else:
#    main()
    pass

"""Print most frequent N-grams in given file.
Usage: python ngrams.py filename
Problem description: Build a tool which receives a corpus of text,
analyses it and reports the top 10 most frequent bigrams, trigrams,
four-grams (i.e. most frequently occurring two, three and four word
consecutive combinations).
NOTES
=====
I'm using collections.Counter indexed by n-gram tuple to count the
frequencies of n-grams, but I could almost as easily have used a
plain old dict (hash table). In that case I'd use the idiom
"dct.get(key, 0) + 1" to increment the count, and heapq.nlargest(10)
or sorted() on the frequency descending instead of the
counter.most_common() call.
In terms of performance, it's O(N * M) where N is the number of words
in the text, and M is the number of lengths of n-grams you're
counting. In this case we're counting digrams, trigrams, and
four-grams, so M is 3 and the running time is O(N * 3) = O(N), in
other words, linear time. There are various micro-optimizations to be
had, but as you have to read all the words in the text, you can't
get much better than O(N) for this problem.
On my laptop, it runs on the text of the King James Bible (4.5MB,
824k words) in about 3.9 seconds. Full text here:
https://www.gutenberg.org/ebooks/10.txt.utf-8
I haven't done the "extra" challenge to aggregate similar bigrams.
However, what I would do to start with is, after calling
count_ngrams(), use difflib.SequenceMatcher to determine the
similarity ratio between the various n-grams in an N^2 fashion. This
would be quite slow, but a reasonable start for smaller texts.
This code took me about an hour to write and test. It works on Python
2.7 as well as Python 3.x.
"""

import collections
import re
import sys
import time


def tokenize(string):
    """Convert string to lowercase and split into words (ignoring
    punctuation), returning list of words.
    """
    return re.findall(r'\w+', string.lower())


def count_ngrams(lines, min_length=2, max_length=4):
    """Iterate through given lines iterator (file object or list of
    lines) and return n-gram frequencies. The return value is a dict
    mapping the length of the n-gram to a collections.Counter
    object of n-gram tuple and number of times that n-gram occurred.
    Returned dict includes n-grams of length min_length to max_length.
    """
    lengths = range(min_length, max_length + 1)
    ngrams = {length: collections.Counter() for length in lengths}
    queue = collections.deque(maxlen=max_length)

    # Helper function to add n-grams at start of current queue to dict
    def add_queue():
        current = tuple(queue)
        for length in lengths:
            if len(current) >= length:
                ngrams[length][current[:length]] += 1

    # Loop through all lines and words and add n-grams to dict
    for line in lines:
        for word in tokenize(line):
            queue.append(word)
            if len(queue) >= max_length:
                add_queue()

    # Make sure we get the n-grams at the tail end of the queue
    while len(queue) > min_length:
        queue.popleft()
        add_queue()

    return ngrams


def print_most_frequent(ngrams, num=10):
    """Print num most common n-grams of each length in n-grams dict."""
    for n in sorted(ngrams):
        print('----- {} most common {}-grams -----'.format(num, n))
        for gram, count in ngrams[n].most_common(num):
            print('{0}: {1}'.format(' '.join(gram), count))
        print('')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python ngrams.py filename')
        sys.exit(1)

    start_time = time.time()
    with open(sys.argv[1]) as f:
        ngrams = count_ngrams(f)
    print_most_frequent(ngrams)
    elapsed_time = time.time() - start_time
    print('Took {:.03f} seconds'.format(elapsed_time))

import nltk, unicodedata
import os
import glob
from file_lib import AmiPath
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
"manuscript", "published", "declare", "conflict", "research", "diagram", "images", "version",
"data", "Fig", "different", "time", "min", "experiments", "group", "analysis",
"study", "activity", "treated", "Extraction", "using", "mean", "work", "file",
"samples", "performed", "analyzed", "support", "values", "approved", "significant",
"thank", "interest", "supported",

}
OIL186 = "/Users/pm286/projects/CEVOpen/searches/oil186" # pmr only

class ProjectCorpus:
    """manages an AMI CProject, not yet fully incorporated"""
    def __init__(self, cwd, tree_glob="./*/"):
        self.cwd = cwd
        self.tree_glob = tree_glob
        self.words = []

    """NEEDS REFACTORING """
    def read_analyze_child_documents(self):
        print("WARNING NYI FULLY")
#        self.files = self.glob_corpus_files()
        self.files = glob.glob(os.path.join(self.cwd, self.tree_glob))
        print("glob", self.cwd, self.tree_glob, str(len(self.files)), self.files[:5])
        for file in self.files:
            section = AmiSection()
            section.read_file(file)
            c = Counter(TextUtil.get_words_in_section(file))
            print(file.split("/")[-2:-1], c.most_common(20))
        wordz = TextUtil.get_aggregate_words_from_files(filez)
        cc = Counter(wordz)
        self.words = wordz
        print("Common", cc.most_common(50))

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

    """
    @staticmethod
    def test_oil():
        print("start test", OIL186)
        assert (os.path.exists(OIL186))
        project = ProjectCorpus(OIL186)
        project.read_analyze_child_documents()
        print("end test")
    """

    def __str__(self):
        return " ".join(map(str, self.sentences))

class Document:
    """ a standalone hierarchical document
    level of Tree or below
    may contain a subset of the conventional document"""

    def __init__(self, file="f"):
        self.sections = None
        self.file = file
        self.words = []
#        if file is not None and os.path.isfile(file):
#            self.words = self.get_words_from_terminal_file(file)


    def create_analyze_sections(self):
        sections_file = os.path.abspath(os.path.join(self.file, "sections"))
        if not os.path.exists(sections_file):
            if not os.path.exists("fulltext.xml"):
                print("No fulltext.xml, so no sections")
            else:
                print("PLEASE CREATE sections with ami sections, will add pyami later")
            return
        terminal_files = glob.glob(os.path.join(sections_file, "**/*.xml"))
        for terminal_file in terminal_files:
            # REFACTOR
            terminal_page = TextUtil.get_words_from_terminal_file(terminal_file)
            self.words.extend(terminal_page.get_words_from_sentences())

    # REFACTOR
    @staticmethod
    def get_words_from_terminal_file(terminal_file):
        ami_section = AmiSection()
        ami_section.read_file(terminal_file)
        ami_section.sentences = [Sentence(s) for s in (nltk.sent_tokenize(ami_section.txt))]
        ami_section.sentences = ami_section.sentences
        if os.path.exists(ami_section.txt_file):
            print("skipping existing text")
        if ami_section.xml_file is not None:
            """read a file as an ami-section of larger document """
            with open(ami_section.xml_file, "r") as f:
                ami_section.xml = f.read()
            # assumes this has been chunked to sections
            #        print("t", len(self.text), self.text[:50])
            ami_section.txt = ami_section.flatten_xml_to_text(ami_section.xml)
            #        self.sentences = Sentence.merge_false_sentence_breaks(self.sentences)

            sentence_file = AmiSection.create_txt_filename_from_xml(ami_section.xml_file)
            if not os.path.exists(sentence_file):
                print("wrote sentence file", sentence_file)
                Sentence.write_numbered_sentence_file(sentence_file, ami_section.sentences)
            ami_section.get_words_from_sentences()
        return ami_section.words


class AmiSection:
    """the xml sub-document with text
    Currently either <title> or <p>

≈    Will often get annotated with sentence markers
    """

    XML_SUFF = ".xml"
    TXT_SUFF = ".txt"

    # sections in template file
    ABSTRACT    = "abstract"
    ACKNOW      = "acknowledge"
    AFFIL       = "affiliation"
    AUTHOR      = "author"
    BACKGROUND  = "background"
    DISCUSS     = "discussion"
    EMPTY       = "empty"
    ETHICS      = "ethics"
    FIG_CAPTION = "fig_caption"
    FRONT       = "front"
    INTRO       = "introduction"
    JRNL        = "jrnl_title"
    KWD         = "keyword"
    METHOD      = "method"
    MATERIAL    = "material"
    OCTREE      = "octree"
    PDFIMAGE    = "pdfimage"
    PUB_DATE    = "pub_date"
    PUBLISHER   = "publisher"
    REFERENCE   = "reference"
    RESULTS     = "results_discuss"
    RESULTS     = "results"
    SECTIONS    = "sections"
    SVG         = "svg"
    TABLE       = "table"
    TITLE       = "title"
    WORD        = "word"

    SECTION_LIST = [
        ABSTRACT,
        ACKNOW,
        AFFIL,
        AUTHOR,
        BACKGROUND,
        DISCUSS,
        EMPTY,
        ETHICS,
        FIG_CAPTION,
        FRONT,
        INTRO,
        JRNL,
        KWD,
        METHOD,
        MATERIAL,
        OCTREE,
        PDFIMAGE,
        PUB_DATE,
        PUBLISHER,
        REFERENCE,
        RESULTS,
        RESULTS,
        SECTIONS,
        SVG,
        TABLE,
        TITLE,
        WORD,
    ]
    def __init__(self):
        self.words = []
        self.xml_file = None
        self.xml = None
        self.txt_file = None
        self.text = None
        self.write_text = True
        self.sentences = None
#        self.read_section()

    def read_file(self, file):
        if file is None:
            raise Exception ("file is None")
        if file.endswith(AmiSection.XML_SUFF):
            self.xml_file = file
            self.txt_file = AmiSection.create_txt_filename_from_xml(self.xml_file)
            if os.path.exists(self.txt_file):
                self.sentences = AmiSection.read_numbered_sentences_file(self.txt_file)
            elif os.path.exists(self.xml_file):
                """read a file as an ami-section of larger document """
                with open(self.xml_file, "r") as f:
                    self.xml = f.read()
                self.txt = self.flatten_xml_to_text(self.xml)
                self.sentences = [Sentence(s) for s in (nltk.sent_tokenize(self.txt))]
#                        self.sentences = Sentence.merge_false_sentence_breaks(self.sentences)
                if self.write_text and not os.path.exists(self.txt_file):
                    print("wrote sentence file", self.txt_file)
                    AmiSection.write_numbered_sentence_file(self.txt_file, self.sentences)
            self.words = self.get_words_from_sentences()

# static utilities
    @staticmethod
    def check_sections(sections):
        for section in sections:
            if section not in AmiSection.SECTION_LIST:
                print("allowed sections", AmiSection.SECTION_LIST)
                raise Exception ("unknown section: ", section)


    @staticmethod
    def create_txt_filename_from_xml(xml_file):
        sentence_file = xml_file[:-len(AmiSection.XML_SUFF)] + AmiSection.TXT_SUFF
        return sentence_file

    @staticmethod
    def flatten_xml_to_text(xml):
        """removes xml tags , diacritics, """
        text = TextUtil.strip_xml_tags(xml)
        text = TextUtil.remove_para_tags(text)
        text = unicodedata.normalize(NFKD, text)
        text = TextUtil.flatten_non_ascii(text)
        return text

    @staticmethod
    def write_numbered_sentence_file(file, sentences):
        """writes numbered sentences"""
        with open(file, "w") as f:
            for i, sentence in enumerate(sentences):
                f.write(str(i) + Sentence.NUMBER_SPLIT + sentence.string + "\n")

    @staticmethod
    def read_numbered_sentences_file(file):
        """ read file with lines of form line_no<sep>text where line_no starts at 0"""
#        print("reading sentences")
        sentences = None
        if file is not None and os.path.exists(file):
            with open(file, "r") as f:
                lines = f.readlines()
            if len(lines) == 0:
#                print("warning empty file", file)
                pass
#            else:
#                print("l", len(lines), lines[0])
            try:
                sentences = Sentence.read_number_sentences(lines)
            except Exception as ex:
                print(ex, file)
#            if len(sentences) > 0:
#                print("s", len(sentences), sentences[0])


        return sentences


    def get_words_from_sentences(self) -> list:
        for sentence in self.sentences:
            words = sentence.words
#            print("w", sentence, len(words))
            self.words.extend(words)
        return self.words

class Sentence:

    NUMBER_SPLIT = ": "

    def __init__(self, string):
        self.string = string
#        self.words = Sentence.tokenize_to_words(string)
        self.words = string.split(" ")
        self.words = Sentence.remove_punct(self.words)

    @staticmethod

    def tokenize_to_words(string):
        """ may be quite slow compared to brute splitting at spaces

        returns: list of words"""
        return nltk.word_tokenize(string)

    @staticmethod
    def remove_punct(tokens):
        """removes tokens consisting of punctuation in present `PUNCT`

        tokens: list of words
        returns: words diminished by deleted punctuation

        """
        tokens = [token for token in tokens if not token in PUNCT]
        return tokens


    @staticmethod
    def read_numbered_line(text):
        chunks = text.split(Sentence.NUMBER_SPLIT)
        if not len(chunks) > 1 or not str.isdigit(text[0]):
            raise Exception("Not a numbered sentence", text)
        return int(chunks[0]), chunks[1]

    @staticmethod
    def read_number_sentences(lines):
        """reads lines of form line_no<sep>text where line_no starts at 0"""
        sentences = []
        lasti = -1
        for i, line in enumerate(lines):
            line_no, text = Sentence.read_numbered_line(line)
            if i != lasti + 1 or i != line_no:
                raise Exception("failed to read lines in order", i, line_no, line)
            lasti = i
            sentences.append(Sentence(text))
        return sentences

    def __str__(self):
        return " ".join(map(str, self.words))

class TextUtil:

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

    @staticmethod
    def get_aggregate_words_from_files(files):
        all_words = []
        for file in files:
            words = TextUtil.get_words_in_section(file)
            all_words.extend(words)
        return all_words

    @staticmethod
    # move to AmiSection
    def get_words_in_section(file):
#        document = Document(file)  # level of tree
#        words = document.words
        section = AmiSection()
        section.read_file(file)
        words = section.words

        word_filter = WordFilter()
 #       words = word_filter.filter_words(words)
        words = TextUtil.filter_words(section.words)
        return words

    @staticmethod #OBSOLETE
    def filter_words(words):
        words = [w for w in words if len(w) > 2]
        words = [w for w in words if w.lower() not in STOPWORDS_EN]
        words = [w for w in words if w.lower() not in STOPWORDS_PUB]
        words = [w for w in words if not w.isnumeric()]
        return words

class WordFilter:

    """ filters a list of words
    generally deletes words not satisfying a condition but this may develop
    """
    def __init__(self):
        self.min_length = 2
        self.use_lower_stopwords = True
        self.stop_words_set = set(STOPWORDS_EN).union(STOPWORDS_PUB)
        self.delete_numeric = True
        self.delete_non_alphanum = True
        self.regex = None
        self.keep_regex = True
        self.split_spaces = False

    def filter_words(self, words):
        words = self.delete_short_words(words, self.min_length)
        words = self.delete_stop_words(words, self.stop_words)
        if self.delete_numeric:
            words = self.delete_num(words)
        if self.delete_non_alphanumeric:
            words = self.delete_non_alphanum(words)
        if self.regex is not None:
            words = self.filter_by_regex(words, self.regex, self.keep_regex)

        return words

    def set_regex(self, regex_string, keep=True):
        """ filter words by regex

        regex_string: regex to match
        keep: if True accept matching words else reject matches
        """
        self.regex = re.compile(regex_string)
        self.keep_regex = keep


    @staticmethod
    def delete_num(self, words):
        """delete words satisfying str.isnumeric() """
        words = [w for w in words if not w.isnumeric()]
        return words

    @staticmethod
    def delete_non_alphanum(self, words):
        """delete strings satisfying str.isalnum()"""
        words = [w for w in words if w.isalnum()]
        return words

    @staticmethod
    def delete_stop_words_list(self, words, stop_words_list):
        """delete words in lists of stop words"""
        for stop_words in stop_words_list:
            words = [w for w in words if w.lower() not in stop_words]
        return words

    def filter_stop_words(self, words, stop_words, keep=False):
        if keep:
            words = [w for w in words if w.lower() in stop_words]
        else:
            words = [w for w in words if w.lower() not in stop_words]
        return words


    def delete_short_words(self, words, min_length):
        """delete words less than equal to min_length"""
        words = [w for w in words if len(w) > min_length]
        return words

    def filter_by_regex(self, words, regex_string, keep=True):
        words1 = [w for w in words if re.match(regex_string)]
        return words1


def main():
    print("started text_lib")
#    ProjectCorpus.test(CCT_PROJ)
#    ProjectCorpus.test(LIION_PROJ)
    ProjectCorpus.test_oil()
    print("finished text_lib")

if __name__ == "__main__":
    main()
else:
#    main()
    pass

class Ngrams:
    """Various codes from StackOverflow and similar"""

    def tokenize(string):
        """Convert string to lowercase and split into words (ignoring
        punctuation), returning list of words.
        """
        return re.findall(r'\w+', string.lower())


    def count_ngrams(self, lines, min_length=2, max_length=4):
        """Iterate through given lines iterator (file object or list of
        lines) and return n-gram frequencies. The return value is a dict
        mapping the length of the n-gram to a collections.Counter
        object of n-gram tuple and number of times that n-gram occurred.
        Returned dict includes n-grams of length min_length to max_length.
        """
        self.lengths = range(min_length, max_length + 1)
        self.ngrams = {length: collections.Counter() for length in lengths}
        self.queue = collections.deque(maxlen=max_length)

    # Helper function to add n-grams at start of current queue to dict
    def add_queue(self):
        current = tuple(self.queue)
        for length in self.lengths:
            if len(current) >= length:
                self.ngrams[length][current[:length]] += 1

    # Loop through all lines and words and add n-grams to dict
        for line in self.lines:
            for word in tokenize(line):
                self.queue._append_facet(word)
                if len(self.queue) >= self.max_length:
                    add_queue()

        # Make sure we get the n-grams at the tail end of the queue
        while len(self.queue) > self.min_length:
            self.queue.popleft()
            add_queue()

        return self.ngrams


    def print_most_frequent(ngrams, num=10):
        """Print num most common n-grams of each length in n-grams dict."""
        for n in sorted(ngrams):
            print('----- {} most common {}-grams -----'.format(num, n))
            for gram, count in ngrams[n].most_common(num):
                print('{0}: {1}'.format(' '.join(gram), count))
            print('')


    def test(file):
        with open(file) as f:
            ngrams = count_ngrams(f)
        print_most_frequent(ngrams)


# http://www.locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/

    def test1():
        input_list = "to be or not to be that is the question whether tis nob"


    @staticmethod
    def find_bigrams(input_list):
        return zip(input_list, input_list[1:])

    @staticmethod
    def explicit_ngrams(input_list):
        # Bigrams
        zip(input_list, input_list[1:])
        # Trigrams
        zip(input_list, input_list[1:], input_list[2:])
        # and so on
        zip(input_list, input_list[1:], input_list[2:], input_list[3:])

    @staticmethod
    def find_ngrams(input_list, n):
        return zip(*[input_list[i:] for i in range(n)])


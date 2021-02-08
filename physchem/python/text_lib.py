
import numpy as np
import matplotlib.pyplot as plt
import nltk, unicodedata
import os

import xml.etree.ElementTree as ET
import re

tags = {
    "\n": "",
    "<sup>": "^",
    "</sup>": "",
    "<sub>": "_",
    "</sub>": "",
    "</xref>": "",
}

regexes = {
    " +<": "<",
    "<xref[^>]*>": "@",
}


class TextLib():
    def __init__(self):
        pass

    def xml_parse(self, file):
        """extract running text-words without tags"""
        with open(file, "r") as f:
            text = f.read()
        for key in tags:
            text = text.replace(key, tags[key])
        for regex in regexes:
            text = re.sub(regex, regexes[regex], text)
#        text = unicodedata.normalize("NKFD", text)
        ascii_text = text.encode("ascii", "ignore").decode("utf-8", "ignore")
        tree = ET.fromstring(text)
        tt = str.join(" ", list(tree.itertext()))
        return tt

    @staticmethod
    def remove_non_alphanumeric(text, remove_digits="False"):
        pattern = r'[^A-Za-z0-9\s]' if not remove_digits else r'[A-Za-z\s]'
        text = re.sub(pattern, '', text)
        return text

    def test(self):
        self.test1(os.path.abspath("../liion/PMC7040616/sections/1_body/0_1__introduction/1_p.xml"))
#        self.test1(os.path.abspath("../liion/PMC7040616/sections/2_back/3_ref-list/1_ref.xml"))

    def test1(self, file):
        texts = self.xml_parse(file)
        print("========")
        sentences = nltk.sent_tokenize(texts)
        for sentence in sentences:
            print(">", sentence)
        print("sentences", len(sentences), "texts",  len(texts), texts)
        word_tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
        print(word_tokens)


def main():
    print("started text_lib")
    TextLib().test()
    print("finished text_lib")

if __name__ == "__main__":
    main()
else:
    main()
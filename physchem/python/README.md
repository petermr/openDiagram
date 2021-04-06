# alpha code for searching document corpus

## prerequisites

- create getpapers output
- run `ami section` to create sections AND/OR
- run `ami pdfbox` to extract images

# strategy

The search is hierarchical, maybe with back wards loops.

## search foreign repository with `(py)getpapers`

This is well established and be a keyword search and depends on the repo's engines - very variable. It's likely to contain many false positives. The results are stored as full text , XML and PDF. The XML can be split into sections with `ami section` or `pyamisection` (being written - nearly finished.

## search for sections

Use glob-based wildcards to extract only the sections of interest (e.g. abstract, references, methods, results...). see [./file_lib.py](section search)

## search content in sections, using dictionaries

The new code [./search.py] will replaces `ami search`.

## DEMO with multiple projects , dictionaries and sections

** for Monday 2021-03-22 **
** RUN **

```
python search_lib.py
```

# demo

## section search

This is set up with files from Steel articles and is hardcoded into `file_lib`.

https://github.com/petermr/openDiagram/blob/master/physchem/python/file_lib.py

This exercises about 20 globs that are useful for scientific papers.
At this stage just try to run it and report any errors. It's fairly easy to point it at your own project.

## word frequencies

An example hardcoded into:

https://github.com/petermr/openDiagram/blob/master/physchem/python/text_lib.py

This extracts the content from sections, removes stopwords , and creates a Counter (Multiset) to show the freequencies of words ("word cloud").

## dictionary search

This will apply dictionaries to sections. Not yet written.

https://github.com/petermr/openDiagram/blob/master/physchem/python/search.py

## xml and sections

Will create sections from JATS-XML (replaces `ami section`). Over 50% written.

https://github.com/petermr/openDiagram/blob/master/physchem/python/xml_lib.py

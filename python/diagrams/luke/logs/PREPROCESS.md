# Preprocessing witn ami
```
$ ami -p papers20210121/ makeproject --rawfiletypes=pdf

Generic values (AMIMakeProjectTool)
================================

Specific values (AMIMakeProjectTool)
================================
```
project has been created. Verify:
````
$ tree
.
├── logs
│   └── ami.log
├── papers.zip
├── papers20210121
│   ├── make_project.json
│   ├── physrevb.94.125203_1_
│   │   └── fulltext.pdf
│   ├── physrevb.96.161201_1_
│   │   └── fulltext.pdf
│   ├── physrevlett.117.046602_1_
│   │   └── fulltext.pdf
│   ├── physrevlett.125.045701_1_
│   │   └── fulltext.pdf
│   ├── physrevlett.125.085902_1_
│   │   └── fulltext.pdf
│   └── physrevmaterials.4.054002
│       └── fulltext.pdf
└── target
    └── log.xml

9 directories, 10 files
```
###extraction of images
````
$ ami -p papers20210121/ pdfbox

Generic values (AMIPDFTool)
================================

Specific values (AMIPDFTool)
================================
AMIPDFTool cTree: physrevb.94.125203_1_
cTree: physrevb.94.125203_1_
pi>include: [-1]

ipageIncluder include: [-1]

 max pages: 5 0 
pageIncluder pages include: [0, 1, 2, 3, 4]
[1][2][.0]Jan 22, 2021 9:23:46 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for Delta1 (8) in font CBKLNO+MTMI
Jan 22, 2021 9:23:46 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for bracketleftbigg (2) in font CBKMNK+MTEX
Jan 22, 2021 9:23:46 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for parenleftbigg (3) in font CBKMNK+MTEX
Jan 22, 2021 9:23:46 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for parenrightbigg (4) in font CBKMNK+MTEX
Jan 22, 2021 9:23:46 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for bracketrightbigg (5) in font CBKMNK+MTEX
Jan 22, 2021 9:23:46 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for parenleftbig (6) in font CBKMNK+MTEX
Jan 22, 2021 9:23:46 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for parenrightbig (7) in font CBKMNK+MTEX
Jan 22, 2021 9:23:46 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for Gamma1 (11) in font CBKLNO+MTMI
[3][.0]Jan 22, 2021 9:23:47 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for prime (4) in font CBKLNP+MTSY
[4][.0][.1][.2][5] img  img  img  img  img  5 
pageIncluder pages include: [5, 6, 7, 8, 9]
[6]end: 
AMIPDFTool cTree: physrevb.96.161201_1_
cTree: physrevb.96.161201_1_
pi>include: [-1]

ipageIncluder include: [-1]

 max pages: 5 0 
pageIncluder pages include: [0, 1, 2, 3, 4]
[1][2][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.0][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1][.1]Jan 22, 2021 9:23:50 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for Gamma1 (3) in font NNCECD+MTMI
[3][.0][.0]tokenList>5000: 6731
pp: 1107 pp: 554 parse: 1905; d 38357 prims: 554/ extract: 1
pp: 553 tokenList>5000: 6748
pp: 1114 pp: 557 parse: 1897; d 38388 prims: 557/ extract: 0
pp: 549 tokenList>5000: 6970
pp: 1159 pp: 580 parse: 1986; d 39534 prims: 580/ extract: 0
[4]Jan 22, 2021 9:24:05 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for Phi1 (7) in font NNCECD+MTMI
[5]large SVG: (336786) PageSerial [page=1, subPage=null]
large SVG: (10383827) PageSerial [page=2, subPage=null]
 img  5 
pageIncluder pages include: [5, 6, 7, 8, 9]
[6]end: 
AMIPDFTool cTree: physrevlett.117.046602_1_
cTree: physrevlett.117.046602_1_
pi>include: [-1]

ipageIncluder include: [-1]

 max pages: 5 0 
pageIncluder pages include: [0, 1, 2, 3, 4]
[1][2]Jan 22, 2021 9:24:07 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for C3 (2) in font CLGLMI+AdvP4C4E74
tokenList>5000: 12403
pp: 1757 pp: 879 parse: 4759; d 73475 prims: 879/ extract: 1
[3]Jan 22, 2021 9:24:12 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for C6 (3) in font CLGLMI+AdvP4C4E74
[4][.0][5][.0]large SVG: (1020589) PageSerial [page=3, subPage=null]
 img  img  5 
pageIncluder pages include: [5, 6, 7, 8, 9]
[6]end: 
AMIPDFTool cTree: physrevlett.125.045701_1_
cTree: physrevlett.125.045701_1_
pi>include: [-1]

ipageIncluder include: [-1]

 max pages: 5 0 
pageIncluder pages include: [0, 1, 2, 3, 4]
[1][2][.0]!![3]![4][.0][.1][5][.0] img  img  img  img  5 
pageIncluder pages include: [5, 6, 7, 8, 9]
[6]!!end: 
AMIPDFTool cTree: physrevlett.125.085902_1_
cTree: physrevlett.125.085902_1_
pi>include: [-1]

ipageIncluder include: [-1]

 max pages: 5 0 
pageIncluder pages include: [0, 1, 2, 3, 4]
[1]Jan 22, 2021 9:24:19 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for C6 (1) in font BIMMLC+AdvP4C4E74
[2]Jan 22, 2021 9:24:19 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for C3 (3) in font BIMMLC+AdvP4C4E74
[.0][3][.0][4][.0][5]Jan 22, 2021 9:24:21 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicode
WARNING: No Unicode mapping for C138 (4) in font BIMMLC+AdvP4C4E74
[.0] img  img  img  img  5 
pageIncluder pages include: [5, 6, 7, 8, 9]
[6][7]end: 
AMIPDFTool cTree: physrevmaterials.4.054002
cTree: physrevmaterials.4.054002
pi>include: [-1]

ipageIncluder include: [-1]

 max pages: 5 0 
pageIncluder pages include: [0, 1, 2, 3, 4]
[1][.0][2][.0][3][.0][.1][4][.0][5] img  img  img  img  img end: 
(base) pm286macbook:luke pm286$ 
```
Verify:
```
(base) pm286macbook:luke pm286$ tree
.
├── logs
│   └── ami.log
├── papers.zip
├── papers20210121
│   ├── make_project.json
│   ├── physrevb.94.125203_1_
│   │   ├── fulltext.pdf
│   │   ├── pdfimages
│   │   │   ├── image.2.1.71_275.60_228.png
│   │   │   ├── image.3.1.65_281.450_692.png
│   │   │   ├── image.4.1.65_281.60_306.png
│   │   │   ├── image.4.2.340_532.61_372.png
│   │   │   └── image.4.3.313_558.611_714.png
│   │   └── svg
│   │       ├── fulltext-page.0.svg
│   │       ├── fulltext-page.1.svg
│   │       ├── fulltext-page.2.svg
│   │       ├── fulltext-page.3.svg
│   │       ├── fulltext-page.4.svg
│   │       └── fulltext-page.5.svg
│   ├── physrevb.96.161201_1_
│   │   ├── fulltext.pdf
│   │   ├── pdfimages
│   │   │   └── image.2.1.230_247.198_212.png
│   │   └── svg
│   │       ├── fulltext-page.0.svg
│   │       ├── fulltext-page.1.svg
│   │       ├── fulltext-page.2.svg
│   │       ├── fulltext-page.3.svg
│   │       ├── fulltext-page.4.svg
│   │       └── fulltext-page.5.svg
│   ├── physrevlett.117.046602_1_
│   │   ├── fulltext.pdf
│   │   ├── pdfimages
│   │   │   ├── image.4.1.332_543.55_214.png
│   │   │   └── image.5.1.137_212.303_308.png
│   │   └── svg
│   │       ├── fulltext-page.0.svg
│   │       ├── fulltext-page.1.svg
│   │       ├── fulltext-page.2.svg
│   │       ├── fulltext-page.3.svg
│   │       ├── fulltext-page.4.svg
│   │       └── fulltext-page.5.svg
│   ├── physrevlett.125.045701_1_
│   │   ├── fulltext.pdf
│   │   ├── pdfimages
│   │   │   ├── image.2.1.56_556.335_639.png
│   │   │   ├── image.4.1.328_548.462_661.png
│   │   │   ├── image.4.2.55_295.55_337.png
│   │   │   └── image.5.1.400_475.474_478.png
│   │   └── svg
│   │       ├── fulltext-page.0.svg
│   │       ├── fulltext-page.1.svg
│   │       ├── fulltext-page.2.svg
│   │       ├── fulltext-page.3.svg
│   │       ├── fulltext-page.4.svg
│   │       └── fulltext-page.5.svg
│   ├── physrevlett.125.085902_1_
│   │   ├── fulltext.pdf
│   │   ├── pdfimages
│   │   │   ├── image.2.1.316_559.55_325.png
│   │   │   ├── image.3.1.52_297.398_628.png
│   │   │   ├── image.4.1.55_558.527_650.png
│   │   │   └── image.5.1.400_475.642_646.png
│   │   └── svg
│   │       ├── fulltext-page.0.svg
│   │       ├── fulltext-page.1.svg
│   │       ├── fulltext-page.2.svg
│   │       ├── fulltext-page.3.svg
│   │       ├── fulltext-page.4.svg
│   │       ├── fulltext-page.5.svg
│   │       └── fulltext-page.6.svg
│   └── physrevmaterials.4.054002
│       ├── fulltext.pdf
│       ├── pdfimages
│       │   ├── image.1.1.114_128.247_260.png
│       │   ├── image.2.1.54_555.60_264.png
│       │   ├── image.3.1.65_281.60_406.png
│       │   ├── image.3.2.328_544.60_239.png
│       │   └── image.4.1.328_544.60_230.png
│       └── svg
│           ├── fulltext-page.0.svg
│           ├── fulltext-page.1.svg
│           ├── fulltext-page.2.svg
│           ├── fulltext-page.3.svg
│           └── fulltext-page.4.svg
└── target
    └── log.xml

```
`

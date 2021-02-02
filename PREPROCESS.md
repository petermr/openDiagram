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

(base) pm286macbook:luke pm286$ ami --inputname=raw --output=rawoctree -p papers20210121/ image --octree 8 --outputfiles="octree"

Generic values (AMIImageTool)
================================

Specific values (AMIImageTool)
================================
AMIImageTool cTree: physrevb.94.125203_1_
 >>>>> imageDirs: 5
T: 714077/W: 670163/NW: 43914
*****OK...physrevb.94.125203_1_//image.2.1.71_275.60_228
physrevb.94.125203_1_//image.2.1.71_275.60_228
transforming: image.2.1.71_275.60_228/raw.png
htmlFile papers20210121/physrevb.94.125203_1_/pdfimages/image.2.1.71_275.60_228/images.html
T: 998865/W: 856315/NW: 142550
*****OK...physrevb.94.125203_1_//image.3.1.65_281.450_692
physrevb.94.125203_1_//image.3.1.65_281.450_692
transforming: image.3.1.65_281.450_692/raw.png
htmlFile papers20210121/physrevb.94.125203_1_/pdfimages/image.3.1.65_281.450_692/images.html
T: 923400/W: 820632/NW: 102768
*****OK...physrevb.94.125203_1_//image.4.1.65_281.60_306
physrevb.94.125203_1_//image.4.1.65_281.60_306
transforming: image.4.1.65_281.60_306/raw.png
htmlFile papers20210121/physrevb.94.125203_1_/pdfimages/image.4.1.65_281.60_306/images.html
T: 1039200/W: 986444/NW: 52756
*****OK...physrevb.94.125203_1_//image.4.2.340_532.61_372
physrevb.94.125203_1_//image.4.2.340_532.61_372
transforming: image.4.2.340_532.61_372/raw.png
htmlFile papers20210121/physrevb.94.125203_1_/pdfimages/image.4.2.340_532.61_372/images.html
T: 436560/W: 408924/NW: 27636
*****OK...physrevb.94.125203_1_//image.4.3.313_558.611_714
physrevb.94.125203_1_//image.4.3.313_558.611_714
transforming: image.4.3.313_558.611_714/raw.png
htmlFile papers20210121/physrevb.94.125203_1_/pdfimages/image.4.3.313_558.611_714/images.html
AMIImageTool cTree: physrevb.96.161201_1_
 >>>>> imageDirs: 1
T: 4526/W: 3322/NW: 1204
*****OK...physrevb.96.161201_1_//image.2.1.230_247.198_212
physrevb.96.161201_1_//image.2.1.230_247.198_212
transforming: image.2.1.230_247.198_212/raw.png
htmlFile papers20210121/physrevb.96.161201_1_/pdfimages/image.2.1.230_247.198_212/images.html
AMIImageTool cTree: physrevlett.117.046602_1_
 >>>>> imageDirs: 2
T: 583656/W: 581219/NW: 2437
*****OK...physrevlett.117.046602_1_//image.4.1.332_543.55_214
physrevlett.117.046602_1_//image.4.1.332_543.55_214
transforming: image.4.1.332_543.55_214/raw.png
htmlFile papers20210121/physrevlett.117.046602_1_/pdfimages/image.4.1.332_543.55_214/images.html
T: 6220/W: 6220/NW: 0
*****OK...physrevlett.117.046602_1_//image.5.1.137_212.303_308
physrevlett.117.046602_1_//image.5.1.137_212.303_308
transforming: image.5.1.137_212.303_308/raw.png
htmlFile papers20210121/physrevlett.117.046602_1_/pdfimages/image.5.1.137_212.303_308/images.html
AMIImageTool cTree: physrevlett.125.045701_1_
 >>>>> imageDirs: 4
T: 2637078/W: 2066786/NW: 570292
*****OK...physrevlett.125.045701_1_//image.2.1.56_556.335_639
physrevlett.125.045701_1_//image.2.1.56_556.335_639
transforming: image.2.1.56_556.335_639/raw.png
htmlFile papers20210121/physrevlett.125.045701_1_/pdfimages/image.2.1.56_556.335_639/images.html
T: 759276/W: 740096/NW: 19180
*****OK...physrevlett.125.045701_1_//image.4.1.328_548.462_661
physrevlett.125.045701_1_//image.4.1.328_548.462_661
transforming: image.4.1.328_548.462_661/raw.png
htmlFile papers20210121/physrevlett.125.045701_1_/pdfimages/image.4.1.328_548.462_661/images.html
T: 1176000/W: 1159939/NW: 16061
*****OK...physrevlett.125.045701_1_//image.4.2.55_295.55_337
physrevlett.125.045701_1_//image.4.2.55_295.55_337
transforming: image.4.2.55_295.55_337/raw.png
htmlFile papers20210121/physrevlett.125.045701_1_/pdfimages/image.4.2.55_295.55_337/images.html
T: 6220/W: 6220/NW: 0
*****OK...physrevlett.125.045701_1_//image.5.1.400_475.474_478
physrevlett.125.045701_1_//image.5.1.400_475.474_478
transforming: image.5.1.400_475.474_478/raw.png
htmlFile papers20210121/physrevlett.125.045701_1_/pdfimages/image.5.1.400_475.474_478/images.html
AMIImageTool cTree: physrevlett.125.085902_1_
 >>>>> imageDirs: 4
T: 2026938/W: 1259519/NW: 767419
*****OK...physrevlett.125.085902_1_//image.2.1.316_559.55_325
physrevlett.125.085902_1_//image.2.1.316_559.55_325
transforming: image.2.1.316_559.55_325/raw.png
htmlFile papers20210121/physrevlett.125.085902_1_/pdfimages/image.2.1.316_559.55_325/images.html
T: 1727544/W: 1674677/NW: 52867
*****OK...physrevlett.125.085902_1_//image.3.1.52_297.398_628
physrevlett.125.085902_1_//image.3.1.52_297.398_628
transforming: image.3.1.52_297.398_628/raw.png
htmlFile papers20210121/physrevlett.125.085902_1_/pdfimages/image.3.1.52_297.398_628/images.html
T: 1628550/W: 1590728/NW: 37822
*****OK...physrevlett.125.085902_1_//image.4.1.55_558.527_650
physrevlett.125.085902_1_//image.4.1.55_558.527_650
transforming: image.4.1.55_558.527_650/raw.png
htmlFile papers20210121/physrevlett.125.085902_1_/pdfimages/image.4.1.55_558.527_650/images.html
T: 5909/W: 5909/NW: 0
*****OK...physrevlett.125.085902_1_//image.5.1.400_475.642_646
physrevlett.125.085902_1_//image.5.1.400_475.642_646
transforming: image.5.1.400_475.642_646/raw.png
htmlFile papers20210121/physrevlett.125.085902_1_/pdfimages/image.5.1.400_475.642_646/images.html
AMIImageTool cTree: physrevmaterials.4.054002
 >>>>> imageDirs: 5
T: 3248/W: 3248/NW: 0
*****OK...physrevmaterials.4.054002//image.1.1.114_128.247_260
physrevmaterials.4.054002//image.1.1.114_128.247_260
transforming: image.1.1.114_128.247_260/raw.png
htmlFile papers20210121/physrevmaterials.4.054002/pdfimages/image.1.1.114_128.247_260/images.html
T: 1780680/W: 1178570/NW: 602110
*****OK...physrevmaterials.4.054002//image.2.1.54_555.60_264
physrevmaterials.4.054002//image.2.1.54_555.60_264
transforming: image.2.1.54_555.60_264/raw.png
htmlFile papers20210121/physrevmaterials.4.054002/pdfimages/image.2.1.54_555.60_264/images.html
T: 1298700/W: 1260778/NW: 37922
*****OK...physrevmaterials.4.054002//image.3.1.65_281.60_406
physrevmaterials.4.054002//image.3.1.65_281.60_406
transforming: image.3.1.65_281.60_406/raw.png
htmlFile papers20210121/physrevmaterials.4.054002/pdfimages/image.3.1.65_281.60_406/images.html
T: 915600/W: 876590/NW: 39010
*****OK...physrevmaterials.4.054002//image.3.2.328_544.60_239
physrevmaterials.4.054002//image.3.2.328_544.60_239
transforming: image.3.2.328_544.60_239/raw.png
htmlFile papers20210121/physrevmaterials.4.054002/pdfimages/image.3.2.328_544.60_239/images.html
T: 868350/W: 793871/NW: 74479
*****OK...physrevmaterials.4.054002//image.4.1.328_544.60_230
physrevmaterials.4.054002//image.4.1.328_544.60_230
transforming: image.4.1.328_544.60_230/raw.png
htmlFile papers20210121/physrevmaterials.4.054002/pdfimages/image.4.1.328_544.60_230/images.html
(base) pm286macbook:luke pm286$ ami --inputname=raw --output=rawoctree -p papers20210121/ image --octree 8 --outputfiles="channels"

Generic values (AMIImageTool)
================================

Specific values (AMIImageTool)
================================
AMIImageTool cTree: physrevb.94.125203_1_
 >>>>> imageDirs: 5
T: 714077/W: 670163/NW: 43914
*****OK...physrevb.94.125203_1_//image.2.1.71_275.60_228
physrevb.94.125203_1_//image.2.1.71_275.60_228
transforming: image.2.1.71_275.60_228/raw.png
htmlFile papers20210121/physrevb.94.125203_1_/pdfimages/image.2.1.71_275.60_228/images.html
T: 998865/W: 856315/NW: 142550
*****OK...physrevb.94.125203_1_//image.3.1.65_281.450_692
physrevb.94.125203_1_//image.3.1.65_281.450_692
transforming: image.3.1.65_281.450_692/raw.png
htmlFile papers20210121/physrevb.94.125203_1_/pdfimages/image.3.1.65_281.450_692/images.html
T: 923400/W: 820632/NW: 102768
*****OK...physrevb.94.125203_1_//image.4.1.65_281.60_306
physrevb.94.125203_1_//image.4.1.65_281.60_306
transforming: image.4.1.65_281.60_306/raw.png
htmlFile papers20210121/physrevb.94.125203_1_/pdfimages/image.4.1.65_281.60_306/images.html
T: 1039200/W: 986444/NW: 52756
*****OK...physrevb.94.125203_1_//image.4.2.340_532.61_372
physrevb.94.125203_1_//image.4.2.340_532.61_372
transforming: image.4.2.340_532.61_372/raw.png
htmlFile papers20210121/physrevb.94.125203_1_/pdfimages/image.4.2.340_532.61_372/images.html
T: 436560/W: 408924/NW: 27636
*****OK...physrevb.94.125203_1_//image.4.3.313_558.611_714
physrevb.94.125203_1_//image.4.3.313_558.611_714
transforming: image.4.3.313_558.611_714/raw.png
htmlFile papers20210121/physrevb.94.125203_1_/pdfimages/image.4.3.313_558.611_714/images.html
AMIImageTool cTree: physrevb.96.161201_1_
 >>>>> imageDirs: 1
T: 4526/W: 3322/NW: 1204
*****OK...physrevb.96.161201_1_//image.2.1.230_247.198_212
physrevb.96.161201_1_//image.2.1.230_247.198_212
transforming: image.2.1.230_247.198_212/raw.png
htmlFile papers20210121/physrevb.96.161201_1_/pdfimages/image.2.1.230_247.198_212/images.html
AMIImageTool cTree: physrevlett.117.046602_1_
 >>>>> imageDirs: 2
T: 583656/W: 581219/NW: 2437
*****OK...physrevlett.117.046602_1_//image.4.1.332_543.55_214
physrevlett.117.046602_1_//image.4.1.332_543.55_214
transforming: image.4.1.332_543.55_214/raw.png
htmlFile papers20210121/physrevlett.117.046602_1_/pdfimages/image.4.1.332_543.55_214/images.html
T: 6220/W: 6220/NW: 0
*****OK...physrevlett.117.046602_1_//image.5.1.137_212.303_308
physrevlett.117.046602_1_//image.5.1.137_212.303_308
transforming: image.5.1.137_212.303_308/raw.png
htmlFile papers20210121/physrevlett.117.046602_1_/pdfimages/image.5.1.137_212.303_308/images.html
AMIImageTool cTree: physrevlett.125.045701_1_
 >>>>> imageDirs: 4
T: 2637078/W: 2066786/NW: 570292
*****OK...physrevlett.125.045701_1_//image.2.1.56_556.335_639
physrevlett.125.045701_1_//image.2.1.56_556.335_639
transforming: image.2.1.56_556.335_639/raw.png
htmlFile papers20210121/physrevlett.125.045701_1_/pdfimages/image.2.1.56_556.335_639/images.html
T: 759276/W: 740096/NW: 19180
*****OK...physrevlett.125.045701_1_//image.4.1.328_548.462_661
physrevlett.125.045701_1_//image.4.1.328_548.462_661
transforming: image.4.1.328_548.462_661/raw.png
htmlFile papers20210121/physrevlett.125.045701_1_/pdfimages/image.4.1.328_548.462_661/images.html
T: 1176000/W: 1159939/NW: 16061
*****OK...physrevlett.125.045701_1_//image.4.2.55_295.55_337
physrevlett.125.045701_1_//image.4.2.55_295.55_337
transforming: image.4.2.55_295.55_337/raw.png
htmlFile papers20210121/physrevlett.125.045701_1_/pdfimages/image.4.2.55_295.55_337/images.html
T: 6220/W: 6220/NW: 0
*****OK...physrevlett.125.045701_1_//image.5.1.400_475.474_478
physrevlett.125.045701_1_//image.5.1.400_475.474_478
transforming: image.5.1.400_475.474_478/raw.png
htmlFile papers20210121/physrevlett.125.045701_1_/pdfimages/image.5.1.400_475.474_478/images.html
AMIImageTool cTree: physrevlett.125.085902_1_
 >>>>> imageDirs: 4
T: 2026938/W: 1259519/NW: 767419
*****OK...physrevlett.125.085902_1_//image.2.1.316_559.55_325
physrevlett.125.085902_1_//image.2.1.316_559.55_325
transforming: image.2.1.316_559.55_325/raw.png
htmlFile papers20210121/physrevlett.125.085902_1_/pdfimages/image.2.1.316_559.55_325/images.html
T: 1727544/W: 1674677/NW: 52867
*****OK...physrevlett.125.085902_1_//image.3.1.52_297.398_628
physrevlett.125.085902_1_//image.3.1.52_297.398_628
transforming: image.3.1.52_297.398_628/raw.png
htmlFile papers20210121/physrevlett.125.085902_1_/pdfimages/image.3.1.52_297.398_628/images.html
T: 1628550/W: 1590728/NW: 37822
*****OK...physrevlett.125.085902_1_//image.4.1.55_558.527_650
physrevlett.125.085902_1_//image.4.1.55_558.527_650
transforming: image.4.1.55_558.527_650/raw.png
htmlFile papers20210121/physrevlett.125.085902_1_/pdfimages/image.4.1.55_558.527_650/images.html
T: 5909/W: 5909/NW: 0
*****OK...physrevlett.125.085902_1_//image.5.1.400_475.642_646
physrevlett.125.085902_1_//image.5.1.400_475.642_646
transforming: image.5.1.400_475.642_646/raw.png
htmlFile papers20210121/physrevlett.125.085902_1_/pdfimages/image.5.1.400_475.642_646/images.html
AMIImageTool cTree: physrevmaterials.4.054002
 >>>>> imageDirs: 5
T: 3248/W: 3248/NW: 0
*****OK...physrevmaterials.4.054002//image.1.1.114_128.247_260
physrevmaterials.4.054002//image.1.1.114_128.247_260
transforming: image.1.1.114_128.247_260/raw.png
htmlFile papers20210121/physrevmaterials.4.054002/pdfimages/image.1.1.114_128.247_260/images.html
T: 1780680/W: 1178570/NW: 602110
*****OK...physrevmaterials.4.054002//image.2.1.54_555.60_264
physrevmaterials.4.054002//image.2.1.54_555.60_264
transforming: image.2.1.54_555.60_264/raw.png
htmlFile papers20210121/physrevmaterials.4.054002/pdfimages/image.2.1.54_555.60_264/images.html
T: 1298700/W: 1260778/NW: 37922
*****OK...physrevmaterials.4.054002//image.3.1.65_281.60_406
physrevmaterials.4.054002//image.3.1.65_281.60_406
transforming: image.3.1.65_281.60_406/raw.png
htmlFile papers20210121/physrevmaterials.4.054002/pdfimages/image.3.1.65_281.60_406/images.html
T: 915600/W: 876590/NW: 39010
*****OK...physrevmaterials.4.054002//image.3.2.328_544.60_239
physrevmaterials.4.054002//image.3.2.328_544.60_239
transforming: image.3.2.328_544.60_239/raw.png
htmlFile papers20210121/physrevmaterials.4.054002/pdfimages/image.3.2.328_544.60_239/images.html
T: 868350/W: 793871/NW: 74479
*****OK...physrevmaterials.4.054002//image.4.1.328_544.60_230
physrevmaterials.4.054002//image.4.1.328_544.60_230
transforming: image.4.1.328_544.60_230/raw.png
htmlFile papers20210121/physrevmaterials.4.054002/pdfimages/image.4.1.328_544.60_230/images.html
(base) pm286macbook:luke pm286$ 

`

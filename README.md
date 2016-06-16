# TriangulateRT

---

**TriangulateRT** is a tool which supports **Triangulation of Moses Reordering Tables**. Details of Triangulation of reordering tables can be found out in [Triangulation of Reordering Tables: An Advancement Over Phrase Table Triangulation in Pivot-Based SMT](https://www.cse.iitb.ac.in/~pb/papers/icon15-triangulation-reordering.pdf) paper. 

---

## Pre-requisites

- Python 2.7

---

## Usage 

##### Triangulation of Reordering tables

`triangulateRT.sh` performs the entire process for Triangulation of Reordering Tables. This is a single script that should be used to get a Triangulated Reordering Table as output. 

Command:

```sh
$ bash triangulateRT.sh [option]
```

where, `option` can take 3 values as mentioned below

* `0` : for Table Based Approach
* `1` : for Basic Count Based Approach
* `2` : for Count Based Approach with Paraphrases

For e.g. 

```sh
$ bash triangulateRT.sh 0
```
for Table Based Triangulation

##### Count Extraction (Necessary for Count based Triangulation of Reordering Tables)

`countExtractor.sh` extracts various reordering orientation counts for various Source-Target phrase combinations. This script can be used to execute just the **Count Extraction** module of the project. This should not be executed separately if you are executing `triangulateRT.sh`

Command : 

```sh
$ bash countExtractor.sh [option]
```

where, `option` can take 3 values as mentioned below

*	`1` : Preprocessing (Extraction of the Phrase table and Corpus retrieval) **Necessary Step 1**
*	`2` : Calculate reordering counts for various Source-Target phrase combinations **Necessary Step 2**
*	`3` : Extracts counts using modified paraphrase based count extraction approach **Optional**

For e.g. 

```sh
$ bash countExtractor.sh 1
```
for Preprocessing.

---

## Resources Required 

Triangulation of Reordering Tables using any of the 3 approaches mentioned above requires,
* **Triangulated Phrase Table**: A triangulated phrase table can be obtained by using other tools available for Phrase Table Triangulation. It should be in `.gz` format.
* **Source-Pivot and Pivot-Target Reordering Tables**: A Source-Pivot Reordering Table named `reordering-table.wbe-msd-bidirectional-fe.gz` (Default name given to a Reordering Table after MOSES Training) must be put inside a `.tar` file e.g. `source-pivot.tar` and Pivot-Target Reordering Table should also be named as the same and be put in a different `.tar` file e.g. `pivot-target.tar`

In addition to the above mentioned resources, Triangulation using Basic Count Based Approach and Count Based Approach with Paraphrases (options 1 and 2 for `triangulateRT.sh`) require,

* **Source-Target Reordering Table**: A Source-Target Reordering Table named `reordering-table.wbe-msd-bidirectional-fe.gz` must be put inside a `.tar` file e.g. `source-target.tar`
* **Source, Pivot And Target Training Corpus**: Training corpus for all three languages i.e. Source, Pivot and Target Language, must be put in the same folder where the scripts reside i.e. `TriangulateRT/src`.

---

## Authors
- Deepak Patil, CFILT, IIT Bombay
- Harshad Chavan, CFILT, IIT Bombay

---

## Version: 1.0

## Revision Log
1.0 : 16 Jun 2016: Initial version. Supports Basic Table Based, Basic Count Based and Count Based with Paraphrases approaches for Triangulation of Reordering tables.

---

## LICENSE

Copyright Deepak Patil and Harshad Chavan 2016 - present

TriangulateRT is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TriangulateRT is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

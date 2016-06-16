# Copyright Deepak Patil and Harshad Chavan 2016 - present
#
# This file is part of TriangulateRT.
#
# TriangulateRT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# TriangulateRT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#!/bin/bash

path=$PWD

if [ $# -eq 1 ]; then

	if [ $1 -eq 1 ]; then

		read -p "Path for Source-Pivot.tar file : " file1
		read -p "path for Pivot-Target.tar file : " file2
		read -p "path for Source-Target.tar file : " file3

		read -p "Name of the source corpus : " scorpus
		read -p "Name of the pivot corpus : " pcorpus
		read -p "Name of the target corpus : " tcorpus

		if [[ ! ( -f "dump-dictionaries.py" ) ]]; then
			echo "Please add \"dump-dictionaries.py\" to the folder !!"
			return
		fi
		
		START=$(date +%s.%N)

		## Extracting Source-Pivot phrase table

		tar -xf $file1 -C $PWD
		filename=$(basename $file1)
		foldername=${filename%.*}

		echo "######################################################"
		printf "\nExtracting $foldername Reordering table\n"
		echo "######################################################"
		cd $foldername
		gunzip reordering-table.wbe-msd-bidirectional-fe.gz
		mv reordering-table.wbe-msd-bidirectional-fe sptable
		mv sptable $path
		cd -
		rm -rf $foldername

		## Extracting Pivot-target phrase table

		tar -xf $file2 -C $PWD
		filename=$(basename $file2)
		foldername=${filename%.*}

		echo "######################################################"
		printf "\nExtracting $foldername Reordering table\n"
		echo "######################################################"
		cd $foldername
		gunzip reordering-table.wbe-msd-bidirectional-fe.gz
		mv reordering-table.wbe-msd-bidirectional-fe pttable
		mv pttable $path
		cd -
		rm -rf $foldername

		## Extracting Source-target phrase table

		tar -xf $file3 -C $PWD
		filename=$(basename $file3)
		foldername=${filename%.*}

		echo "######################################################"
		printf "\nExtracting $foldername Reordering table\n"
		echo "######################################################"
		cd $foldername
		gunzip reordering-table.wbe-msd-bidirectional-fe.gz
		mv reordering-table.wbe-msd-bidirectional-fe sttable
		mv sttable $path
		cd -
		rm -rf $foldername

		## Replace ||| by | 

		echo "######################################################"
		printf "\nChange field seperator to | : source-pivot table\nVerify the sample:\n\n"
		echo "######################################################"
		sed -i 's/ ||| / | /g' sptable
		head -n 2 sptable

		echo "######################################################"
		printf "\nChange field seperator to | : pivot-target table\nVerify the sample:\n\n"
		echo "######################################################"
		sed -i 's/ ||| / | /g' pttable
		head -n 2 pttable

		echo "######################################################"
		printf "\nChange field seperator to | : source-target table\nVerify the sample:\n\n"
		echo "######################################################"
		sed -i 's/ ||| / | /g' sttable
		head -n 2 sttable


		## Replace [ by ( and ] by )

		echo "######################################################"
		printf "\nRemoval of Square brackets and multiple spaces: source-pivot table\nVerify the sample:\n\n"
		echo "######################################################"
		sed -i 's/\]/)/g;s/\[/(/g' sptable
		sed -i 's/  */ /g' sptable
		head -n 2 sptable

		echo "######################################################"
		printf "\nRemoval of Square brackets and multiple spaces: pivot-target table\nVerify the sample:\n\n"
		echo "######################################################"
		sed -i 's/\]/)/g;s/\[/(/g' pttable
		sed -i 's/  */ /g' pttable
		head -n 2 pttable

		echo "######################################################"
		printf "\nRemoval of Square brackets and multiple spaces: source-target table\nVerify the sample:\n\n"
		echo "######################################################"
		sed -i 's/\]/)/g;s/\[/(/g' sttable
		sed -i 's/  */ /g' sttable
		head -n 2 sttable

		## Replace multiple spaces by single one from all the three corpus

		echo "######################################################"
		printf "\nRemoval of Multiple spaces : source corpus\nVerify the sample:\n\n"
		echo "######################################################"
		sed -i 's/  */ /g' $scorpus
		head -n 4 $scorpus

		echo "######################################################"
		printf "\nRemoval of Multiple spaces : pivot corpus\nVerify the sample:\n\n"
		echo "######################################################"
		sed -i 's/  */ /g' $pcorpus
		head -n 4 $pcorpus

		echo "######################################################"
		printf "\nRemoval of Multiple spaces : Target corpus\nVerify the sample:\n\n"
		echo "######################################################"
		sed -i 's/  */ /g' $tcorpus
		head -n 4 $tcorpus

		
		echo "######################################################"
		printf "\nCreating translation dictionaries using reordering tables\n\n"
		echo "######################################################"
		python dump-dictionaries.py

		END=$(date +%s.%N)
		DIFF=$(echo "($END - $START)" | bc)
		printf "\n<<<<<<<<<<<<<<<<< CONCLUSION >>>>>>>>>>>>>>>>\n\nPreprocessing Completed in $DIFF Seconds \n\n"

	fi

	##################################### CALCULATE THE COUNTS ##################################

	if [ $1 -eq 2 ]; then

		## Check if all the required files exists or not
			
		if [[ ! ( -f "extract-valid-phrases.py" ) ]]; then
			echo "Please add \"extract-valid-phrases.py\" to the folder !!"
			return
		fi
		if [[ ! ( -f "prev-next-phrases.py" ) ]]; then
			echo "Please add \"prev-next-phrases.py\" to the folder !!"
			return
		fi
		if [[ ! ( -f "extract-distinct-valid-translations.py" ) ]]; then
			echo "Please add \"extract-distinct-valid-translations.py\" to the folder !!"
			return
		fi
		if [[ ! ( -f "final-structure.py" ) ]]; then
			echo "Please add \"final-structure.py\" to the folder !!"
			return
		fi
		if [[ ! ( -f "calculate-left-counts.py" ) ]]; then
			echo "Please add \"calculate-counts.py\" to the folder !!"
			return
		fi
		if [[ ! ( -f "calculate-right-counts.py" ) ]]; then
			echo "Please add \"calculate-counts.py\" to the folder !!"
			return
		fi
		

		read -p "Name of the source corpus : " scorpus
		read -p "Name of the pivot corpus : " pcorpus
		read -p "Name of the target corpus : " tcorpus

		START=$(date +%s.%N)
		
		echo "######################################################"
		printf "\nRunning extract-valid-phrases.py\n"
		echo "######################################################"
		python extract-valid-phrases.py $scorpus $pcorpus $tcorpus

		echo "######################################################"
		printf "\nRunning prev-next-phrases.py\n"
		echo "######################################################"
		python prev-next-phrases.py $scorpus $pcorpus $tcorpus

		echo "######################################################"
		printf "\nRunning extract-distinct-valid-translations.py\n"
		echo "######################################################"
		python extract-distinct-valid-translations.py $scorpus $pcorpus $tcorpus

		echo "######################################################"
		printf "\nRunning final-structure.py\n"
		echo "######################################################"
		python final-structure.py $scorpus $pcorpus $tcorpus

		echo "######################################################"
		printf "\nRunning forward counts : calculate-left-counts.py\n"
		echo "######################################################"
		python calculate-left-counts.py $scorpus $pcorpus $tcorpus & pid=$!
		PID_LIST+=" $pid"
	
		echo "######################################################"
		printf "\nRunning Reverse counts : calculate-right-counts.py\n"
		echo "######################################################"
		python calculate-right-counts.py $scorpus $pcorpus $tcorpus & pid=$!
		PID_LIST+=" $pid"

		trap "kill $PID_LIST" SIGINT
		echo "#################################################"
		echo "   LEFT & RIGHT COUNT EXTRACTION IS STARTED"
		echo "#################################################"

		wait $PID_LIST
		
		python non-zero-count-rows.py

		END=$(date +%s.%N)
		DIFF=$(echo "($END - $START)" | bc)
		printf "\n<<<<<<<<<<<<<<<<< CONCLUSION >>>>>>>>>>>>>>>>\n\nExperiment Completed in $DIFF Seconds \n\n"
		
		rm finalLeftCount
		rm finalRightCount 
		rm finalStruct
		rm pttable sptable sttable sample 
		rm *.leftPhrases *.rightPhrases *.validPhraseDict *.validTrans

	fi

	if [ $1 -eq 3 ]; then

		START=$(date +%s.%N)

		echo "######################################################"
		printf "\nRunning Paraphrase based count extraction for LeftCounts\n"
		echo "######################################################"
		python paraphrase-based-count-extract.py 'Left' & pid=$!
		PID_LIST+=" $pid"

		echo "######################################################"
		printf "\nRunning Paraphrase based count extraction for RightCounts\n"
		echo "######################################################"
		python paraphrase-based-count-extract.py 'Right' & pid=$!
		PID_LIST+=" $pid"

		trap "kill $PID_LIST" SIGINT
		echo "#################################################"
		echo "   LEFT & RIGHT COUNT EXTRACTION IS STARTED"
		echo "#################################################"

		wait $PID_LIST

		python non-zero-count-rows-paraphrase.py

		END=$(date +%s.%N)
		DIFF=$(echo "($END - $START)" | bc)
		printf "\n<<<<<<<<<<<<<<<<< CONCLUSION >>>>>>>>>>>>>>>>\n\nExperiment Completed in $DIFF Seconds \n\n"
		
	fi

else
	
	printf "\n<=============== How to run ? ================>\n\n"
	printf "bash countExtractor.sh <opt1>\nWhere,\n\n"
	printf "1 : Preprocessing (Extracting Phrase table, corpus and formatting them)\n"
	printf "2 : Calculate SOURCE-TARGET reordering counts\n"
	printf "3 : Extracts counts using modified paraphrase based count extraction approach\n"
	printf "\n<=============== End of Description ================>\n\n"

fi

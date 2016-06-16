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

	method=$1

	######################### Check if all the required files exists or not ##########################
	
	if [[ ! ( -f "fasterProReordering.py" ) ]]; then
		echo		
		echo "Please add \"fasterProReordering.py\" to the folder !!"
		echo
		exit
	fi

	if [[ ! ( -f "getTriDict.py" ) ]]; then
		echo		
		echo "Please add \"getTriDict.py\" to the folder !!"
		echo		
		exit
	fi

	prune=1

	ptPath=""
	
	if [ $prune -eq 1 ]; then
		read -p "Enter the path of triangulated phrase table (.gz file) : " ptPath
		echo
	fi

	if [ $method -eq 0 ]; then

		read -p "Path for Source-Pivot.tar file : " file1
		read -p "path for Pivot-Target.tar file : " file2
		echo

		if [[ ! ( -f "dump-dictionaries.py" ) ]]; then
			echo "Please add \"dump-dictionaries.py\" to the folder !!"
			return
		fi
		
		echo "######################################################"
		printf "\nNo further user inputs required.\nTriangulated Reordering Table will be stored in this directory with the name \"tri-reord-table-table-based\"\n"
		echo "######################################################"

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
		printf "\nCreating translation dictionaries using reordering tables\n\n"
		echo "######################################################"
		python dump-dictionaries-table-based.py

		END=$(date +%s.%N)
		DIFF=$(echo "($END - $START)" | bc)
		printf "\n<<<<<<<<<<<<<<<<< CONCLUSION >>>>>>>>>>>>>>>>\n\nPreprocessing Completed in $DIFF Seconds \n\n"

		rm -rf pttable sptable 

	fi
	
	if [ $method -eq 0 ]; then
		echo "######################################################"
		printf "Processing..."
		echo "######################################################"		
	else
		echo "######################################################"
		printf "\nPlease wait for providing further inputs.\n"
		echo "######################################################"
	fi
	
	if [ $prune -eq 1 ]; then

		echo "######################################################"
		printf "\nExtracting Triangulated Phrase table table from $ptPath\n"
		echo "######################################################"				
		
		gzip -d < $ptPath > triTable

		echo "######################################################"
		printf "Replacing ||| by |\n"
		echo "######################################################"			
	
		sed -i 's/ ||| / | /g' triTable

		lines=$(cat triTable | wc -l)
		printf "\n Table has $lines lines\n"

		echo "######################################################"
		printf "Building a dictionary from triangulated phrase table "
		echo "######################################################"

		python getTriDict.py triTable triDict $lines
		
		rm -rf triTable

	fi

	if [ $method -eq 0 ];then

		if [[ ! ( -f "sp-trans" ) ]]; then
			echo
			echo "Please add \"sp-trans\" to the folder !!"
			echo		
			exit
		fi

		if [[ ! ( -f "pt-trans" ) ]]; then
			echo		
			echo "Please add \"pt-trans\" to the folder !!"
			echo		
			exit
		fi

		if [[ ! ( -f "tp-trans" ) ]]; then
			echo		
			echo "Please add \"tp-trans\" to the folder !!"
			echo		
			exit
		fi
		
		if [ $prune -eq 1 ]; then
			printf "python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-table-based 1 $method triDict\n"
			python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-table-based 1 $method triDict
		else
			printf "python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-table-based 1 $method\n"
			python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-table-based 1 $method
		fi
		
	fi

	if [ $method -eq 1 ];then

		if [[ ! ( -f "countExtractor.sh" ) ]]; then
			echo
			echo "Please add \"countExtractor.sh\" to the folder !!"
			echo			
			exit
		fi

		if [[ ! ( -f "getTotalCountDict.py" ) ]]; then
			echo
			echo "Please add \"getTotalCountDict.py\" to the folder !!"
			echo			
			exit
		fi		

		bash countExtractor.sh 1
		
		bash countExtractor.sh 2

		if [[ ! ( -f "finalLeftCountDict" ) ]]; then
			echo			
			echo "Please add \"finalLeftCountDict\" to the folder !!"
			echo			
			exit
		fi

		if [[ ! ( -f "finalRightCountDict" ) ]]; then
			echo			
			echo "Please add \"finalRightCountDict\" to the folder !!"
			echo			
			exit
		fi

		echo "######################################################"
		printf "\nNo further user inputs required.\nTriangulated Reordering Table will be stored in the current directory with the name \"tri-reord-table-count-based\"\n"
		echo "######################################################"

		rm -rf finalLeftCountDictShelve totalLeftCountDictShelve finalRightCountDictShelve totalRightCountDictShelve

		printf "\nGenerating Total Count Dictionaries\n"
		python getTotalCountDict.py finalLeftCountDict totalLeftCountDictShelve
		python getTotalCountDict.py finalRightCountDict totalRightCountDictShelve
		printf "\nTotal Count Dictonaries generated in shelve\n"

		if [[ ! ( -f "totalLeftCountDictShelve" ) ]]; then
			echo			
			echo "Please add \"totalLeftCountDictShelve\" to the folder by running \"getTotalCountDict.py\"!!"
			echo			
			exit
		fi

		if [[ ! ( -f "totalRightCountDictShelve" ) ]]; then
			echo			
			echo "Please add \"totalRightCountDictShelve\" to the folder by running \"getTotalCountDict.py\"!!"
			echo			
			exit
		fi

		if [[ ! ( -f "finalLeftCountDictShelve" ) ]]; then
			echo			
			echo "Please add \"finalLeftCountDictShelve\" to the folder by running \"getTotalCountDict.py\"!!"
			echo			
			exit
		fi

		if [[ ! ( -f "finalRightCountDictShelve" ) ]]; then
			echo			
			echo "Please add \"finalRightCountDictShelve\" to the folder by running \"getTotalCountDict.py\"!!"
			echo			
			exit
		fi

		if [ $prune -eq 1 ]; then
			printf "python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-count-based 1 $method triDict\n"
			python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-count-based 1 $method triDict
		else
			printf "python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-count-based 1 $method\n"
			python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-count-based 1 $method
		fi
	
	fi

	if [ $method -eq 2 ];then

		if [[ ! ( -f "countExtractor.sh" ) ]]; then
			echo
			echo "Please add \"countExtractor.sh\" to the folder !!"
			echo			
			exit
		fi

		if [[ ! ( -f "getTotalCountDict-para.py" ) ]]; then
			echo
			echo "Please add \"getTotalCountDict-para.py\" to the folder !!"
			echo			
			exit
		fi
		
		if [[ ( -f "finalLeftCountDict" ) && ( -f "finalRightCountDict" ) ]]; then
			printf "\nWe see that you have already run the code for Basic Count based Approach.\nDo you want to use those already build dictionaries?\n(If you are at all unsure please enter 0)\n0: No\n1: Yes\n"
			read -p "Enter your choice : " choice

			if [ $choice -eq 0 ]; then
				bash countExtractor.sh 1
				bash countExtractor.sh 2
			fi			
		else
			bash countExtractor.sh 1
			bash countExtractor.sh 2
		fi

		if [[ ! ( -f "finalLeftCountDict" ) ]]; then
			echo			
			echo "Please add \"finalLeftCountDict\" to the folder !!"
			echo			
			exit
		fi

		if [[ ! ( -f "finalRightCountDict" ) ]]; then
			echo			
			echo "Please add \"finalRightCountDict\" to the folder !!"
			echo			
			exit
		fi
		
		bash countExtractor.sh 3

		if [[ ! ( -f "paraphrasefinalLeftCountDict" ) ]]; then
			echo			
			echo "Please add \"paraphrasefinalLeftCountDict\" to the folder !!"
			echo			
			exit
		fi

		if [[ ! ( -f "paraphrasefinalRightCountDict" ) ]]; then
			echo			
			echo "Please add \"paraphrasefinalRightCountDict\" to the folder !!"
			echo			
			exit
		fi

		echo "######################################################"
		printf "No further user inputs required.\nTriangulated Reordering Table will be stored in the current directory with the name \"tri-reord-table-para\""
		echo "######################################################"

		printf "\nGenerating Total Count Dictionaries\n"
		python getTotalCountDict-para.py paraphrasefinalLeftCountDict paraphrasetotalLeftCountDictShelve
		python getTotalCountDict-para.py paraphrasefinalRightCountDict paraphrasetotalRightCountDictShelve
		printf "\nTotal Count Dictonaries generated in shelve"

		if [[ ! ( -f "paraphrasefinalLeftCountDictShelve" ) ]]; then
			echo			
			echo "Please add \"paraphrasefinalLeftCountDictShelve\" to the folder by running \"getTotalCountDict-para.py\"!!"
			echo			
			exit
		fi

		if [[ ! ( -f "paraphrasefinalRightCountDictShelve" ) ]]; then
			echo			
			echo "Please add \"paraphrasefinalRightCountDictShelve\" to the folder by running \"getTotalCountDict-para.py\"!!"
			echo			
			exit
		fi

		if [[ ! ( -f "paraphrasetotalLeftCountDictShelve" ) ]]; then
			echo			
			echo "Please add \"paraphrasetotalLeftCountDictShelve\" to the folder by running \"getTotalCountDict-para.py\"!!"
			echo			
			exit
		fi

		if [[ ! ( -f "paraphrasetotalRightCountDictShelve" ) ]]; then
			echo			
			echo "Please add \"paraphrasetotalRightCountDictShelve\" to the folder by running \"getTotalCountDict-para.py\"!!"
			echo			
			exit
		fi


		if [ $prune -eq 1 ]; then
			printf "python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-para 1 $method triDict\n"
			python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-para 1 $method triDict
		else
			printf "python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-para 1 $method\n"
			python fasterProReordering.py sp-trans tp-trans pt-trans tri-reord-table-para 1 $method
		fi
	fi

	rm -rf *-trans
			
else
	
	printf "\n<=============== How to run ? ================>\n\n"
	printf "bash master-triangulator.sh <method-of-triangulation>\nWhere <method-of-triangulation> could be,\n\n"
	printf "0 : Table Based Approach\n"
	printf "1 : Count Based Approach (Basic)\n"
	printf "2 : Count Based Approach (Paraphrase Based)\n"
	printf "\n<=============== End of Description ================>\n\n"

fi

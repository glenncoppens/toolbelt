#!/bin/bash

# clear terminal screen
# clear

# test against input parameters
if [ $# -ne 2 ]
  then
    echo "2 arguments should be applied, 'sourceFilePath' and 'destinationFilePath'" 
    exit 1
fi

# get absolute file paths and cache current directory
sourceFile=$(perl -e 'use Cwd "abs_path";print abs_path(shift)' $1)
destinationFile=$(perl -e 'use Cwd "abs_path";print abs_path(shift)' $2)

# cache paths and filenames
currentPath=$(pwd)
currentPath=${currentPath}
sourceFilePath=$(dirname "$sourceFile")
sourceFilePath=${sourceFilePath}
destinationFilePath=$(dirname "$destinationFile")
destinationFilePath=${destinationFilePath}

sourceFileName=$(basename "$sourceFile")
destinationFileName=$(basename "$destinationFile")

echo 'Source file to be cleaned:'
echo '--->' $sourceFile
echo 'Destination file/location to save the cleaned data file:'
echo '--->' $destinationFile

# start cleanup
echo 'Executing cleanup:'

# use a temp file to manipulate the data
tempFileName='temp_'$sourceFileName
tempFilePath=${sourceFilePath}
tempFile=$tempFilePath'/'${tempFileName}

# create working-file in which we will do the manipulations
cp "$sourceFile" "$tempFile"

# go into directory to manipulate temp file
cd "$tempFilePath"

# print the amount of lines in the source file
amountLinesBefore=$(wc -l "$tempFileName" | awk '{ print $1 }')
amountLinesBefore=$(($amountLines-1))
echo '---> Amount of data lines before cleanup (without headers):' $amountLinesBefore

# replace all \r\n with \n
echo '---> Replacing all \\r\\n with \\n.'
perl -pi'' -e 's/[\r\n]/\n/g' "$tempFileName"

# replace all \r with \n
echo '---> Replacing all \\r with \\n.'
perl -pi'step_carriagelinefeedfilter_*' -e 's/[\r]/\n/g' "$tempFileName"

# replace \n inside column values with ''
echo '---> Replacing \\n in fields with <empty-space>.'
perl -0pi'step_carriagefilter_*' -e 's/"[^\n"]*"(*SKIP)(*F)|("[^"\n]*)\n([^"]*")/$1 $2/g' "$tempFileName"

# replace \n inside column values with ''
# same as previous command, but running it only once does not replace all '\n' characters.
# this seems to be a glitch? That's why it's being run a 2nd time
echo '---> Replacing \\n in fields with <empty-space> (2nd time).'
perl -0pi'step_clean1_*' -e 's/"[^\n"]*"(*SKIP)(*F)|("[^"\n]*)\n([^"]*")/$1 $2/g' "$tempFileName"

# print the amount of lines in the resulting file
amountLinesAfter=$(wc -l "$tempFileName" | awk '{ print $1 }')
amountLinesAfter=$(($amountLines-1))
echo '---> Amount of data lines after cleanup (without headers):' $amountLinesAfter

# copy tempfile to destination file
echo '---> Copying result file to destination folder.'
cp "$tempFileName" "$destinationFile"

# remove tempfiles 'steps_*'
echo '---> Removing temporary files.'
rm -f step_*_"$tempFileName"
rm -f "$tempFileName"

# go back to original path
cd "$currentPath"

echo '---> Result file copied to' \""$destinationFile"\"
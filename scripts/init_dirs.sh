#!/bin/bash
Help()
{
   # Display Help
   echo "Usage: init_dirs [path_to_root_directory]"
   echo
   echo "Creates \"data\" and \"artifacts\" directories."
   echo "In no argument provided, creates them in your current directory."
}

# Get the options
while getopts ":h" option; do
   case $option in
      h) # display Help
         Help
         exit;;
     \?) # incorrect option
         echo "Error: Invalid option"
         exit;;
   esac
done


if [ -z "$1" ]; then
    echo "No argument supplied."
    exit;;
elif [ ! -d "$1" ]; then
    echo Directory "$1" not found.
    exit;;
fi

mkdir -p "$1"/data
mkdir -p "$1"/artifacts/models
mkdir -p "$1"/artifacts/outputs
mkdir -p "$1"/artifacts/plots

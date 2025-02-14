#!/bin/bash

[[ -z $SHA ]] && SHA=${1}
MSG=$(git log -1 --pretty="%B" "${SHA}")

(( LIMIT=4000 ))
(( COUNT=0 ))
for FILE in $(git ls-files --others --deleted --modified); do
  git add "${FILE}"
  (( COUNT=COUNT+1 ))
  if (( COUNT == LIMIT )); then
    git commit -m "PARTIAL COMMIT: ${MSG}"
    COUNT=0
  fi
done

git commit -m "PARTIAL COMMIT: ${MSG}"

# Added scraped data to the repo. Lmao

# [CHANGELOG]
# 🟢 Added 7k+ images
# 🟢 Added a Git Ignore file to ignore the TSV files that's more than the allowed file size for GH (100 MB)
# 🟡 Updated the main "imdb" Jupyter Notebook to now scrape for data using multithreading, along with some major refactoring to classify codes per section and classification.
# 🔴 Removed 2 Jupyter Notebooks due to redundancy.
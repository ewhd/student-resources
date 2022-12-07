#!/bin/bash


# https://unix.stackexchange.com/questions/569361/remove-all-files-directories-except-specified-ones-in-multiple-levels
# https://en.wikibooks.org/wiki/Regular_Expressions/POSIX-Extended_Regular_Expressions
# https://en.wikibooks.org/wiki/Regular_Expressions/Shell_Regular_Expressions
# https://stackoverflow.com/questions/72157108/recursively-delete-all-empty-folders-in-bash


# copies relevant dirs and files
cp -r ~/git-projects/ops-201-guide/curriculum/* .
cp -r ~/git-projects/ops-201-guide/.editorconfig .
cp -r ~/git-projects/ops-201-guide/.eslintrc.json .
cp -r ~/git-projects/ops-201-guide/.gitignore .
cp -r ~/git-projects/ops-201-guide/.markdownlint.json .
cp -r ~/git-projects/ops-201-guide/resources .
cp -r ~/git-projects/ops-201-guide/reference/submission-instructions .



# find class-* ! -regex '\./README.md\|\.challenges/*' -delete    
# find class-* -regextype posix-extended -regex '.*(README).*' -print 
# find . -regextype posix-extended -regex '\./class-..(/README.md)|\./class-../challenges(/.*)' -print 

# removes files and subfolders which aren't for students (but not their containing dirs -- I'm sure I can do this, but regex is hard)
find . -regextype posix-extended -regex '\./class-../DISCUSSION.md|\./class-../challenges/ASSIGNMENT.md|\./class-../facilitator(/.*)|\./class-../lab(/.*)|\./solution(/.*)|\./class-../assets(/.*)|\./class-../solution(/.*)' -delete

# removes all empty dirs
find . -type d -empty -delete
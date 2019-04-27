# Linguistics Final Project

For my final essay in Linguistics, I decided to learn about a topic called phonotactics, which is the study of how sounds can be combined into syllables. Since phonotactics is very rule-based, I thought it would be neat to use the rules write a program that tries to generate random "pseudowords" that sound like English words but aren't.

This program will output a list of "words" in increasing order of "English-ness". The words are actually sequences of phonemes in ARPABET notation, which maps directly to IPA. See the Wikipedia page on ARPABET for instructions on how to read it. Additionally, with each word the program outputs an "English-ness" score and a list of phonotactic rules that the word violated, if any.

### How To Run It

To run this program, you will need Python 3.x and a library called `python-blick` (the secret sauce that makes sure the program doesn't output anything egregiously wrong) which can be installed via pip. Once you have all that, just run the program with `python word.py`.

### Apology

This code is horrible and bad to read and look at. Sorry.

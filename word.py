import random
from itertools import product
from collections import namedtuple
from blick import BlickLoader
from math import exp
from operator import itemgetter

class Syllable(namedtuple("Syllable", "onset nucleus coda")):
	__slots__ = ()

	def __new__(cls, onset, nucleus, coda):
		if type(onset) != tuple:
			onset = tuple(onset.split(" "))
		if len(onset) == 1 and onset[0] == "":
			onset = ()
		if type(coda) != tuple:
			coda = tuple(coda.split(" "))
		if len(coda) == 1 and coda[0] == "":
			coda = ()
		return super().__new__(cls, onset, nucleus, coda)

	def __repr__(self):
		onset =  " ".join(self.onset)
		nucleus = self.nucleus
		coda = " ".join(self.coda)
		return " ".join([onset, nucleus, coda]).strip()

VOWELS = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"}
SHORT_VOWELS = {"AO", "AE", "EH", "IH", "UH", "AH"}

syllables = set()

nucleus1 = VOWELS
onsets1 = {"B", "CH", "D", "DH", "F", "G", "HH", "JH", "K", "L", "M", "N", "P", "R", "S", "SH", "T", "TH", "V", "W", "Y", "Z", "ZH", "B L", "F L", "G L", "K L", "P L", "S L", "S P L", "B R", "D R", "F R", "G R", "K R", "P R", "S K R", "S P R", "S T R", "SH R", "T R", "TH R", "V R", "S F", "S K", "S M", "S N", "S P", "S T", "S W", "S K W"}
syllables |= {Syllable(onset, nucleus, "") for onset, nucleus in product(onsets1, nucleus1)}

nucleus2 = {"UW"}
onsets2 = {"B Y", "F Y", "G Y", "HH Y", "K W", "K Y", "M Y", "P Y", "V Y"}
syllables |= {Syllable(onset, nucleus, "") for onset, nucleus in product(onsets2, nucleus2)}

nucleus3 = VOWELS - {"UH", "UW", "AH", "AW"}
onsets3 = {"D W", "K W", "G W", "P W", "T W", "TH W"}
syllables |= {Syllable(onset, nucleus, "") for onset, nucleus in product(onsets3, nucleus3)}

nucleus4 = VOWELS - {"UH"}
syllables |= {Syllable("", nucleus, "") for nucleus in nucleus4}

codas1 = {"B", "D", "JH", "DH", "F", "G", "K", "L", "M", "N", "P", "R", "S", "SH", "T", "CH", "TH", "V", "Z", "ZH", "L P", "L B", "L T", "L D", "L CH", "L JH", "L K", "R P", "R B", "R T", "R D", "R CH", "R JH", "R K", "R G", "L F", "L V", "L TH", "L S", "L Z", "L SH", "R F", "R V", "R TH", "R S", "R Z", "R SH", "L M", "L N", "R M", "R N", "R L", "M P", "N T", "N D", "N CH", "N JH", "M F", "M TH", "N TH", "N S", "N Z", "F T", "S P", "S T", "S K", "F TH", "P T", "K T", "P TH", "P S", "T TH", "T S", "D TH", "K S", "L P T", "L P S", "L F TH", "L T S", "L S T", "L K T", "L K S", "R M TH", "R P T", "R P S", "R T S", "R S T", "R K T", "M P T", "M P S", "N D TH", "K S TH", "K S T"}
syllables |= {Syllable(syl.onset, syl.nucleus, coda) for syl, coda in product(syllables, codas1)}

additions = set()
for syl in syllables:
	if syl.nucleus in {"AE", "EH", "IH", "UH"}:
		for coda in {"NG", "NG K", "NG TH", "NG K T", "NG K S", "NG K TH"}:
			additions.add(Syllable(syl.onset, syl.nucleus, coda))
syllables |= additions

def getWord():
	rnd = random.randrange(0, 100)
	if rnd < 2:
		num_syls = 5
	elif rnd < 10:
		num_syls = 4
	elif rnd < 30:
		num_syls = 3
	elif rnd < 60:
		num_syls = 2
	else:
		num_syls = 1

	syls = []
	primary_stress = random.choice(list(range(num_syls)))

	for ii in range(num_syls):
		is_first = (ii == 0)
		is_last = (ii == num_syls - 1)
		if is_first:
			prev_syl = None
		else:
			prev_syl = syls[-1]
		if ii == primary_stress:
			stress_lvl = 1
		else:
			stress_lvl = 0
		onset_len, coda_len = getPartLengths(is_first, is_last, prev_syl, stress_lvl)
		syl = getSyllable(onset_len, coda_len, is_first, is_last, stress_lvl)
		syls.append(syl)

	return "  ".join(map(str, syls))

def getPartLengths(is_first, is_last, prev_syl, stress_lvl):
	if is_first:
		rnd = random.randrange(0, 100)
		if rnd < 1:
			onset_length = 3
		elif rnd < 5:
			onset_length = 0
		elif rnd < 55:
			onset_length = 2
		else:
			onset_length = 1
		rnd2 = random.randrange(0, 100)
		if is_last:
			if rnd2 < 20:
				coda_length = 0
			elif rnd2 < 30:
				coda_length = 3
			elif rnd2 < 70:
				coda_length = 1
			else:
				coda_length = 2
		else:
			if rnd2 < 1:
				coda_length = 3
			elif rnd2 < 6:
				coda_length = 2
			else:
				coda_length = 0
	else:
		rnd = random.randrange(0, 100)
		if len(prev_syl.coda) == 3:
			if rnd < 10:
				onset_length = 1
			else:
				onset_length = 0
		elif len(prev_syl.coda) == 2:
			if rnd < 1:
				onset_length = 3
			elif rnd < 20:
				onset_length = 2
			elif rnd < 60:
				onset_length = 1
			else:
				onset_length = 0
		else:
			if rnd < 1:
				onset_length = 0
			elif rnd < 5:
				onset_length = 3
			elif rnd < 20:
				onset_length = 2
			else:
				onset_length = 1
		rnd2 = random.randrange(0, 100)
		if is_last:
			if rnd2 < 20:
				coda_length = 0
			elif rnd2 < 30:
				coda_length = 3
			elif rnd2 < 70:
				coda_length = 1
			else:
				coda_length = 2
		else:
			if rnd2 < 1:
				coda_length = 3
			elif rnd2 < 6:
				coda_length = 2
			else:
				coda_length = 0

	return (onset_length, coda_length)

def getSyllable(onset_len, coda_len, is_first, is_last, stress_lvl):
	possibilities = list(getPossibleSyllables(onset_len, coda_len))
	while len(possibilities) > 0:
		syl = random.choice(possibilities)
		if isValidSyllable(syl, onset_len, coda_len, is_first, is_last, stress_lvl):
			if stress_lvl == 0 and syl.nucleus not in {"AH", "IH", "IY", "UW", "ER", "OW"}:
				stress_lvl = 2
			return syl._replace(nucleus=syl.nucleus+str(stress_lvl))
		else:
			possibilities.remove(syl)


def getPossibleSyllables(onset_len, coda_len):
	for syl in syllables:
		if len(syl.onset) == onset_len and len(syl.coda) == coda_len:
			yield syl

def isValidSyllable(syl, onset_len, coda_len, is_first, is_last, stress_lvl):
	if onset_len == 0 or (is_last and coda_len == 0):
		if syl.nucleus == "UH":
			return False
	if is_last and stress_lvl == 1:
		if syl.nucleus in SHORT_VOWELS:
			return False
	if is_first and syl.onset and syl.onset[0] == "ZH":
		return False
	# if is_last and stress_lvl == 1 and len(syl.coda) == 0:
	# 	return False
	if syl.onset and syl.coda and syl.onset[0] == "S" and not syl.onset[-1] == "T" and syl.nucleus in SHORT_VOWELS:
		if syl.coda[0] == syl.onset[-1]:
			return False
	if stress_lvl != 1 and syl.nucleus not in {"AH", "ER", "IH", "IY", "OW", "UW"}:
		return False
	return True

blick_rater = BlickLoader()
words = []

for i in range(100):
	word = getWord()
	score, rules = blick_rater.assessWord(word.replace("  ", " "), includeConstraints=True)
	score = exp(-score)
	words.append([word, score, rules])

for word, score, rules in sorted(words, key=itemgetter(1)):
	if score > 0.00001:
		print(word, score, rules)
		print()
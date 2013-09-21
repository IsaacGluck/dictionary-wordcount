#!/usr/bin/env python
import argparse, string, os
from operator import itemgetter
from tempfile import TemporaryFile
 

parser = argparse.ArgumentParser()
parser.add_argument("file", type = str, nargs ='*', help = "The file or files (seperated by spaces) whose words will be counted.")
parser.add_argument("-s", "--sort", type = str, help = "Whether to sort the words by MostToLeast, LeastToMost or Alphabetically. The default is MostToLeast.", choices = ['mostfirst','leastfirst', 'alpha'], default = 'mostfirst')
parser.add_argument("-l","--limit", type = int, help = "The number of results shown. The default is all the values.")
args = parser.parse_args()

#If there are more then one files, combine them all into a temp file in a tmp directorty and use the read from that file as the main file
if len(args.file) == 1:
	file = args.file[0]
	text = open(file, 'r')
	modify = text.read()
	text.close()
else:
	temp = TemporaryFile()
	for i in args.file:
		x = open(i, 'r')
		hold = x.read()
		temp.write(hold)
		x.close()
	temp.seek(0)
	modify = temp.read()
	temp.close()


#Remove punctuation, make everyting lowercase, and put the words in a list
modify = modify.translate(string.maketrans("",""), string.punctuation)
modify = string.lower(modify)
words = modify.split()

count = {}
for i in words:
	if i in count:
		words.remove(i)
	else:
		num = 1
		for n in words:
			if n == i:
				num += 1
		count[i] = num

list_count = count.items()

if args.limit == None:
	num = 0
else:
	num = len(list_count) - int(args.limit)


if args.sort == 'mostfirst':
	# Order the word counts from most to least from the list of items
	final = sorted(list_count, key = itemgetter(1), reverse = True)
	while len(final) > num:
		for i in final:
			print i[0] + ':' + str(i[1])
			final.remove(i)
			break
		
	
elif args.sort == 'leastfirst':
	# Order the word counts from least to most from the list of items
	final = sorted(list_count, key = itemgetter(1))
	while len(final) > num:
		for i in final:
			print i[0] + ':' + str(i[1])
			final.remove(i)
			break
else:
	# Order the word counts alphabetically
	final = sorted(list_count, key = itemgetter(0))
	while len(final) > num:
		for i in final:
			print i[0] + ':' + str(i[1])
			final.remove(i)
			break
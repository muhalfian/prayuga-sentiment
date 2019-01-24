from pprint import pprint
import csv

class ConFile(object):
	"""docstring for ConFile"""
	def __init__(self):
		super(ConFile, self).__init__()
		##self.arg = arg
	
	def readFile(self, file, split_arr, ignore_column=None):
		f = open(file,'r');
		i = 0;

		return_arr = {};
		for line in f:
			val = line.split(split_arr);
			if ignore_column is None:
				return_arr[i] = val;
			else:
				val_include = {};
				ii=0;
				for (key,x) in enumerate(val):
					ignore = 1;
					for ignore_i in ignore_column:
						if ignore_i == key:
							ignore = 0;
							break;
					if ignore == 1:
						val_include[ii] = x;
						ii += 1;
				return_arr[i] = val_include;
			i += 1;
		return return_arr;

	def writeFile(self, name_file, data, split):
		with open(name_file, 'w') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',')
			for val in data:
				spamwriter.writerow(val);
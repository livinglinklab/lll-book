def main():
	import pickle
	import pandas as pd
	with open('book.pickle', 'rb') as f:
		obj = pickle.load(f)
	df = pd.DataFrame(obj)
	df.to_csv(r'data.csv')

if __name__ == '__main__':
	main()

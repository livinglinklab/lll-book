def main():
	from grid_divide import main as load_data
	d = load_data()
	import pickle
	with open('dict.pickle', 'wb') as f:
		pickle.dump(d, f)

if __name__ == '__main__':
	main()

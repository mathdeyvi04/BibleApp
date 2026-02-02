all:
	g++ main.cpp -o main -O3 -march=native; ./main; rm main;
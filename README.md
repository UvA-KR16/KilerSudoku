
A) If you are simply here to download some killer sudoku sample files:
Go to ./data and there you will find 1000 examples for size of cage from 2 to 9

B) If you are here to play with killer sudokus using PicoSAT:

1) Set up your computer using the following command:

sudo apt-get install python-setuptools python-dev build-essential
sudo easy_install pip
sudo pip install pycosat

2) (Optioinal)
after installation, please use the following command to test:
https://pypi.python.org/pypi/pycosat
You may choose to also install ipython by:
sudo pip install ipython


3) To run the code, you need to install the following packages:

pip
numpy 
pyparsing
pycosat
satispy (optional)


4) You are ready to solve a killer sudoku!

To run:

python eval.py solver_name subdirectory amount

for example
	solver_name = killerSolver.py
	subdirectory =  news
	amount = 100

i.e. if your data files are unzipped in a folder called data, just run the code as follows:

python eval.py killerSolver.py data 100







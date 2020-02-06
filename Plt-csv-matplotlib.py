import matplotlib.pyplot as plt
import csv

namefile=input("Please enter your filename, without extension, e.g. *.csv: \n ")
plottitle=input("Please enter your system name, or title of your graph: \n")
xxlabel=input("Please enter x label for your plot: \n")
yylabel=input("Please enter y label for your plot: \n")

x=[]
y=[]

with open(''+namefile+'.csv') as csvfile:
	plots=csv.reader(csvfile, delimiter=',')
	for row in plots:
		x.append(int(row[0]))
		y.append(float(row[1]))
plt.plot(x,y,marker='o')
plt.title('Data from CSV file: Dinamica1')

plt.xlabel('Timestep')
plt.ylabel('RMSD')
plt.show()

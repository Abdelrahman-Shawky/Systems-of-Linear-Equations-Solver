import pprint
import tkinter as tk
# import methods as root_finder
# import numpy as np
# import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import filedialog as fd
import methods as methods
import numpy as np
from math import *



class RootCalculator:
    def __init__(self, master):
        # super().__init__(master)
        self.master = master
        # self.myFrame = ttk.LabelFrame(self.master, text="Linear Equations")
        # self.myFrame.pack(fill='both', side='left', anchor="nw", expand='false', padx=10, pady=10)
        self.methodFrame = ttk.LabelFrame(self.master, text="Choose Solving Method")
        self.methodFrame.pack(fill='both', side='top', expand='false', padx=10, pady=10)
        self.tableFrame = ttk.LabelFrame(self.master, text="Systems of Linear Equations")
        self.tableFrame.pack(fill='both', side='bottom', anchor="sw", expand='true', padx=10, pady=10)
        # self.iterationsTable = ttk.Treeview(self.tableFrame)
        # self.resultLabel = ttk.Label(self.tableFrame)
        # self.executionTimeLabel = ttk.Label(self.tableFrame)
        # self.errorLabel = ttk.Label(self.tableFrame)
        self.entries = []
        self.labels = []
        self.initialPoints = []
        self.degreeClicked = tk.StringVar()
        self.resultLabel = ttk.Label(self.tableFrame)
        self.executionTimeLabel = ttk.Label(self.tableFrame)
        self.solveButton = ttk.Button(self.tableFrame, text="Solve", command=lambda:self.solve(int(self.degreeClicked.get())))
        self.createMethodSelector()

    def createMethodSelector(self):
        self.degreeLabel = ttk.Label(self.methodFrame, text="Degree")
        self.degreeLabel.grid(row=0, column=0)
        self.degreeOptions = ["1", "2", "3", "4", "5"]

        self.degreeClicked.set(self.degreeOptions[0])
        self.degreeSelect = tk.OptionMenu(self.methodFrame, self.degreeClicked, *self.degreeOptions)
        self.degreeSelect.grid(row=0, column=1, padx=10, pady=5)
        self.degreeClicked.trace("w", self.changeNumberOfEquations)

        self.methodLabel = ttk.Label(self.methodFrame, text="Method")
        self.methodLabel.grid(row=0, column=2)
        self.options = ["Gaussian-Elimination", "LU Decomposition", "Gaussian-Jordan", "Gauss-Seidel"]
        self.clicked = tk.StringVar()
        self.clicked.set(self.options[0])
        self.clicked.trace("w", self.changeFunction)
        self.methodSelect = tk.OptionMenu(self.methodFrame, self.clicked, *self.options)
        self.methodSelect.grid(row=0, column=3, padx=10, pady=5)

        self.maxIterationsLabel = ttk.Label(self.methodFrame, text="Max Iterations ")
        # self.maxIterationsLabel.grid(row=1, column=0, padx=10, pady=3)
        self.maxIterationsEntry = ttk.Entry(self.methodFrame)
        self.maxIterationsEntry.insert(0, "50")
        # self.maxIterationsEntry.grid(row=1, column=1, padx=10, pady=3)
        self.toleranceLabel = ttk.Label(self.methodFrame, text="Tolerance ")
        # self.toleranceLabel.grid(row=1, column=2, padx=10, pady=3)
        self.toleranceEntry = ttk.Entry(self.methodFrame)
        self.toleranceEntry.insert(0, "0.00001")
        # self.toleranceEntry.grid(row=1, column=3, padx=10, pady=3)
        self.loadFileButton = ttk.Button(self.methodFrame, text="Load File", command=lambda: self.loadFile())
        self.loadFileButton.grid(row=0, column=6, padx=40, pady=20)


    def changeNumberOfEquations(self, *args):
        for entry in self.entries:
            entry.grid_forget()
        for label in self.labels:
            label.grid_forget()
        for entry in self.initialPoints:
            entry.grid_forget()
        self.entries.clear()
        self.labels.clear()
        self.initialPoints.clear()
        self.solveButton.grid_forget()
        self.resultLabel.grid_forget()
        self.executionTimeLabel.grid_forget()

        if self.clicked.get() == "Gauss-Seidel":
            self.initialLabel = ttk.Label(self.methodFrame, text="Initial Points")
            self.initialLabel.grid(row=1, column=0, padx=10, pady=3)
            self.labels.append(self.initialLabel)
            flag = 0
            for i in range(2 * int(self.degreeClicked.get())):
                if flag == 0:
                    self.initialPointLabel = ttk.Label(self.methodFrame, text="x{}".format(i // 2 + 1))
                    self.initialPointLabel.grid(row=2, column=i, padx=10, pady=3)
                    self.labels.append(self.initialPointLabel)
                    flag = 1
                else:
                    self.initialPointEntry = ttk.Entry(self.methodFrame, width="10")
                    self.initialPointEntry.insert(0, "0")
                    self.initialPointEntry.grid(row=2, column=i, padx=10, pady=3)
                    self.initialPoints.append(self.initialPointEntry)
                    flag = 0

        for i in range(int(self.degreeClicked.get())):
            flag = 0
            for j in range(2 * int(self.degreeClicked.get())):
                if flag == 0:
                    self.xLabel = ttk.Label(self.tableFrame, text="x{}".format(j // 2 + 1))
                    self.xLabel.grid(row=i, column=j, padx=5, pady=5)
                    self.labels.append(self.xLabel)
                    flag = 1
                else:
                    self.xEntry = ttk.Entry(self.tableFrame, width=10)
                    self.xEntry.grid(row=i, column=j, padx=5, pady=5)
                    self.entries.append(self.xEntry)
                    flag = 0
            self.equalLabel = ttk.Label(self.tableFrame, text="=")
            self.equalLabel.grid(row=i, column=j + 1, padx=5, pady=5)
            self.labels.append(self.equalLabel)
            self.equalEntry = ttk.Entry(self.tableFrame, width=10)
            self.equalEntry.grid(row=i, column=j + 2, padx=5, pady=5)
            self.entries.append(self.equalEntry)

        self.solveButton.grid(row=i + 1, column=0, columnspan=20, padx=5, pady=5, sticky=tk.W + tk.E)

    def solve(self, n):
        entriesList = []
        initialList = []
        for i in range(len(self.entries)):
            entriesList.append(self.entries[i].get())
        for i in range(len(self.initialPoints)):
            initialList.append(self.initialPoints[i].get())

        result = methods.selectMethod(self.clicked.get(), entriesList, n, initialList, float(self.toleranceEntry.get()), int(self.maxIterationsEntry.get()))
        x = result['result']
        resultString = " "
        for i in range(n):
            resultString += 'x%d = %0.4f' % (i, x[i]) + '\t'
            # print('X%d = %0.2f' % (i, x[i]), end='\t')
        self.resultLabel['text'] = resultString
        self.resultLabel.grid(row=20, column=0, columnspan=20, padx=5, pady=5, sticky=tk.W + tk.E)
        if self.clicked.get() == "Gauss-Seidel":
            self.executionTimeLabel['text'] = "Execution time: " + result['execution_time'] + "s"
            self.executionTimeLabel.grid(row=21, column=0, columnspan=20, padx=5, pady=5, sticky=tk.W + tk.E)


    def changeFunction(self, *args):
        self.changeNumberOfEquations()
        if self.clicked.get() == "Gauss-Seidel":
            self.maxIterationsLabel.grid(row=3, column=0, padx=10, pady=3)
            self.maxIterationsEntry.grid(row=3, column=1, padx=10, pady=3)
            self.toleranceLabel.grid(row=3, column=2, padx=10, pady=3)
            self.toleranceEntry.grid(row=3, column=3, padx=10, pady=3)
        else:
            self.maxIterationsLabel.grid_forget()
            self.maxIterationsEntry.grid_forget()
            self.toleranceLabel.grid_forget()
            self.toleranceEntry.grid_forget()



    def loadFile(self):
        file_name = fd.askopenfilename(title="Select A File", filetypes=[("txt files", ".txt")])
        file = open(file_name, 'r')
        file_input = []
        for line in file:
            file_input.append(line.rstrip("\n"))

        numOfEquations = int(file_input[0])
        self.degreeClicked.set(numOfEquations)
        self.clicked.set(file_input[1])
        a = np.ones((numOfEquations, numOfEquations + 1))

        for i in range(numOfEquations):
            line = file_input[2+i].split()
            j = 0
            print(line)
            for x in line:
                if x == '-':
                    a[i][j] = -1
                    continue
                elif x == '+':
                    a[i][j] = 1
                    continue
                if j == numOfEquations:
                    a[i][j] *= -1
                    a[i][j] *= int(x)
                else:
                    value = x.split("*")
                    a[i][j] *= float(value[0])
                    j += 1
        current = np.zeros(numOfEquations)
        if file_input[1] == "Gauss-Seidel":
            initials = file_input[len(file_input)-1].split()
            count = 0
            for x in initials:
                current[count] = float(x)
                count += 1
            for i in range(numOfEquations):
                self.initialPoints[i].insert(0, current[i])

        count = 0
        for i in range(numOfEquations):
            for j in range(numOfEquations + 1):
                self.entries[count].insert(0, a[i][j])
                count += 1

        print(current)
        pprint.pprint(a)
        file.close()


root = tk.Tk()
root.title("Solving Linear Systems")
root.geometry('1000x500')
s = ttk.Style()
s.theme_use('xpnative')
rootCalculator = RootCalculator(root)
root.mainloop()

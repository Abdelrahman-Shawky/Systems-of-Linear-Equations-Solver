import tkinter as tk
# import methods as root_finder
# import numpy as np
# import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import filedialog as fd
import methods as methods
from math import *



class RootCalculator:
    def __init__(self, master):
        # super().__init__(master)
        # self.self=master
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
        self.degreeClicked = tk.StringVar()
        self.resultLabel = ttk.Label(self.tableFrame)
        self.solveButton = ttk.Button(self.tableFrame, text="Solve", command=lambda:self.solve(int(self.degreeClicked.get())))
        # self.createButton(2)
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
        self.options = ["Gaussian-Elimination", "LU decomposition", "Gaussian-Jordan", "Gauss-Seidel"]
        self.clicked = tk.StringVar()
        self.clicked.set(self.options[0])
        # self.clicked.trace("w", self.changeEntry)
        self.methodSelect = tk.OptionMenu(self.methodFrame, self.clicked, *self.options)
        self.methodSelect.grid(row=0, column=3, padx=10, pady=5)
        self.lowerBoundLabel = ttk.Label(self.methodFrame, text="x (lower bound) ")
        self.lowerBoundLabel.grid(row=1, column=0, padx=10, pady=3)
        self.lowerBoundEntry = ttk.Entry(self.methodFrame)
        self.lowerBoundEntry.grid(row=1, column=1, padx=10, pady=3)
        self.upperBoundLabel = ttk.Label(self.methodFrame, text="x (upper bound) ")
        self.upperBoundLabel.grid(row=1, column=2, padx=10, pady=3)
        self.upperBoundEntry = ttk.Entry(self.methodFrame)
        self.upperBoundEntry.grid(row=1, column=3, padx=10, pady=3)
        self.maxIterationsLabel = ttk.Label(self.methodFrame, text="Max Iterations ")
        self.maxIterationsLabel.grid(row=2, column=0, padx=10, pady=3)
        self.maxIterationsEntry = ttk.Entry(self.methodFrame)
        self.maxIterationsEntry.insert(0, "50")
        self.maxIterationsEntry.grid(row=2, column=1, padx=10, pady=3)
        self.toleranceLabel = ttk.Label(self.methodFrame, text="Tolerance ")
        self.toleranceLabel.grid(row=2, column=2, padx=10, pady=3)
        self.toleranceEntry = ttk.Entry(self.methodFrame)
        self.toleranceEntry.insert(0, "0.00001")
        self.toleranceEntry.grid(row=2, column=3, padx=10, pady=3)
        self.loadFileButton = ttk.Button(self.methodFrame, text="Load File", command=lambda: self.loadFile())
        self.loadFileButton.grid(row=1, column=6, padx=40, pady=20)
        self.singleMode = tk.IntVar()
        single_mode_check_box = ttk.Checkbutton(self.methodFrame, text="Single Mode", variable=self.singleMode)
        single_mode_check_box.grid(row=2, column=6, padx=40, pady=20)

    def changeNumberOfEquations(self, *args):
        for entry in self.entries:
            entry.grid_forget()
        for label in self.labels:
            label.grid_forget()
        self.entries.clear()
        self.labels.clear()
        self.solveButton.grid_forget()

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
        for i in range(len(self.entries)):
            entriesList.append(self.entries[i].get())

        x = methods.selectMethod(self.clicked.get(), entriesList, n, float(self.toleranceEntry.get()), int(self.maxIterationsEntry.get()))

        # print(x)
        # Displaying solution
        print('\nRequired solution is: ')
        resultString = " "
        for i in range(n):
            resultString += 'x%d = %0.4f' % (i, x[i]) + '\t'
            # print('X%d = %0.2f' % (i, x[i]), end='\t')
        self.resultLabel['text'] = resultString
        self.resultLabel.grid(row=20, column=0)


    def changeEntry(self, *args):
        if self.clicked.get() == "Fixed Point" or self.clicked.get() == "Newton Raphson":
            self.upperBoundEntry.delete(0, tk.END)
            self.upperBoundEntry.insert(0, "0")
            self.upperBoundEntry.grid_forget()
            self.upperBoundLabel.grid_forget()
        else:
            self.upperBoundLabel.grid(row=1, column=2, padx=10, pady=5)
            self.upperBoundEntry.grid(row=1, column=3, padx=10, pady=5)

    def loadFile(self):
        file_name = fd.askopenfilename(title="Select A File", filetypes=[("txt files", ".txt")])
        file = open(file_name, 'r')
        file_input = []
        for line in file:
            file_input.append(line.rstrip("\n"))
        self.functionEntry.delete(0, tk.END)
        self.lowerBoundEntry.delete(0, tk.END)
        self.upperBoundEntry.delete(0, tk.END)
        if file_input[1] == "Bisection" or file_input[1] == "False-Position" or file_input[1] == "Secant":
            self.clicked.set(file_input[1])
            self.functionEntry.insert(0, file_input[0])
            self.lowerBoundEntry.insert(0, file_input[2])
            self.upperBoundEntry.insert(0, file_input[3])

            if len(file_input) == 6:
                self.maxIterationsEntry.delete(0, tk.END)
                self.maxIterationsEntry.insert(0, file_input[4])
                self.toleranceEntry.delete(0, tk.END)
                self.toleranceEntry.insert(0, file_input[5])
            else:
                self.functionEntry.insert(0, "Error Reading File")
        elif file_input[1] == "Fixed Point" or file_input[1] == "Newton Raphson":
            self.functionEntry.insert(0, file_input[0])
            self.clicked.set(file_input[1])
            self.lowerBoundEntry.insert(0, file_input[2])
            if len(file_input) == 5:
                self.maxIterationsEntry.delete(0, tk.END)
                self.maxIterationsEntry.insert(0, file_input[3])
                self.toleranceEntry.delete(0, tk.END)
                self.toleranceEntry.insert(0, file_input[4])
            else:
                self.functionEntry.insert(0, "Error Reading File")
        else:
            self.functionEntry.insert(0, "Error Reading File")
        file.close()


root = tk.Tk()
root.title("Solving Linear Systems")
root.geometry('1300x700')
s = ttk.Style()
s.theme_use('xpnative')
rootCalculator = RootCalculator(root)
root.mainloop()

#!pip install prettytable
import math
import xlrd
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde
from numpy import linspace
from pylab import plot
import pandas as pd
import numpy as np
from prettytable import PrettyTable
import matplotlib.pyplot as plt

class Lab1M:
    def __init__(self, Array):                     # ��������� ������ ����� ��� �������������
        self.N=len(Array)                          # �������� ���������� ���������
        print ("Num of elements: " + str(self.N))  # ������� ��� ����� �� �����
        self.m = 1 + math.log2(self.N)             # ����������� ���������� �����
        print ("m =  " + str(self.m))
        self.m = math.ceil(self.m)
        print ("Num of groups: " + str(self.m))    # ������� ���������� ����� �� �����
        self.Group(self.N, self.m)                 # �������� ����� Group ��� ���������� 1 �������
        
        self.Kernel()                              # ��������� ����� Kernel ��� ���������� 2 �������
        
        self.CharactTable(self.N, self.m)          # ��������� ����� CharactTable ��� ���������� 3 �������
        
    def Group(self, N, m):                         # ����� Group ����������� ��� ����������� ��������� ��� ���������� ���������� � ������� ������� ������ ���������
        self.Del = (max(Array) - min(Array))/(1 + math.log2(self.N))     # ����������� ��������
        self.Del = self.Rounding(self.Del)         # ��������� ���������� ��������
        print("Gap is " + str(self.Del))           # ������� ��� �� �����
        
        self.C = []
        self.C.append(min(Array))                  # ��������� ������ ������ ������ �������� ����� ����������� ����� � �������
        print ("C0 is " + str(self.C[0]))          # ������� ��� �� �����
        self.i = 0                                 
        while self.i < m - 1:                          # ��������� ����� ���������� ���������
            self.C.append(self.Rounding(self.Borders(self.C[self.i], self.Del)))          # � ������� ������ Borders ������� ��������� �������
            print ("C" + str(self.i+1) + " is " + str(self.C[self.i+1]))                  # ������� � �� �����
            self.i=self.i+1
        self.C.append(max(Array))                  # ��������� ������ ������ ��������� �������� ����� ������������ ����� � �������
        print ("C9 is " + str(self.C[len(self.C) - 1]))          # ������� ��� �� �����
        
        self.CA = []
        self.i = 0
        while self.i < m:                                                                              # ��������� ������ �������� � ���������
            self.CA.append(self.Rounding(self.Average_in_gap(self.C[self.i], self.C[self.i+1])))                      # c ������� ������ Average_in_gap ������� ������� � ��������� ��� �������
            print ("Average " + str(self.i) + " - " + str(self.i+1) + " is " + str(self.CA[self.i]))   # ������� ������������ ����� �� �����
            self.i=self.i+1
        
        self.F = []
        self.i = 0
        while self.i < m:                                                                   # ��������� ������ ���������� ��������� � ������ ������
            self.F.append(self.Num_elmnts_in_group(self.C[self.i], self.C[self.i + 1]))     # � ������� ������ Num_elements_in_group �������� ������� ��� ������ ������
            print("Num elements in group " + str(self.i+1) + " is " + str(self.F[self.i]))  # ������� �� ����� ��������
            self.i=self.i+1
            
        self.RelF = []
        self.i = 0
        for self.i in self.F:            # ��������� ������ ������������� ����������� ��� ������ ������
            self.RelF.append(self.Rounding(self.i / N)) # ������� ��� �� �������
        print ("Relative frequency is ") # ������� �� �����
        print (self.RelF)
        
        self.GA = []
        self.i = 0
        while self.i < m:                                                              # ��������� ������ �������� �� ������
            self.GA.append(self.Rounding(self.Group_average(self.C[self.i], self.C[self.i + 1])))     # ������� ������� ��� ������ ������ � ������� ������ Group_average
            print("Average in group " + str(self.i+1) + " is " + str(self.GA[self.i])) # ������� ���������� �������� �� �����
            self.i = self.i+1       
        
        self.NumOfGroup = []
        self.Yoha = 0
        while self.Yoha < m:                                                # ������ ������ ����� ��������� � ������
            self.NumOfGroup.append(self.Yoha+1)                             
            self.Yoha = self.Yoha + 1
        self.TableCreator(self.C, self.CA, self.GA, self.F, self.RelF, m)   # ������� ������ � ������� � ������� ������ TableCreator
        
        self.PercentRelF = []
        self.K = 0
        for self.K in self.RelF:                                              # ������� ���������� ���� ������������� �����������
            self.PercentRelF.append(self.K*100)                               
            
        self.K = 0
        self.Den = []
        for self.K in self.RelF:                   
            self.Den.append(self.K/self.Del)       
        self.K = 0
        self.Inter = []
        while self.K < m:                                                                          # ������ ������ ���������� ��� ������ �� �� �����������
            self.Inter.append("[" + str(self.C[self.K]) + ';' + str(self.C[self.K + 1]) + ")")     
            self.K = self.K + 1
            
        print ("Histogramma of frequency")
        self.Histogramma1(self.NumOfGroup, self.F)                    # �������� ������ ����������� � ������� ������ Histogramma1
        print ("Histograma of relative frequency in %")
        self.Histogramma2(self.NumOfGroup, self.PercentRelF)           # �������� ������ ����������� � ������� ������ HIstogramma2
        print ("Histograma of estimation of the probability density")  
        self.Histogramma3(self.Inter, self.Den)                         # �������� ������ ����������� � ������� ������ Histogramma 3
        
        return 0
    
    def Rounding(self, X):                           # �����, ����������� ��������� ����� �� �������� ����������
        return round(X,3)
    #  if (X - math.floor(X) >= 0.5):        
      #      return (math.ceil(X))
      #  else:
       #     return (math.floor(X))
        
    def Borders(self, C1, Del):                   # ���� ����������� �������� ������ �������
        return (C1 + Del)
    
    def Average_in_gap(self, C1, C2):             # �����, ����������� �������� ������� � ���������
        return ((C1+C2)/2)
    
    def Num_elmnts_in_group(self, C1, C2):        # �����, ����������� �������� ���������� �������� � ������ ������
        self.Count=0
        for self.K in Array:
            if ((self.K >= C1) and (self.K < C2)) or ((C2 == 24.8) and (self.K >= C1) and (self.K <= C2)):
                self.Count = self.Count+1   
        return self.Count
    
    def Group_average(self, C1, C2):              # �����, ����������� �������� ������� �� ������
        self.K = 0
        self.Count = 0
        self.Sum = 0
        for self.K in Array:                       
            if (self.K >= C1) and (self.K < C2):   
                self.Sum = self.Sum + self.K       
                self.Count = self.Count+1
        return (self.Sum/self.Count)
        
    def TableCreator(self, C, CA, GA, F, RelF, m):           # ����� ����������� ������� ������� � ������� ���������� PrettyTable
        self.th = ['# of group', 'Interval', 'Interval average', 'Group average', 'Frequency', 'Relative frequency']      # ���������� ����� ����� �������
        self.DataArray = []
        self.CC = 0
        while self.CC < m:        # ��������� ������� �������
            self.DataArray.extend([self.CC+1,"[" + str(C[self.CC]) + ";" + str(C[self.CC+1]) + ")", CA[self.CC], GA[self.CC], F[self.CC], RelF[self.CC]])
            self.CC=self.CC+1
        self.col = len(self.th)
        self.table = PrettyTable(self.th)
        self.td = self.DataArray
        while self.td:                                 # ������ ������� 
            self.table.add_row(self.td[:self.col])
            self.td = self.td[self.col:]
        print (self.table)                              # ������� � �� �����
        return 0
    
    def Histogramma1(self, Arr1, Arr2):                  # ����� ����������� ���������� ������ �����������
        plt.title("Histogramma of frequency")
        plt.xlabel("# of group")
        plt.ylabel("Frequency")
        plt.bar(Arr1, Arr2, width = 0.1, color = 'blue')   # �������� ������ ��������� ������� �������� 0.1, ���� �������
        plt.show()
        return 0
    
    def Histogramma2(self, Arr1, Arr2):                    # ����� ����������� �������� ������ �����������
        plt.title("Histograma of relative frequency in %")
        plt.xlabel("# of group")
        plt.ylabel("Relative frequency")
        plt.bar(Arr1, Arr2)
        plt.show()
        return 0
    
    def Histogramma3(self, Arr1, Arr2):                        # ����� ����������� �������� ������ �����������
        plt.figure(figsize=(16, 9), constrained_layout=True)    # ����������� ������ ����������� ��� ��������� ���������
        plt.title("Histograma of estimation of the probability density")
        plt.xlabel("Interval")
        plt.ylabel("Dencity")
        plt.bar(Arr1, Arr2, width = 1)                        # ���������� ��������� �����������: ������� �������� - 1
        plt.show()
        return 0
    
    def Kernel(self):                                     # ����� ����������� �������� ������� ������ ��������� �����������
        AH = pd.read_csv('Auto.txt', sep = "\t", header = 0, index_col = False)       #  ��������� ������ ��� ���������� �������
        AH1 = np.asarray(AH['Acceleration'])
        my_density1 = gaussian_kde(AH1)
       #  my_density2 = gaussian_kde(AH1, bw_method = 1) 
        my_density3 = gaussian_kde(AH1, bw_method = 0.1) 
        x = linspace(min(AH['Acceleration']), max(AH['Acceleration']), 100) 
        print ("Kernel Density Estimation:")
        plot(x, my_density1(x), 'r')
        plot(x, my_density3(x), 'r')               # ������� ������ �� �����
        return 0
    
    def CharactTable(self, N, m):                          # �����, ����������� �������� ������� ���������� ������������� �������������
        self.summator = 0
        for self.e in Array:                                  # �������� ��� ����������� �������������� �� ��������� ��������
            self.summator = self.summator + self.e
        self.X_Mid = self.summator / N
        self.Med = np.percentile(Array, 50)
        self.R = max(Array) - min(Array)
        self.IQR = np.percentile(Array, 75) - np.percentile(Array, 25)
        self.summator = 0
        self.e = 0
        for self.e in Array:
            self.summator = self.summator + abs(self.e - self.X_Mid)
        self.D_Mid = self.summator / N
        self.summator = 0
        self.e = 0
        for self.e in Array:
            self.summator = self.summator + (self.e - self.X_Mid)**2
        self.S = math.sqrt(self.summator / (N - 1))
        self.Disp = self.S * self.S
        self.V = (self.S / self.X_Mid) * 100
        self.th = ['Sample characteristics', 'Values']                    #
        self.td = ['Mean', self.Rounding(self.X_Mid), 'Median', self.Rounding(self.Med), 'Swipe variation', 
                   self.Rounding(self.R), 'Quartile scope', self.Rounding(self.IQR), 'Average linear deviation', 
                   self.Rounding(self.D_Mid), 'Mean square deviation', self.Rounding(self.S), 'Dispersion', 
                   self.Rounding(self.Disp), 'The coefficient of variation', self.Rounding(self.V)]
        self.col = len(self.th)
        self.table = PrettyTable(self.th)
        while self.td:
            self.table.add_row(self.td[:self.col])
            self.td = self.td[self.col:]
        print (self.table)                             # ������� ���������� ������� �� �����
        return 0
        
		
rb=xlrd.open_workbook('auto.xls' ,formatting_info=True)               #��������� ������ �� ����� Excel
sheet=rb.sheet_by_index(0)                # �������� ���� � �����
Array=[]
i=0
for i in range(sheet.nrows):              # ������� ���������� �� ����� ������ � ������ Array
    row = sheet.row_values(i)
    if i>1:
        Array.append(row[1])
print(Array)
print ("Min " + str(min(Array)))          # ������� ����������� �������� ��������� �� �������
print ("Max " + str(max(Array)))          # ������� ������������ �������� ��������� �� ������ 



Lab1M(Array)                              # �������� ����� Lab1M � ������� � ����� �������������� ������
from tkinter import *
import time
from math import log
from random import randrange

def duplicate(lst):
    duplicateList = []
    index = 0
    for i in lst:
        for j in range(index + 1, len(lst)):
            if i == lst[j]:
                duplicateList.append(i)
        index += 1
    return duplicateList

def testrun(fct, n, color, runs):
    'rest-run fct on list of n elements for runs runs'

    t = 0
    for i in range(0,runs):
        rand_lst = [randrange(1, 101) for k in range(n)]
        t1 = time.time()
        fct(rand_lst)
        t2 = time.time()
        t += t2-t1
    return (n,t/runs, color)

def plot_data(data, name):
    'plot data for name'
    
    T = Tk()
    T.title('Running times plot for ' + name)
    Button(T, text='Quit', command=T.quit).pack()

    cv = Canvas(T,width=510, height=410, bg='white')
    cv.pack()
    cv.create_line(10,400,500,400, width=1)
    cv.create_line(10,400,10,0, width=1)

    maxn=0
    maxt=0
    for (n,t,color) in data:
        if n >= maxn:
            maxn = n
        if t >= maxt:
            maxt = t
    for (n,t,color) in data:
        x,y= 10+(n/maxn)*490,400-(t/maxt)*380
        cv.create_oval(x-3,y-3,x+3,y+3,width=1, outline='black', fill=color)
    T.mainloop()
    
def run_analysis():
    'run analysis for duplicate function'

    data = []
    for n in range(10,110,10):
        print(n)
        data.append(testrun(duplicate, n, 'red',10**4))

    plot_data(data,'Duplicate')
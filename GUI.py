import tkinter as tk
from tkinter import filedialog
from tkinter import StringVar
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
#import csv
#from tables import createStandardTable as cst
import os


def select_active_items():
    selected_list = []
    for item in curitem:
        selected_list.append(trv.item(item)['values'])
    print(selected_list)


def selectItem(a):
    global curitem
    curitem = trv.selection()
    for item in curitem:
        print(trv.item(item))

def running_analysis():
    print("button clicked with", filename)
    print("sh runningscript.sh {}".format(filename[0]))
    print("analyis status: ", haplotype_var.get())
    if haplotype_var.get() == 1:
        haplonumber = entry.get()
        if len(filename) > 1:
    # change to import maybe instead of different program
            print("python3 Haplotype_file_analysis.py '{}'".format(filename))
            os.system("python3 Haplotype_file_analysis.py '{}' {}".format(filename, haplonumber))
    os.system("sh /Users/iwanhidding/PycharmProjects/Internship-Helsinki/runningscript.sh {}".format(filename[0]))
    #path.os(runstuff)


def on_button_click():
    #filename = entry.get()
    running_analysis()


def UploadAction(event=None):
    global filename
    filename = filedialog.askopenfilenames()
    #filelabelname.set('Selected file: {}'.format(filename))
    file_label.configure(text='Selected file: {}'.format(filename))
    #cst(filename, window).pack()
    print('Selected:', filename)

def Load_UploadAction(event=None):
    #global filename
    analysis_file = filedialog.askopenfilename()
    #filelabelname.set('Selected file: {}'.format(filename))
    #file_label.configure(text='Selected file: {}'.format(filename))
    print('checkers')
    print(analysis_file)
    df = pd.read_csv(analysis_file, sep='\t', header=0)
    # global rows
    rows = df[['#CHROM', 'POS', 'REF', 'ALT']]
    print(rows)
    update_table(rows)
    #cst(open(analysis_file), window).pack()
    print('Selected:', analysis_file)


def update_table(rows):
    for index, row in rows.iterrows():
        # Expand on this with other columns later
        # add a scrollbar and a search option, coding vs non-coding
        trv.insert('', 'end', values=[row['#CHROM'], row['POS'], row['REF'], row['ALT']])

#root = tk.Tk()

window = tk.Tk()
window.title("Iwan's analysis pipeline")

wrapper1 = LabelFrame(window, text="Pathogenicity analysis")
wrapper2 = LabelFrame(window, text="Additional analysis")


wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)


greeting = tk.Label(wrapper1, text="Put your vcf down here:")


global haplotype_var
haplotype_var = IntVar()

#filelabelname = tk.StringVar()
#filelabelname.set("No file selected")
#print(filelabelname)
entry = tk.Entry(wrapper1)
file_label = tk.Label(wrapper1, text="No file selected")
haplolabel = tk.Label(wrapper1, text="Enter the required number of matching variants for haplotype analysis:")
#print('this isnt it')


button = tk.Button(
    wrapper1,
    text="Start analysis!",
    command=on_button_click
)

button_2 = tk.Button(wrapper1, text='Open', command=UploadAction)
button_3 = tk.Button(wrapper2, text='Open', command=Load_UploadAction)
button_selection = tk.Button(wrapper2, text='confirm selection', command=select_active_items)
haplocheckmark = Checkbutton(wrapper1, text="Haplotype Analysis", variable=haplotype_var)

trv = ttk.Treeview(wrapper2, columns=(1,2,3,4), show="headings", height="10")


greeting.pack()
button_2.pack()
file_label.pack()
haplocheckmark.pack()
haplolabel.pack()
entry.pack()
button.pack()
button_3.pack()
trv.pack()
button_selection.pack()
trv.heading(1, text="chr")
trv.heading(2, text="pos")
trv.heading(3, text="ref")
trv.heading(4, text="alt")
trv.bind('<ButtonRelease-1>', selectItem)



#button_4 = tk.Button(window, text='Open', command=UploadAction)
#f = open("output_annotation/clinpred_pred.txt")

#print(f)
#newtable = cst(f, window)

#newtable.pack()
# on button click run runningscript with the filename from the entry pack
window.mainloop()


# turn to grid over pack to allow better visualisation, add scrolling, maybe less detials


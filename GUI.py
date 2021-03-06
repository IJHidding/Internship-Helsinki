import tkinter as tk
from tkinter import filedialog
from tkinter import StringVar
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import os
from proteinplotter import plotprotein
from tables import get_sequence, one_of_each
import tensorflow as tf


def run_protein_analysis():
    biglist_of_everything = []
    for index, row in df.iterrows():
        print(row['#CHROM'], row['POS'], row['ALT'], row['REF'])
        variant_location_list, sequence_list, variant_sequence_list = get_sequence([row['#CHROM'], row['POS']], row['ALT'], row['REF'])
        biglist_of_everything.append([variant_location_list, sequence_list, variant_sequence_list])
    df['protein_analysis'] = biglist_of_everything
    rows = df[['#CHROM', 'POS', 'REF', 'ALT', 'PREDICTIONSCORE', 'protein_analysis']]
    print(rows)
    update_table(rows, 2)


def select_active_items():
    global sequence_location
    #results_storage_dict = {}
    selected_list = []
    for item in curitem:
        selected_list.append(trv.item(item)['values'])
    print(selected_list)
    for item in selected_list:
        print(item)


        # protein plotter here instead
        #results_storage_dict[selection[:2]] = [variant_location_list, sequence_list, variant_sequence_list]
        #listofsequences.append(sequences)
        #listof_variant_sequences(variant_sequence)

    #print(listofsequences)

    #get_sequence("\t".join(selected_list))


def get_plot(sequence):
    def get_model():
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(3000,)),
            tf.keras.layers.Dense(5000, activation='relu'),
            tf.keras.layers.Dense(3000, activation='sigmoid')
        ])
        model.compile(loss='binary_crossentropy', optimizer='adam')
        return model
    if len(sequence) > 3000:
        print("protein too big, cant analyse")
    else:
        model = get_model()
        model.load_weights('./models/binding.sav')
        other_binding = model.predict(one_of_each(sequence))
        model = get_model()
        model.load_weights('./models/dna_binding.sav')
        dna_binding = model.predict(one_of_each(sequence))
        model = get_model()
        model.load_weights('./models/metal.sav')
        metal_binding = model.predict(one_of_each(sequence))
        model = get_model()
        model.load_weights('./models/Act_sites.sav')
        active = model.predict(one_of_each(sequence))
        plot_image = plotprotein(sequence, other_binding, dna_binding, metal_binding, active, sequence_location)
        return plot_image


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
    global df
    analysis_file = filedialog.askopenfilename()
    print(analysis_file)
    df = pd.read_csv(analysis_file, delim_whitespace=True, header=0)
    # global rows
    # add score
    rows = df[['#CHROM', 'POS', 'REF', 'ALT', 'PREDICTIONSCORE']]
    print(rows)
    update_table(rows, 1)
    # cst(open(analysis_file), window).pack()
    print('Selected:', analysis_file)


def update_table(rows, instance):
    for index, row in rows.iterrows():
        # Expand on this with other columns later
        # add a scrollbar and a search option, coding vs non-coding
        if instance == 1:
            trv.insert('', 'end', values=[row['#CHROM'], row['POS'], row['REF'], row['ALT'], row['PREDICTIONSCORE']])
        elif instance == 2:
            trv.insert('', 'end', values=[row['#CHROM'], row['POS'], row['REF'], row['ALT'], row['PREDICTIONSCORE'], row['protein_analysis']])

def load_image():
    #canvas = Canvas(root, width=300, height=300)
    #canvas.pack()
    #img = plotprotein()
    #canvas.create_image(20, 20, anchor=NW, image=img)
    pass


window = tk.Tk()
window.title("Iwan's analysis pipeline")

wrapper1 = LabelFrame(window, text="Pathogenicity analysis")
wrapper2 = LabelFrame(window, text="Additional analysis")


wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)


greeting = tk.Label(wrapper1, text="Put your vcf down here:")


global haplotype_var
haplotype_var = IntVar()

entry = tk.Entry(wrapper1)
file_label = tk.Label(wrapper1, text="No file selected")
haplolabel = tk.Label(wrapper1, text="Enter the required number of matching variants for haplotype analysis:")

button = tk.Button(
    wrapper1,
    text="Start analysis!",
    command=on_button_click
)

button_2 = tk.Button(wrapper1, text='Open', command=UploadAction)
button_3 = tk.Button(wrapper2, text='Open', command=Load_UploadAction)
button_selection = tk.Button(wrapper2, text='plot selection', command=select_active_items)
button_protein = tk.Button(wrapper2, text='Run protein analysis', command=run_protein_analysis)
haplocheckmark = Checkbutton(wrapper1, text="Haplotype Analysis", variable=haplotype_var)

trv = ttk.Treeview(wrapper2, columns=(1, 2, 3, 4, 5, 6), show="headings", height="10")


greeting.pack()
button_2.pack()
file_label.pack()
haplocheckmark.pack()
haplolabel.pack()
entry.pack()
button.pack()
button_3.pack()
trv.pack()
button_protein.pack()
button_selection.pack()
trv.heading(1, text="chr")
trv.heading(2, text="pos")
trv.heading(3, text="ref")
trv.heading(4, text="alt")
trv.heading(5, text="Pathogenicity score")
trv.heading(6, text="Protein analysis")
trv.bind('<ButtonRelease-1>', selectItem)



#button_4 = tk.Button(window, text='Open', command=UploadAction)
#f = open("output_annotation/clinpred_pred.txt")

#print(f)
#newtable = cst(f, window)

#newtable.pack()
# on button click run runningscript with the filename from the entry pack
window.mainloop()


# turn to grid over pack to allow better visualisation, add scrolling, maybe less detials


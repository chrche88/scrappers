import pandas as pd
import tkinter
import tkinter.filedialog as fd
import os
import datetime
import fnmatch

pd.options.mode.chained_assignment = None  # default='warn'
date = datetime.datetime.today().strftime('%Y-%m-%d')

root = tkinter.Tk()
root.withdraw()  # use to hide tkinter window

# currdir = os.getcwd()
old_path = fd.askopenfilename(title='Choisir l\'ancien', parent=root,
                           filetypes=(("Template files", "*.csv"), ("All files", "*")))
new_path = fd.askopenfilename(title='Choisir le nouveau à comparer', parent=root,
                           filetypes=(("Template files", "*.csv"), ("All files", "*")))
# tempdir = fd.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
# if len(tempdir) > 0:
# print("You chose %s" % tempdir)

df_old = pd.read_csv(old_path, header=1)
df_new = pd.read_csv(new_path)
print(df_old)
print(df_new)


df_old_inter = df_old[['ID']]
df_old_inter=df_old_inter[df_old_inter['ID']!='Pas de match']
df_new_inter = df_new[['ID']]
df_old_inter = pd.to_numeric(df_old_inter['ID'])
df_old_inter= df_old_inter.to_frame()


df_diff=df_old_inter.merge(df_new_inter, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='right_only']
df_diff.to_csv('D:\\Users\\chenchr\\Desktop\\Stage\\nouveaux_leads\\'+date+'_test.csv')
IDs_to_extract=df_diff['ID'].to_list()

print('Enregistrement dans une nouvelle feuille\n')
result = pd.DataFrame(columns=df_new.columns)
for y in IDs_to_extract:
    new_line = df_new.loc[df_new['ID'] == y]
    new_line['Date notification Stripe']=date
    result = result.append(new_line)

print(result)
result.to_csv('D:\\Users\\chenchr\\Desktop\\Stage\\nouveaux_leads\\'+date+'_bilan.csv')
listOfFiles = os.listdir('D:\\Users\\chenchr\\Desktop\\Stage\\nouveaux_leads')
pattern = "*.csv"
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, pattern):
        print(entry)
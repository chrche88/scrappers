import pandas as pd
import tkinter
import tkinter.filedialog as fd
import os
import datetime
import fnmatch

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

df_old = pd.read_csv(old_path)
df_new = pd.read_csv(new_path)

df_old_inter = df_old[['ID', 'Stripe']]
df_new_inter = df_new[['ID', 'Stripe']]
df_diff = pd.concat([df_old_inter, df_new_inter])
df_diff = df_diff.reset_index(drop=True)
df_gpby = df_diff.groupby(list(df_diff.columns))
idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
new_elements = df_diff.reindex(idx)
print('Nouvelles Activations : \n')
print(new_elements)
IDs_to_extract = new_elements['ID'].to_list()

print('Enregistrement dans une nouvelle feuille\n')
result = pd.DataFrame(columns=df_new.columns)
for y in IDs_to_extract:
    print(df_new.loc[df_new['ID'] == y])
    new_line = df_new.loc[df_new['ID'] == y]
    new_line.loc['Date notification Stripe']=date
    result = result.append(new_line)
del result['Unnamed: 0']
del result['Unnamed: 0.1']
print(result)
result.to_csv('D:\\Users\\chenchr\\Desktop\\Stage\\nouveaux_Stripe_actifs\\'+date+'_bilan.csv')
listOfFiles = os.listdir('D:\\Users\\chenchr\\Desktop\\Stage\\nouveaux_Stripe_actifs')
pattern = "*.csv"
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, pattern):
        print(entry)
import pandas as pd
import datetime
import os, fnmatch

date = datetime.datetime.today().strftime('%Y-%m-%d')

df = pd.read_csv('D:\\Users\\chenchr\\Desktop\\Stage\\aeo_stripe_modified2.csv')
noms_colonnes = df.columns.values
non_stripe = pd.DataFrame(columns=noms_colonnes)
stripe = pd.DataFrame(columns=noms_colonnes)

non_stripe = df.loc[df['Stripe'] == 'non']
stripe = df.loc[df['Stripe'] == 'oui']

non_stripe.to_csv('D:\\Users\\chenchr\\Desktop\\Stage\\Stripe\\' + date + '_stripe_non_actif.csv')
stripe.to_csv('D:\\Users\\chenchr\\Desktop\\Stage\\Stripe\\' + date + '_stripe_actif.csv')
print("Liste Fichiers : \n")
listOfFiles = os.listdir('D:\\Users\\chenchr\\Desktop\\Stage\\Stripe')
pattern = "*.csv"
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, pattern):
        print(entry)
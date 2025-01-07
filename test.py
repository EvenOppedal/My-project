[verdi**3 for verdi in range(10)]

liste= ["en", "to"]

[print(i) for i in motorcycles]

# +
# motorcycles = ['honda', 'yamaha', 'suzuki']

motorcycles.insert(0, 'ducati')
# -

motorcycles

import pandas as pd

df = pd.read_parquet("gs://ssb-finmark-data-produkt-prod/kredind/inndata/K3/kodelister/kodeliste_prefiks6.parquet")

 df.Post.unique()

liste = ['22000', '22100', '22200',
       '23800']

df.loc[df["Post"].isin([liste[1]])]

# +
for post in liste:
    display(df.loc[df["Post"].isin([post])])


# -

r13 = pd.read_parquet("gs://ssb-finmark-data-produkt-prod/orbof_data/inndata/o13_25per.parquet", 
                     columns = ['orgnr', 'periode', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5',
       'ltid', 'pant', 'portf', 'verd', 'sek', 'nace', 'landkode',
       'fylke', 'valuta', 'verdi', 'stype_filial',
       'stype']
                     )

r13.loc[r13["f3"]== "6"].valuta.unique()

r13.columns



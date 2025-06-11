import pandas as pd
import pickle
import sqlite3

with open('/myapp/data/product_names.pkl', 'rb') as handle:
	product_names = pickle.load(handle)
with open('/myapp/data/color.pkl', 'rb') as handle:
	color = pickle.load(handle)
with open('/myapp/data/colors_mesh.pkl', 'rb') as handle:
	colors_mesh = pickle.load(handle)

con = sqlite3.connect("/myapp/data/dataset_LDA2D.db")
dataset_LDA2D = pd.read_sql_query("SELECT * FROM dataset_LDA2D", con)
con.close()

con = sqlite3.connect("/myapp/data/df_mesh.db")
df_mesh = pd.read_sql_query("SELECT * FROM df_mesh", con)
con.close()

product_names.insert(0,"Ecosystem")
import matplotlib.pyplot as plt
import pandas as pd
import umap
import umap.plot
import numpy as np
from bokeh.plotting import output_file, save
from sklearn.preprocessing import LabelEncoder

# Import your dataset
path= 'The path to your dataset (whose format is excel spreadsheet in this case)'
kappa_df = pd.read_excel(path)

# Encode with numerical values from 0 to n_class-1 (this step is optional)
labelencoder = LabelEncoder()
kappa_df['bond type_N']  = labelencoder.fit_transform(kappa_df['bond type'])
kappa_df['name_N'] = labelencoder.fit_transform(kappa_df['name'])

# A dataframe without target column
kappa_df_X = kappa_df.loc[:, kappa_df.columns!='thermal conductivity [W/mK]']
# A dataframe with only target column
kappa_df_Y = kappa_df.loc[:, kappa_df.columns=='thermal conductivity [W/mK]']

refcodes = kappa_df_X .index.values
bg = kappa_df_Y.values
bg_class = np.empty(len(refcodes), dtype=object)
bg = np.empty(len(refcodes))

# Define the class of thermal conductivity values
for i, ref in enumerate(refcodes):
	b = kappa_df_Y.loc[ref]['thermal conductivity [W/mK]']
	bg[i] = b
	if b < 0.3:
		bg_class[i] = '[0 , 0.3)'
	elif b < 0.5:
		bg_class[i] = '[0.3 , 0.5)'
	elif b < 1:
		bg_class[i] = '[0.5 , 1)'
	elif b< 3:
		bg_class[i] = '[1 , 3)'
	else:
		bg_class[i] = '[3, 60]'
        
# Perform UMAP
seed = 42
fit = umap.UMAP(n_neighbors=50, min_dist=0.8, random_state=seed, metric='jaccard')
u = fit.fit(kappa_df_X)
# Make static plot
plt.rcParams["figure.dpi"] = 1000
p = umap.plot.points(u, labels=bg_class, color_key_cmap='Spectral',
					 width=8500, height=8500)
p.texts[0].set_visible(False)
plt.savefig('umap_.png', transparent=False)

# Make interactive plot
hover_data = pd.DataFrame({'Refcode': refcodes, 'E_g': bg})
p_int = umap.plot.interactive(
	u, labels=bg_class, color_key_cmap='Spectral', hover_data=hover_data, point_size=2)
output_file('umap.html')
save(p_int)


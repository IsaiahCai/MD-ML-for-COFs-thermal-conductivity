import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 

# Import your dataset
path= 'The path to your dataset (whose format is excel spreadsheet in this case)'
df = pd.read_excel(path)

plt.figure(figsize=(16,8))
# Use the Heatmap Api 
heatmap = sns.heatmap(df.corr(), vmin=-1,vmax=1,annot=True,cmap='BrBG')
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':16}, pad=12)
plt.savefig('The path for the created image',dpi=300,bbox_inches='tight')
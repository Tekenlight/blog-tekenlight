import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
data= pd.read_csv('AF_PORT.csv')
data.Nationality.replace('British ', 'British', inplace=True)
data.LogbookLanguage.replace('British', 'English', inplace=True)

def get_annual(col, n):
    #count unique voyages by unique ships
    dat = data[[col, 'Year', 'VoyageIni']].drop_duplicates()
    nat_by_day = dat[dat.Year > 1745].groupby(['Year'])[col].value_counts().unstack(1).fillna(0)
    top_places = nat_by_day.sum().sort_values(ascending=False)[:n].index
    return nat_by_day, top_places
def norm(df):
    return df.div(df.sum(axis=1), axis=0)

nat_by_day, top_places = get_annual('LogbookLanguage', 10)
# norm(nat_by_day[top_places]).plot(kind='area', figsize=(15, 5), cmap=matplotlib.colors.ListedColormap(sns.color_palette('RdYlGn', 10)))
fig = plt.figure()
ax = fig.add_subplot(111)
nat_by_day.plot(kind='area', figsize=(15, 5), ax=ax, cmap=matplotlib.colors.ListedColormap(sns.color_palette('Paired', 10)))
plt.title('Logbook language over time')
fig.savefig('AF1.png')

#Nationality
nat_by_day, top_places = get_annual('Nationality', 10)
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
norm(nat_by_day).plot(kind='area', figsize=(15, 5), ax=ax2, cmap=matplotlib.colors.ListedColormap(sns.color_palette('Paired', 16)))
plt.title('Nationality over time (normalized)')
plt.ylim([0,1])
fig2.savefig('AF2.png')

#Ship type
nat_by_day, top_places = get_annual('ShipType', 7)
fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
norm(nat_by_day[top_places]).plot(kind='area', figsize=(15, 5), ax=ax3, cmap=matplotlib.colors.ListedColormap(sns.color_palette('Paired', 7)))
plt.ylim([0,1])
plt.title('Top-7 ship types (normalized)')
fig3.savefig('fig_3.png')
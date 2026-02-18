import matplotlib.pyplot as plt
from collections import Counter,defaultdict
import csv
import sys
import os

from hp_eval import get_ships_hp,build_df_hp,get_stats_hp
from sw_eval import get_ships_sw,build_df_sw,get_stats_sw
from lotr_eval import get_ships_lotr,build_df_lotr,get_stats_lotr
from got_eval import get_ships_got,build_df_got,get_stats_got

ships_hp=get_ships_hp()
df_hp=build_df_hp(ships_hp)
stats_hp=get_stats_hp(ships_hp)
print(stats_hp)

ships_got=get_ships_got()
df_got=build_df_got(ships_got)
stats_got=get_stats_got(ships_got)
print(stats_got)

"""ships_lotr=get_ships_lotr()
df_lotr=build_df_lotr(ships_lotr)
stats_lotr=get_stats_lotr()

ships_sw=get_ships_sw()
df_sw=build_df_sw(ships_sw)
stats_sw=get_stats_sw()

print(df_sw)"""

lotr_data={'F/M':5}
sw_data={'F/M':3}
hp_data={'F/M':7,'M/M':1}


"""
plt.figure(figsize=(14,7))"""

"""for ship in df_hp.columns:
    plt.plot(df_hp.index, df_hp[ship], label=ship)"""
       



top_ships = df_hp.iloc[-1].sort_values(ascending=False).head(10).index

plt.figure(figsize=(14, 7))

for ship in top_ships:
    plt.plot(
        df_hp.index,
        df_hp[ship],
        label=ship,
        linewidth=2,
        alpha=0.9  
    )

plt.xlabel("Date")
plt.ylabel("Total number of apparitions")
plt.title("Top 10 Ships")


plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

plt.legend(title="10 most popular HP ships",bbox_to_anchor=(1.05, 1),loc="upper left")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



"""plt.figure(figsize=(14,7))

for ship in df_got.columns:
    plt.plot(df_got.index, df_got[ship], label=ship)"""


top_ships = df_got.iloc[-1].sort_values(ascending=False).head(10).index

plt.figure(figsize=(14, 7))

for ship in top_ships:
    plt.plot(df_got.index,df_got[ship],label=ship,linewidth=2,alpha=0.9  )

plt.xlabel("Date")
plt.ylabel("Total number of apparitions")
plt.title("Top 10 Ships")


plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

plt.legend(title="10 most popular GOT ships",bbox_to_anchor=(1.05, 1),loc="upper left")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


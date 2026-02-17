import matplotlib.pyplot as pt
from collections import Counter,defaultdict
import csv
import sys
import os

from harry_potter_evaluations import get_ships_hp,build_df_hp
from star_wars_eval import get_ships_sw,build_df_sw
from lord_of_the_rings_evaluation import get_ships_lotr,build_df_lotr
from got_eval import get_ships_got,build_df_got

ships_hp=get_ships_hp()
df_hp=build_df_hp(ships_hp)

ships_got=get_ships_got()
df_got=build_df_got(ships_got)

ships_lotr=get_ships_lotr()
df_hlotr=build_df_lotr(ships_lotr)

ships_sw=get_ships_sw()
df_sw=build_df_sw(ships_sw)


print(df_sw)

lotr_data={'F/M':5}
sw_data={'F/M':3}
hp_data={'F/M':7,'M/M':1}

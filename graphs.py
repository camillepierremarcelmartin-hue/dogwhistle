import matplotlib.pyplot as plt
from collections import Counter,defaultdict
import csv
import sys
import os
import pandas as pd 
import numpy as np
from hp_eval import get_ships_hp,build_df_hp,get_stats_hp
from sw_eval import get_ships_sw,build_df_sw,get_stats_sw
from lotr_eval import get_ships_lotr,build_df_lotr,get_stats_lotr
from got_eval import get_ships_got,build_df_got,get_stats_got
def save_plot(name):
    os.makedirs("graphs", exist_ok=True)
    plt.savefig(f"graphs/{name}.png", dpi=300, bbox_inches="tight")

ships_hp=get_ships_hp()
df_hp=build_df_hp(ships_hp)
stats_hp=get_stats_hp(ships_hp)


ships_got=get_ships_got()
df_got=build_df_got(ships_got)
stats_got=get_stats_got(ships_got)


ships_lotr=get_ships_lotr()
df_lotr=build_df_lotr(ships_lotr)
stats_lotr=get_stats_lotr(ships_lotr)

ships_sw=get_ships_sw()
df_sw=build_df_sw(ships_sw)
stats_sw=get_stats_sw(ships_sw)


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
save_plot("top10hp")
plt.show()



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
save_plot("top10got")
plt.show()


top_ships = df_sw.iloc[-1].sort_values(ascending=False).head(10).index

plt.figure(figsize=(14, 7))

for ship in top_ships:
    plt.plot(df_sw.index,df_sw[ship],label=ship,linewidth=2,alpha=0.9  )

plt.xlabel("Date")
plt.ylabel("Total number of apparitions")
plt.title("Top 10 Ships")


plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

plt.legend(title="10 most popular SW ships",bbox_to_anchor=(1.05, 1),loc="upper left")

plt.xticks(rotation=45)
plt.tight_layout()
save_plot("top10sw")
plt.show()


top_ships = df_lotr.iloc[-1].sort_values(ascending=False).head(10).index

plt.figure(figsize=(14, 7))

for ship in top_ships:
    plt.plot(df_lotr.index,df_lotr[ship],label=ship,linewidth=2,alpha=0.9  )

plt.xlabel("Date")
plt.ylabel("Total number of apparitions")
plt.title("Top 10 Ships")


plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

plt.legend(title="10 most popular LOTR ships",bbox_to_anchor=(1.05, 1),loc="upper left")

plt.xticks(rotation=45)
plt.tight_layout()
save_plot("top10lotr")
plt.show()

colors = {
    "Harry Potter": "#6A0DAD",        
    "Game of Thrones": "#8B0000",     
    "Lord of the Rings": "#228B22",   
    "Star Wars": "#1E90FF"            
}

fandoms = {
    "Harry Potter": get_stats_hp(ships_hp),
    "Game of Thrones": get_stats_got(ships_got),
    "Lord of the Rings": get_stats_lotr(ships_lotr),
    "Star Wars": get_stats_sw(ships_sw),
}

rows = []

for name, stats in fandoms.items():
    (
        pronouns,
        gendered_characters,
        gendered_characters_canon,
        unique_ships,
        ship_to_characters,
        type_counts
    ) = stats

    total_pronouns = sum(pronouns.values())
    total_ships = sum(type_counts.values())
    total_characters = sum(gendered_characters.values())

    row = {
        "Fandom": name,

        "Masc_pronouns_ratio": pronouns["masc_pronoun"] / total_pronouns if total_pronouns else 0,
        "Fem_pronouns_ratio": pronouns["fem_pronoun"] / total_pronouns if total_pronouns else 0,
        "Neut_pronouns_ratio": pronouns["neutral_pronoun"] / total_pronouns if total_pronouns else 0,

 
        "Masc_char_ratio": gendered_characters["male_characters"] / total_characters if total_characters else 0,
        "Fem_char_ratio": gendered_characters["female_characters"] / total_characters if total_characters else 0,

        "MM_ratio": type_counts["M/M"] / total_ships if total_ships else 0,
        "FF_ratio": type_counts["F/F"] / total_ships if total_ships else 0,
        "FM_ratio": type_counts["F/M"] / total_ships if total_ships else 0,
        "Gen_ratio": type_counts["Gen"] / total_ships if total_ships else 0,

        "Total_ships": total_ships
    }

    rows.append(row)

df = pd.DataFrame(rows).set_index("Fandom")

df[["MM_ratio", "FF_ratio", "FM_ratio", "Gen_ratio"]].plot(
    kind="bar",
    figsize=(12,6)
)

plt.title("Ship type distribution by title")
plt.ylabel("Proportion")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
save_plot("ship_per_title")
plt.show()


plt.figure(figsize=(8,6))

plt.scatter(
    df["Masc_char_ratio"],
    df["MM_ratio"],
    s=df["Total_ships"]*1.5,
    alpha=0.7
)

for fandom in df.index:
    plt.text(
        df.loc[fandom, "Masc_char_ratio"],
        df.loc[fandom, "MM_ratio"],
        fandom
    )

plt.xlabel("Male character ratio (fandom)")
plt.ylabel("Ratio M/M")
plt.title("Male characters ↔  M/M Ships")
plt.grid(True, linestyle="--", alpha=0.6)
save_plot("male_to_MM")
plt.show()


plt.figure(figsize=(8,6))

sizes = df["Total_ships"] * 1.5  # pondération

plt.scatter(
    df["Masc_pronouns_ratio"],
    df["MM_ratio"],
    s=sizes,
    color=colors[fandom],
    alpha=0.85,
    edgecolor=colors[fandom],
    linewidth=1.2)


for fandom in df.index:
    plt.text(
        df.loc[fandom, "Masc_pronouns_ratio"],
        df.loc[fandom, "MM_ratio"],
        fandom
    )

plt.xlabel("Proportion of male-assigned pronouns")
plt.ylabel("Proportion of M/M ships")
plt.title("Corrélation male-assigned pronouns ↔ M/M (size = nb of ships)")
plt.grid(True, linestyle="--", alpha=0.6)
save_plot("pronouns_to_MM")
plt.show()





pronoun_cols = {
    "Masc_pronouns_ratio": "Pronoms masculins",
    "Fem_pronouns_ratio": "Pronoms féminins",
    "Neut_pronouns_ratio": "Pronoms neutres"
}

relation_cols = {
    "MM_ratio": "M/M",
    "FF_ratio": "F/F",
    "FM_ratio": "F/M",
    "Gen_ratio": "Gen"
}

fig, axes = plt.subplots(3, 4, figsize=(18, 12))

for i, (p_col, p_label) in enumerate(pronoun_cols.items()):
    for j, (r_col, r_label) in enumerate(relation_cols.items()):
        
        ax = axes[i, j]

        ax.scatter(
            df[p_col],
            df[r_col],
            s=df["Total_ships"] * 1.5,
            color=colors[fandom],
            alpha=0.85,
            edgecolor=colors[fandom],
            linewidth=1.2)

        for fandom in df.index:
            ax.text(
                df.loc[fandom, p_col],
                df.loc[fandom, r_col],
                fandom,
                fontsize=8
            )

        ax.set_xlabel(p_label)
        ax.set_ylabel(r_label)
        ax.grid(True, linestyle="--", alpha=0.5)

plt.suptitle("Pronouns correlation ↔ Ship types (weighted by # of ships)", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
save_plot("everything")
plt.show()

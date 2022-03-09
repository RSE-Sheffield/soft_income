import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

table_4c = pd.read_csv("table-4c.csv", header=11)

print(list(table_4c.columns))

# Data cleanup

table_4c["Multiplier"] = table_4c.apply(
    lambda row: int(str(1) + re.sub("[^0-9]", "", row["Unit"])), axis=1
)

table_4c["Value (£s)"] = table_4c.apply(
    lambda row: row["Value"] * row["Multiplier"], axis=1
)

# Filter

table_4c_sl = table_4c[(table_4c["Income source"] == "Software licences income")]

table_4c_sl_tuos = table_4c[
    (table_4c["HE Provider"] == "The University of Sheffield")
    & (table_4c["Income source"] == "Software licences income")
]

mean_sl = (
    table_4c_sl.groupby(["HE Provider", "Academic Year"])
    .sum()
    .groupby(["Academic Year"])["Value (£s)"]
    .mean()
    .rename("All Higher Education")
)

tuos_sl = (
    table_4c_sl_tuos.groupby(["Academic Year"])["Value (£s)"]
    .sum()
    .rename("University of Sheffield")
)

combined_sl = pd.concat([tuos_sl, mean_sl], axis=1)

print(list(combined_sl.columns))

# Plot

plt.figure()

p = sns.lineplot(data=combined_sl)

p.set_xlabel("Academic Year")
p.set_ylabel("Amount (£s)")

plt.show()

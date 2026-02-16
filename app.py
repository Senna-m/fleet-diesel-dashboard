try:
    from readline import redisplay  # Linux/macOS
except ModuleNotFoundError:
    redisplay = None  # Windows: ignora ou trate de outra forma
import pandas as pd
import numpy as np

df = pd.read_csv(
    "Abastecimento.csv",
    sep=";",        # separador correto
    decimal=".",    # decimal brasileiro
    encoding="latin1"  # comum em arquivos exportados do Excel
)

df.columns = df.columns.str.strip()
df_model = df[["VEICULO", "KM RODADA", "DIESEL","GAS","GASOLINA","ALCOOL"]].copy()
df_model = df_model.dropna(how="all")

df_model["VEICULO"] = df_model["VEICULO"].astype(str).str.strip()

# KM RODADA: já é numérico → só garante conversão
df_model["KM RODADA"] = pd.to_numeric(df_model["KM RODADA"], errors="coerce")

# DIESEL: vem como string BR → troca vírgula por ponto (NÃO remove ".")
s = df_model["DIESEL"].astype(str).str.strip()
s = s.replace({"": np.nan, "nan": np.nan, "None": np.nan, "NaN": np.nan})
s = s.str.replace(r"\s+", "", regex=True)
s = s.str.replace(",", ".", regex=False)
df_model["DIESEL"] = pd.to_numeric(s, errors="coerce")
df_model["GAS"] = pd.to_numeric(df_model["GAS"], errors="coerce")
df_model["GASOLINA"] = pd.to_numeric(df_model["GASOLINA"], errors="coerce")
df_model["ALCOOL"] = pd.to_numeric(df_model["ALCOOL"], errors="coerce")

# Remover inválidos
df_model = df_model.dropna(
    subset=["VEICULO", "KM RODADA", "DIESEL", "GAS", "GASOLINA", "ALCOOL"]
)
df_model = df_model[(df_model["KM RODADA"] > 0) & (df_model["DIESEL"] > 0)]

print("Após limpeza:", df_model.shape)
if redisplay:
    redisplay()
print(df_model.head())

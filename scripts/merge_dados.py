# merge_dados.py
import pandas as pd

print("⏳ Iniciando o cruzamento de dados do UFC...")

# 1. Carregar os datasets reais
df_fights = pd.read_csv("data/ufc_fights_processed.csv")
df_fighters = pd.read_csv("data/ufc_fighters_final.csv")

# 2. Criar chaves padronizadas (minúsculo e sem espaços) para evitar falhas no cruzamento
df_fights['f1_clean'] = df_fights['Fighter_1'].astype(str).str.lower().str.strip()
df_fights['f2_clean'] = df_fights['Fighter_2'].astype(str).str.lower().str.strip()
df_fighters['fighter_clean'] = df_fighters['Fighter_Name'].astype(str).str.lower().str.strip()

# 3. Preparar as tabelas de lutadores com sufixos identificando cada corner (_f1 e _f2)
fighters_f1 = df_fighters.add_suffix('_f1')
fighters_f2 = df_fighters.add_suffix('_f2')

# 4. Primeiro Merge: Cruzando as características do Fighter_1
df_merged = pd.merge(
    df_fights,
    fighters_f1,
    left_on='f1_clean',
    right_on='fighter_clean_f1',
    how='left'
)

# 5. Segundo Merge: Cruzando as características do Fighter_2
df_merged = pd.merge(
    df_merged,
    fighters_f2,
    left_on='f2_clean',
    right_on='fighter_clean_f2',
    how='left'
)

# 6. Remover as colunas auxiliares usadas na limpeza para manter a tabela organizada
colunas_limpeza = ['f1_clean', 'f2_clean', 'fighter_clean_f1', 'fighter_clean_f2']
df_merged = df_merged.drop(columns=colunas_limpeza, errors='ignore')

# 7. Salvar o arquivo mesclado final
caminho_salvar = "data/ufc_fights_merged_full.csv"
df_merged.to_csv(caminho_salvar, index=False)

print("✅ Cruzamento concluído com sucesso!")
print(f"💾 Arquivo unificado salvo em: {caminho_salvar}")
print(f"📊 Total de lutas processadas no histórico: {len(df_merged)}")
print(f"✨ Agora você tem colunas como 'Reach_f1', 'Reach_f2', 'DOB_f1' e 'DOB_f2' na mesma linha!")
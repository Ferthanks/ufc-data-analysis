# scripts/idade_experiencia.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("⏳ Processando dados no Modo Escuro (Transparente)...")

# ==========================================
# 1. CONFIGURAÇÃO MODO ESCURO (TEXTOS BRANCOS)
# ==========================================
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['axes.titlecolor'] = 'white'

# ==========================================
# 2. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ==========================================
df = pd.read_csv("data/ufc_fights_merged_full.csv")

df['Event_Date'] = pd.to_datetime(df['Event_Date'])
df['DOB_f1'] = pd.to_datetime(df['DOB_f1'], errors='coerce')
df['DOB_f2'] = pd.to_datetime(df['DOB_f2'], errors='coerce')

df = df.sort_values('Event_Date').reset_index(drop=True)

# Contar Experiência Acumulada
fights_counter = {}
f1_historical_fights = []
f2_historical_fights = []

for idx, row in df.iterrows():
    f1 = row['Fighter_1']
    f2 = row['Fighter_2']
    
    f1_historical_fights.append(fights_counter.get(f1, 0))
    f2_historical_fights.append(fights_counter.get(f2, 0))
    
    fights_counter[f1] = fights_counter.get(f1, 0) + 1
    fights_counter[f2] = fights_counter.get(f2, 0) + 1

df['Exp_f1'] = f1_historical_fights
df['Exp_f2'] = f2_historical_fights

# Calcular Idade
df['Age_f1'] = (df['Event_Date'] - df['DOB_f1']).dt.days / 365.25
df['Age_f2'] = (df['Event_Date'] - df['DOB_f2']).dt.days / 365.25

df_limpo = df.dropna(subset=['Age_f1', 'Age_f2']).copy()

def determinar_corner_vencedor(row):
    if row['Winner'] == row['Fighter_1']: return 'F1'
    elif row['Winner'] == row['Fighter_2']: return 'F2'
    return 'Outro'
df_limpo['Winner_Corner'] = df_limpo.apply(determinar_corner_vencedor, axis=1)
df_limpo = df_limpo[df_limpo['Winner_Corner'].isin(['F1', 'F2'])].copy()

# Análise de Idade
df_idade = df_limpo[df_limpo['Age_f1'] != df_limpo['Age_f2']].copy()
df_idade['Older_Corner'] = df_idade.apply(lambda r: 'F1' if r['Age_f1'] > r['Age_f2'] else 'F2', axis=1)
df_idade['Resultado_Idade'] = df_idade.apply(
    lambda r: 'Mais Jovem Venceu' if r['Winner_Corner'] != r['Older_Corner'] else 'Mais Velho Venceu', axis=1
)
taxa_idade = df_idade['Resultado_Idade'].value_counts(normalize=True) * 100

# Análise de Experiência
df_exp = df_limpo[df_limpo['Exp_f1'] != df_limpo['Exp_f2']].copy()
df_exp['More_Exp_Corner'] = df_exp.apply(lambda r: 'F1' if r['Exp_f1'] > r['Exp_f2'] else 'F2', axis=1)
df_exp['Resultado_Exp'] = df_exp.apply(
    lambda r: 'Mais Experiente Venceu' if r['Winner_Corner'] == r['More_Exp_Corner'] else 'Menos Experiente Venceu', axis=1
)
taxa_exp = df_exp['Resultado_Exp'].value_counts(normalize=True) * 100

# ==========================================
# 3. CRIAÇÃO DOS GRÁFICOS (VISUAL)
# ==========================================
# Fundo transparente na figura e nos eixos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='none')
ax1.set_facecolor('none')
ax2.set_facecolor('none')

# Gráfico 1: Idade (Ouro e Prata)
cores_idade = ['#FFD700', '#C0C0C0'] # Dourado e Prata
sns.barplot(x=taxa_idade.index, y=taxa_idade.values, palette=cores_idade, ax=ax1)
ax1.set_title('O Fator Idade\n(Quem é mais jovem tem vantagem?)', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('Taxa de Vitória (%)', fontsize=12)
ax1.set_ylim(0, 100)
for i, v in enumerate(taxa_idade.values):
    # Texto branco e com contorno/peso maior para aparecer bem
    ax1.text(i, v + 3, f"{v:.1f}%", ha='center', fontsize=14, fontweight='bold', color='white')

# Gráfico 2: Experiência (Vermelho UFC)
cores_exp = ['#FF2400', '#8B0000'] # Vermelho vibrante e Vinho
sns.barplot(x=taxa_exp.index, y=taxa_exp.values, palette=cores_exp, ax=ax2)
ax2.set_title('O Peso da Experiência\n(Mais lutas no UFC garantem a vitória?)', fontsize=14, fontweight='bold', pad=15)
ax2.set_ylabel('')
ax2.set_ylim(0, 100)
for i, v in enumerate(taxa_exp.values):
    ax2.text(i, v + 3, f"{v:.1f}%", ha='center', fontsize=14, fontweight='bold', color='white')

# Limpar bordas superiores e direitas
sns.despine(ax=ax1)
sns.despine(ax=ax2)

plt.suptitle('Juventude vs. Bagagem: O que dita o Sucesso no Octógono?', fontsize=18, fontweight='bold', y=1.05, color='white')
plt.tight_layout()

# ==========================================
# 4. SALVAR COM FUNDO TRANSPARENTE
# ==========================================
caminho_imagem = 'graphs/idade_vs_experiencia_dark.png'
# O segredo absoluto está no transparent=True
plt.savefig(caminho_imagem, dpi=300, transparent=True, bbox_inches='tight')

print(f"✅ Gráfico dark mode gerado com sucesso em: {caminho_imagem}")
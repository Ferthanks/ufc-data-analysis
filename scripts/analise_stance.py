# scripts/analise_stance.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("⏳ Analisando o impacto da base dos lutadores (Stance)...")

# 1. Carregar a base de dados mesclada
df = pd.read_csv("data/ufc_fights_merged_full.csv")

# 2. Identificar o corner vencedor (F1 ou F2) e remover empates
def determinar_corner_vencedor(row):
    if row['Winner'] == row['Fighter_1']: return 'F1'
    elif row['Winner'] == row['Fighter_2']: return 'F2'
    return 'Outro'

df['Winner_Corner'] = df.apply(determinar_corner_vencedor, axis=1)
df_limpo = df[df['Winner_Corner'].isin(['F1', 'F2'])].copy()

# Padronizar os textos das colunas de Stance (remover espaços e garantir texto)
df_limpo['Stance_f1'] = df_limpo['Stance_f1'].astype(str).str.strip()
df_limpo['Stance_f2'] = df_limpo['Stance_f2'].astype(str).str.strip()

# 3. ANÁLISE 1: Taxa de Vitória Geral por Stance
# Como cada luta tem dois atletas, vamos empilhar os dados para contar aparições e vitórias de cada base
f1_data = df_limpo[['Stance_f1', 'Winner_Corner']].rename(columns={'Stance_f1': 'Stance'})
f1_data['Ganhou'] = f1_data['Winner_Corner'] == 'F1'

f2_data = df_limpo[['Stance_f2', 'Winner_Corner']].rename(columns={'Stance_f2': 'Stance'})
f2_data['Ganhou'] = f2_data['Winner_Corner'] == 'F2'

df_aparentes = pd.concat([f1_data, f2_data])

# Filtrar apenas as 3 bases principais do UFC
bases_principais = ['Orthodox', 'Southpaw', 'Switch']
df_aparentes = df_aparentes[df_aparentes['Stance'].isin(bases_principais)]

# Calcular a taxa de vitória de cada base
stats_geral = df_aparentes.groupby('Stance')['Ganhou'].agg(['count', 'sum'])
stats_geral['Taxa_Vitoria'] = (stats_geral['sum'] / stats_geral['count']) * 100
stats_geral = stats_geral.reindex(bases_principais) # Manter ordem fixa

# 4. ANÁLISE 2: Confronto Direto (Southpaw vs Orthodox)
df_matchup = df_limpo[
    ((df_limpo['Stance_f1'] == 'Southpaw') & (df_limpo['Stance_f2'] == 'Orthodox')) |
    ((df_limpo['Stance_f1'] == 'Orthodox') & (df_limpo['Stance_f2'] == 'Southpaw'))
].copy()

def verificar_vencedor_matchup(row):
    if row['Winner_Corner'] == 'F1':
        return row['Stance_f1']
    else:
        return row['Stance_f2']

df_matchup['Stance_Vencedora'] = df_matchup.apply(verificar_vencedor_matchup, axis=1)
taxa_matchup = df_matchup['Stance_Vencedora'].value_counts(normalize=True) * 100
taxa_matchup = taxa_matchup.reindex(['Southpaw', 'Orthodox']) # Focar apenas nos dois

# 5. Configurar e Desenhar os Gráficos Lado a Lado
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
sns.set_theme(style="white")

# Gráfico 1: Aproveitamento Geral
cores_geral = ['#4682B4', '#2E8B57', '#8B0000'] # Cores distintas para cada base
sns.barplot(x=stats_geral.index, y=stats_geral['Taxa_Vitoria'], palette=cores_geral, ax=ax1)
ax1.set_title('Aproveitamento Geral por Base\n(Total de lutas de cada estilo)', fontsize=12, fontweight='bold', pad=10)
ax1.set_ylabel('Taxa de Vitória (%)', fontsize=11)
ax1.set_xlabel('Base (Stance)', fontsize=11)
ax1.set_ylim(0, 100)
for i, v in enumerate(stats_geral['Taxa_Vitoria']):
    ax1.text(i, v + 2, f"{v:.1f}%", ha='center', fontsize=12, fontweight='bold')

# Gráfico 2: Confronto Direto
cores_matchup = ['#2E8B57', '#4682B4'] # Mantém as cores correspondentes (Southpaw e Orthodox)
sns.barplot(x=taxa_matchup.index, y=taxa_matchup.values, palette=cores_matchup, ax=ax2)
ax2.set_title('Confronto Direto: Southpaw vs. Orthodox\n(Quem vence quando eles se enfrentam?)', fontsize=12, fontweight='bold', pad=10)
ax2.set_ylabel('')
ax2.set_xlabel('Base Vencedora', fontsize=11)
ax2.set_ylim(0, 100)
for i, v in enumerate(taxa_matchup.values):
    ax2.text(i, v + 2, f"{v:.1f}%", ha='center', fontsize=12, fontweight='bold')

# Remover bordas desnecessárias
sns.despine(ax=ax1)
sns.despine(ax=ax2)

plt.suptitle('A Geometria do Combate: A base do lutador influencia no resultado?', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()

# Salvar gráfico na pasta graphs
caminho_imagem = 'graphs/analise_stance.png'
plt.savefig(caminho_imagem, dpi=300, bbox_inches='tight')

print(f"✅ Gráfico de Stance gerado com sucesso em: {caminho_imagem}")
print(f"📊 Total de confrontos diretos Southpaw vs Orthodox analisados: {len(df_matchup)}")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Processando a análise de base (Stance) em Modo Escuro (Transparente)...")

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
stats_geral = stats_geral.reindex(bases_principais)

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
taxa_matchup = taxa_matchup.reindex(['Southpaw', 'Orthodox'])

# ----------------- INÍCIO DA MÁGICA DO DARK MODE -----------------

# Configurar o estilo global para letras e eixos brancos
plt.rcParams.update({
    "text.color": "white",
    "axes.labelcolor": "white",
    "axes.edgecolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "figure.facecolor": "none", # Fundo 100% transparente
    "axes.facecolor": "none"    # Fundo 100% transparente
})

# 5. Configurar e Desenhar os Gráficos Lado a Lado
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Gráfico 1: Aproveitamento Geral
# Cores combinando com o slide: Orthodox (Vermelho), Southpaw (Cinza Claro), Switch (Cinza Escuro)
cores_geral = ['#FF3333', '#AAAAAA', '#555555'] 
sns.barplot(
    x=stats_geral.index, 
    y=stats_geral['Taxa_Vitoria'], 
    palette=cores_geral, 
    hue=stats_geral.index,
    legend=False,
    ax=ax1
)
ax1.set_title('Aproveitamento Geral por Base\n(Total de lutas de cada estilo)', fontsize=12, fontweight='bold', pad=10)
ax1.set_ylabel('Taxa de Vitória (%)', fontsize=11)
ax1.set_xlabel('Base (Stance)', fontsize=11)
ax1.set_ylim(0, 100)

# Forçar a cor branca nos textos das porcentagens
for i, v in enumerate(stats_geral['Taxa_Vitoria']):
    ax1.text(i, v + 2, f"{v:.1f}%", ha='center', fontsize=12, fontweight='bold', color='white')

# Gráfico 2: Confronto Direto
# Mantém as cores correspondentes ao gráfico 1 para Southpaw e Orthodox
cores_matchup = ['#AAAAAA', '#FF3333'] 
sns.barplot(
    x=taxa_matchup.index, 
    y=taxa_matchup.values, 
    palette=cores_matchup, 
    hue=taxa_matchup.index,
    legend=False,
    ax=ax2
)
ax2.set_title('Confronto Direto: Southpaw vs. Orthodox\n(Quem vence quando eles se enfrentam?)', fontsize=12, fontweight='bold', pad=10)
ax2.set_ylabel('')
ax2.set_xlabel('Base Vencedora', fontsize=11)
ax2.set_ylim(0, 100)

# Forçar a cor branca nos textos das porcentagens
for i, v in enumerate(taxa_matchup.values):
    ax2.text(i, v + 2, f"{v:.1f}%", ha='center', fontsize=12, fontweight='bold', color='white')

# Remover bordas desnecessárias
sns.despine(ax=ax1, top=True, right=True)
sns.despine(ax=ax2, top=True, right=True)

plt.suptitle('A Geometria do Combate: A base do lutador influencia no resultado?', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()

# Salvar gráfico forçando a transparência na pasta para os slides
caminho_imagem = 'png_para_slide/analise_stance.png'
plt.savefig(caminho_imagem, transparent=True, dpi=300, bbox_inches='tight')

print(f"✅ Gráfico dark mode gerado com sucesso em: {caminho_imagem}")
print(f"📊 Total de confrontos diretos Southpaw vs Orthodox analisados: {len(df_matchup)}")
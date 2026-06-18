import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Processando os dados de envergadura em Modo Escuro (Transparente)...")

# 1. Carregar a base de dados mesclada
df = pd.read_csv("data/ufc_fights_merged_full.csv")

# 2. Limpar os dados de Envergadura (Reach)
df['Reach_f1_num'] = df['Reach_f1'].astype(str).str.replace('"', '').str.replace("'", "").astype(float, errors='ignore')
df['Reach_f2_num'] = df['Reach_f2'].astype(str).str.replace('"', '').str.replace("'", "").astype(float, errors='ignore')

# Converter forçadamente para numérico, transformando erros em NaN
df['Reach_f1_num'] = pd.to_numeric(df['Reach_f1_num'], errors='coerce')
df['Reach_f2_num'] = pd.to_numeric(df['Reach_f2_num'], errors='coerce')

# Remover lutas onde não temos os dados de envergadura de algum dos lutadores
df_limpo = df.dropna(subset=['Reach_f1_num', 'Reach_f2_num']).copy()

# 3. Determinar quem ganhou a luta (Fighter 1 ou Fighter 2)
def determinar_vencedor(row):
    if row['Winner'] == row['Fighter_1']: return 'F1'
    elif row['Winner'] == row['Fighter_2']: return 'F2'
    else: return 'Empate/NC'

df_limpo['Winner_Corner'] = df_limpo.apply(determinar_vencedor, axis=1)

# Filtrar apenas as lutas que tiveram um vencedor claro (remover empates)
df_limpo = df_limpo[df_limpo['Winner_Corner'].isin(['F1', 'F2'])].copy()

# 4. Determinar quem tinha a maior envergadura
def vantagem_envergadura(row):
    if row['Reach_f1_num'] > row['Reach_f2_num']: return 'F1'
    elif row['Reach_f2_num'] > row['Reach_f1_num']: return 'F2'
    else: return 'Igual'

df_limpo['Reach_Advantage'] = df_limpo.apply(vantagem_envergadura, axis=1)

# 5. Avaliar o resultado: O lutador com braços mais longos ganhou?
df_diferenca = df_limpo[df_limpo['Reach_Advantage'] != 'Igual'].copy()

def resultado_luta(row):
    if row['Reach_Advantage'] == row['Winner_Corner']:
        return 'Maior Envergadura Venceu'
    else:
        return 'Menor Envergadura Venceu'

df_diferenca['Resultado_Final'] = df_diferenca.apply(resultado_luta, axis=1)

# Calcular as percentagens
taxa_vitorias = df_diferenca['Resultado_Final'].value_counts(normalize=True) * 100

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

# 6. Gerar o Gráfico (Visualização)
plt.figure(figsize=(9, 6))

# Usar um esquema de cores combinando com o slide do UFC (Vermelho e Cinza)
cores = ['#FF3333', '#888888'] 
ax = sns.barplot(
    x=taxa_vitorias.index, 
    y=taxa_vitorias.values, 
    hue=taxa_vitorias.index, # <-- Corrige o aviso do Seaborn
    legend=False,            # <-- Esconde a legenda
    palette=cores
)

plt.title('O Mito da Envergadura: Ter braços longos garante a vitória?', fontsize=14, fontweight='bold', pad=15)
plt.ylabel('Taxa de Vitória (%)', fontsize=12)
plt.xlabel('')

# Adicionar as percentagens no topo das barras (Forçando a cor branca no texto)
for i, v in enumerate(taxa_vitorias.values):
    ax.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=13, fontweight='bold', color='white')

# Ajustar o limite do eixo Y para dar espaço ao texto
plt.ylim(0, max(taxa_vitorias.values) + 15)

# Remover a linha de cima e da direita para um visual limpo
sns.despine(top=True, right=True)

# Salvar a imagem na pasta correta para os slides forçando a transparência
caminho_imagem = 'png_para_slide/mito_envergadura.png'
plt.tight_layout()
plt.savefig(caminho_imagem, transparent=True, dpi=300)

print(f"✅ Gráfico dark mode gerado com sucesso em: {caminho_imagem}")
print(f"📊 Total de lutas analisadas com diferença de envergadura: {len(df_diferenca)}")
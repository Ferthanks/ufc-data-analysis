import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Processando o Box Plot em Modo Escuro (Transparente)...")

# 1. Carregar os dados
df = pd.read_csv('data/ufc_fights_processed.csv')

# 2. Configurar o estilo global para letras e eixos brancos
plt.rcParams.update({
    "text.color": "white",
    "axes.labelcolor": "white",
    "axes.edgecolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "figure.facecolor": "none", # Fundo 100% transparente
    "axes.facecolor": "none"    # Fundo 100% transparente
})

# 3. Criar a Figura
plt.figure(figsize=(12, 7))

# 4. Gerar o Box Plot (Usando os nomes exatos das colunas)
ax = sns.boxplot(
    data=df, 
    x='Era', 
    y='Total_Fight_Time_Min',
    hue='Era',           
    legend=False,        
    palette='Reds_r', 
    linewidth=2,
    flierprops={"marker": "o", "markerfacecolor": "white", "markeredgecolor": "white", "alpha": 0.5}
)

# 5. Textos e Títulos
plt.title('Tempo de Combate e Regulamentação: A Estabilização nas Eras Modernas', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Era Institucional', fontsize=14, labelpad=10)
plt.ylabel('Duração da Luta (Minutos)', fontsize=14, labelpad=10)

# Rotacionar os nomes das eras no eixo X
plt.xticks(rotation=15)

# Remover a linha de cima e da direita
sns.despine(top=True, right=True)

# 6. Salvar a imagem forçando a transparência na pasta correta
caminho_imagem = 'png_para_slide/box_plot_tempo_medio_por_eras.png'
plt.tight_layout()
plt.savefig(caminho_imagem, transparent=True, dpi=300)

print(f"✅ Gráfico dark mode gerado com sucesso em: {caminho_imagem}")
# scatter_plot.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plotar_dispersao_por_era():
    try:
        df_stats = pd.read_csv('ufc_stats_per_min.csv')
    except FileNotFoundError:
        print("Erro: O arquivo 'ufc_stats_per_min.csv' não foi encontrado.")
        return

    print("Gerando gráficos de dispersão separados por Era...")
    
    sns.set_theme(style="whitegrid")
    
    # As mesmas cores de alto contraste
    cores_claras = {
        'No-Rules Era': '#E63946',
        'Dark Ages': '#F4A261',
        'Zuffa Boom': '#2A9D8F',
        'Fox & USADA Era': '#457B9D',
        'Modern/ESPN Era': '#7209B7'
    }
    
    # 1. Criar o grid de múltiplos gráficos (Facets)
    g = sns.relplot(
        data=df_stats,
        x='Sig_Landed_Per_Min',
        y='TD_Landed_Per_Min',
        col='Era',             # Informa ao Seaborn para criar 1 gráfico por Era
        col_wrap=3,            # Define no máximo 3 gráficos por linha
        hue='Era',
        palette=cores_claras,
        alpha=0.5,             # Transparência
        kind='scatter',
        height=4,              # Altura de cada sub-gráfico
        aspect=1.2,            # Proporção largura/altura
        legend=False
    )

    # 2. Renomear os títulos de cada sub-gráfico e os eixos
    g.set_axis_labels('Golpes Sig. / Minuto', 'Quedas / Minuto')
    g.set_titles(col_template="{col_name}", size=13, weight='bold') # Remove o texto "Era =" do título
    
    # 3. Calcular a média para desenhar o "X" central
    df_eras_centro = df_stats.groupby('Era', observed=True)[['Sig_Landed_Per_Min', 'TD_Landed_Per_Min']].mean().reset_index()
    
    # 4. Iterar sobre cada gráfico criado para adicionar o "X" e fixar as escalas
    for era, ax in g.axes_dict.items():
        # Pegar apenas a média da era atual do loop
        media_era = df_eras_centro[df_eras_centro['Era'] == era]
        
        if not media_era.empty:
            ax.scatter(
                x=media_era['Sig_Landed_Per_Min'].values[0],
                y=media_era['TD_Landed_Per_Min'].values[0],
                color=cores_claras[era],
                s=300,
                marker='X',
                edgecolor='black',
                linewidth=2,
                zorder=10 # Força o X a ficar na frente das outras bolinhas
            )
            
            # CRÍTICO: Fixar o mesmo limite de eixo para TODOS os gráficos
            # Sem isso, não tem como comparar uma era com a outra de forma justa
            ax.set_xlim(-0.5, 8)
            ax.set_ylim(-0.05, 0.6)

    # 5. Título geral da figura
    plt.subplots_adjust(top=0.88) # Dá um espaço extra no topo
    g.fig.suptitle('Evolução Tática do UFC: Distribuição de Estilos por Era', fontsize=18, fontweight='bold')
    
    print("Gráfico em painéis gerado com sucesso!")
    plt.show()

if __name__ == "__main__":
    plotar_dispersao_por_era()
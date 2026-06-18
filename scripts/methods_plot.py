# methods_plot.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plotar_evolucao_metodos():
    try:
        df = pd.read_csv('data/ufc_fights_processed.csv')
    except FileNotFoundError:
        print("Erro: O arquivo 'ufc_fights_processed.csv' não foi encontrado.")
        return

    print("Calculando a evolução dos métodos de vitória (Ordem Cronológica)...")

    # 1. Função para limpar e agrupar a coluna 'Method'
    def categorizar_metodo(metodo):
        metodo = str(metodo).lower()
        if 'ko' in metodo:          
            return 'KO/TKO'
        elif 'sub' in metodo:       
            return 'Finalização'
        elif 'dec' in metodo:       
            return 'Decisão'
        else:
            return 'Outros'         

    df['Method_Group'] = df['Method'].apply(categorizar_metodo)

    # 2. Calcular a proporção (%)
    df_counts = df.groupby(['Era', 'Method_Group'], observed=True).size().reset_index(name='Count')
    df_total = df.groupby('Era', observed=True).size().reset_index(name='Total')
    
    df_props = df_counts.merge(df_total, on='Era')
    df_props['Percentage'] = (df_props['Count'] / df_props['Total']) * 100
    df_props = df_props[df_props['Method_Group'] != 'Outros']

    # 3. Lista explícita com a ordem cronológica correta
    ordem_eras = [
        'No-Rules Era', 
        'Dark Ages', 
        'Zuffa Boom', 
        'Fox & USADA Era', 
        'Modern/ESPN Era'
    ]

    # 4. Configuração do Gráfico
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))

    paleta = {'KO/TKO': '#E63946', 'Finalização': '#2A9D8F', 'Decisão': '#457B9D'}

    # Adicionado o parâmetro "order=ordem_eras" para travar o eixo X
    ax = sns.barplot(
        data=df_props, 
        x='Era', 
        y='Percentage', 
        hue='Method_Group', 
        palette=paleta,
        order=ordem_eras 
    )

    # 5. Textos e títulos
    plt.title('Como as lutas terminam? Evolução dos Resultados por Era', fontsize=16, fontweight='bold')
    plt.ylabel('Porcentagem das Lutas (%)', fontsize=12)
    plt.xlabel('Era Histórica', fontsize=12)
    plt.legend(title='Método de Vitória')
    plt.ylim(0, 100) 

    # 6. Colocar os números (%) no topo de cada barra
    for p in ax.patches:
        if p.get_height() > 0: 
            ax.annotate(f"{p.get_height():.1f}%", 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', 
                        xytext=(0, 8), 
                        textcoords='offset points',
                        fontsize=10, weight='bold')

    plt.tight_layout()
    print("Gráfico cronológico gerado com sucesso!")
    plt.show()

if __name__ == "__main__":
    plotar_evolucao_metodos()
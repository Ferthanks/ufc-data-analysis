# weight_class_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plotar_analise_por_peso():
    try:
        df = pd.read_csv('ufc_fights_processed.csv')
    except FileNotFoundError:
        print("Erro: O arquivo 'ufc_fights_processed.csv' não foi encontrado.")
        return

    # 1. Definir e filtrar a partir da "Zuffa Boom" (2001 em diante)
    eras_validas = ['Zuffa Boom', 'Fox & USADA Era', 'Modern/ESPN Era']
    df = df[df['Era'].isin(eras_validas)].copy()

    # 2. Criar os grupos de peso
    def agrupar_peso(wc):
        wc = str(wc).lower()
        if any(x in wc for x in ['flyweight', 'bantamweight', 'featherweight', 'lightweight']):
            return 'Leves (Fly a Light)'
        elif any(x in wc for x in ['welterweight', 'middleweight']):
            return 'Médios (Welter/Middle)'
        elif any(x in wc for x in ['light heavyweight', 'heavyweight']):
            return 'Pesados (LHW/Heavy)'
        else:
            return 'Outros'

    df['Weight_Group'] = df['Weight_Class'].apply(agrupar_peso)
    df = df[df['Weight_Group'] != 'Outros']

    # 3. Categorizar métodos de vitória
    def categorizar_metodo(metodo):
        metodo = str(metodo).lower()
        if 'ko' in metodo: return 'KO/TKO'
        elif 'sub' in metodo: return 'Finalização'
        elif 'dec' in metodo: return 'Decisão'
        else: return 'Outros'

    df['Method_Group'] = df['Method'].apply(categorizar_metodo)
    df = df[df['Method_Group'] != 'Outros']

    # 4. Calcular porcentagens
    df_res = df.groupby(['Weight_Group', 'Era', 'Method_Group'], observed=True).size().reset_index(name='Count')
    df_total = df.groupby(['Weight_Group', 'Era'], observed=True).size().reset_index(name='Total')
    df_final = df_res.merge(df_total, on=['Weight_Group', 'Era'])
    df_final['Percentage'] = (df_final['Count'] / df_final['Total']) * 100

    # 5. Configurar e plotar o gráfico de categorias
    sns.set_theme(style="whitegrid")
    
    g = sns.catplot(
        data=df_final, kind='bar',
        x='Era', y='Percentage', hue='Method_Group',
        col='Weight_Group',
        palette={'KO/TKO': '#E63946', 'Finalização': '#2A9D8F', 'Decisão': '#457B9D'},
        order=eras_validas, # CORREÇÃO: Força as eras a ficarem em ordem cronológica
        height=5, aspect=1.1, legend_out=False
    )

    # Fixar a escala de 0 a 100% para todos os painéis
    g.set(ylim=(0, 100))
    g.set_axis_labels("Era Histórica", "Porcentagem das Lutas (%)")
    g.set_titles("{col_name}", size=12, weight='bold')
    
    # Adicionar as porcentagens no topo de cada barra
    for ax in g.axes.flat:
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(
                    f"{height:.1f}%", 
                    (p.get_x() + p.get_width() / 2., height), 
                    ha='center', va='center', 
                    xytext=(0, 8), 
                    textcoords='offset points',
                    fontsize=9, weight='bold'
                )

    plt.subplots_adjust(top=0.82)
    g.fig.suptitle('Evolução dos Resultados por Categoria de Peso (Desde 2001)', fontsize=16, fontweight='bold')
    
    print("Gráfico cronológico por peso gerado com sucesso!")
    plt.show()

if __name__ == "__main__":
    plotar_analise_por_peso()
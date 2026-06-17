# box_plot.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plotar_distribuicao_tempo():
    try:
        # Puxa os dados limpos direto do arquivo processado
        df_fights = pd.read_csv('ufc_fights_processed.csv')
    except FileNotFoundError:
        from pipeline_dados import processar_dados_ufc
        df_fights = processar_dados_ufc()
        
    print("Gerando o gráfico Boxplot...")
    
    # Configurações visuais do gráfico
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))
    
    # Renderiza o boxplot usando os dados do arquivo
    sns.boxplot(
        data=df_fights, 
        x='Era', 
        y='Total_Fight_Time_Min', 
        hue='Era', 
        palette='pastel', 
        legend=False
    )
    
    plt.title('Distribuição e Dispersão da Duração das Lutas por Era', fontsize=15, fontweight='bold')
    plt.xlabel('Era Histórica', fontsize=12)
    plt.ylabel('Duração da Luta (Minutos)', fontsize=12)
    plt.xticks(rotation=15)
    
    # Opcional: Define zoom limitando o eixo Y se houver outliers gigantescos distortivos
    plt.ylim(-1, 27)
    
    plt.tight_layout()
    print("Gráfico exibido com sucesso!")
    plt.show()

if __name__ == "__main__":
    plotar_distribuicao_tempo()
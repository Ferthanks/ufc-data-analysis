# heatmap.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plotar_heatmap_correlacao():
    try:
        # Lemos o arquivo bruto para extrair o tempo de controle (Ctrl_Sec) que não tínhamos nos outros
        df = pd.read_csv('data/ufc_gold_dataset_final.csv')
    except FileNotFoundError:
        print("Erro: O arquivo 'ufc_gold_dataset_final.csv' não foi encontrado.")
        return

    print("Calculando matriz de correlação...")

    # 1. Preparar os Dados (Criar as métricas de proporção)
    tempo = (df['Total_Fight_Time_Sec'] / 60).replace(0, np.nan) # Evitar erro de divisão por zero
    
    # Vamos criar um DataFrame limpo SÓ com as colunas que queremos cruzar
    df_corr = pd.DataFrame()
    df_corr['Duração da Luta (Min)'] = tempo
    df_corr['Volume Golpes (Tentados/Min)'] = df['F1_Sig_Att'] / tempo
    df_corr['Volume Golpes (Conectados/Min)'] = df['F1_Sig_Landed'] / tempo
    df_corr['Wrestling (Quedas/Min)'] = df['F1_TD_Landed'] / tempo
    df_corr['Tempo de Controle (Min)'] = df['F1_Ctrl_Sec'] / 60
    df_corr['Poder (Knockdowns)'] = df['F1_KD']
    df_corr['Ameaça Sub (Tentativas)'] = df['F1_Sub_Att']

    # 2. Calcular a correlação estatística (Método de Pearson)
    corr_matrix = df_corr.corr()

    # 3. Criar uma máscara matemática para cortar a parte de cima do quadrado
    # Isso faz com que o heatmap fique num formato de "escada", muito mais limpo
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    # 4. Configurar o layout e as cores
    sns.set_theme(style="white")
    plt.figure(figsize=(10, 8))
    
    # Paleta de cores: Do vermelho (negativo) para o azul (positivo)
    cmap = sns.diverging_palette(20, 230, as_cmap=True)

    # 5. Desenhar o gráfico
    sns.heatmap(
        corr_matrix, 
        mask=mask, 
        cmap=cmap, 
        vmax=1, vmin=-1, 
        center=0,
        square=True, 
        linewidths=.5, 
        annot=True,       # Isso é crucial: desenha os números dentro dos quadrados
        fmt=".2f",        # Arredonda para 2 casas decimais
        cbar_kws={"shrink": .8, "label": "Força da Correlação (-1 a 1)"},
        annot_kws={"size": 11, "weight": "bold"} # Deixa os números mais fáceis de ler
    )

    plt.title('Mapa de Calor: Correlações Táticas no UFC', fontsize=18, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=11)
    plt.yticks(fontsize=11)
    
    plt.tight_layout()
    print("Mapa de calor gerado com sucesso!")
    plt.show()

if __name__ == "__main__":
    plotar_heatmap_correlacao()
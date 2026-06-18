# df_stats.py
import pandas as pd
import numpy as np

def gerar_estatisticas_por_minuto():
    try:
        # Lê o arquivo que já possui as Eras processadas
        df_fights = pd.read_csv('data/ufc_fights_processed.csv')
    except FileNotFoundError:
        # Se você esquecer de rodar o pipeline antes, ele roda automaticamente
        from pipeline_dados import processar_dados_ufc
        df_fights = processar_dados_ufc()

    print("Calculando estatísticas por minuto (Strikes e Takedowns)...")

    # Separar e padronizar dados do Lutador 1
    stats_f1 = df_fights[['Era', 'Total_Fight_Time_Min', 'F1_Sig_Landed', 'F1_Sig_Att', 'F1_TD_Landed', 'F1_TD_Att']].copy()
    stats_f1.columns = ['Era', 'Time', 'Sig_Landed', 'Sig_Att', 'TD_Landed', 'TD_Att']
    
    # Separar e padronizar dados do Lutador 2
    stats_f2 = df_fights[['Era', 'Total_Fight_Time_Min', 'F2_Sig_Landed', 'F2_Sig_Att', 'F2_TD_Landed', 'F2_TD_Att']].copy()
    stats_f2.columns = ['Era', 'Time', 'Sig_Landed', 'Sig_Att', 'TD_Landed', 'TD_Att']
    
    # Combinar ambos em uma visão única de performance individual
    df_stats = pd.concat([stats_f1, stats_f2], ignore_index=True)
    
    # Prevenir erro de divisão por zero caso haja alguma luta inválida de 0 segundos
    df_stats['Time'] = df_stats['Time'].replace(0, np.nan)
    
    # Calcular as colunas finais por minuto
    df_stats['Sig_Landed_Per_Min'] = df_stats['Sig_Landed'] / df_stats['Time']
    df_stats['Sig_Att_Per_Min'] = df_stats['Sig_Att'] / df_stats['Time']
    df_stats['TD_Landed_Per_Min'] = df_stats['TD_Landed'] / df_stats['Time']
    df_stats['TD_Att_Per_Min'] = df_stats['TD_Att'] / df_stats['Time']
    
    # Exportar tabela final calculada
    caminho_salvar = "data/ufc_stats_per_min.csv"
    df_stats.to_csv(caminho_salvar, index=False)
    print("Arquivo 'ufc_stats_per_min.csv' gerado!")
    
    # Exibe um resumo no terminal para você validar os dados
    print("\nMédia de desempenho por Era:")
    print(df_stats.groupby('Era', observed=True)[['Sig_Landed_Per_Min', 'TD_Landed_Per_Min']].mean())
    
    return df_stats

if __name__ == "__main__":
    gerar_estatisticas_por_minuto()
# pipeline_dados.py
import pandas as pd

def processar_dados_ufc():
    print("Iniciando o processamento dos dados do UFC...")
    
    # Carrega o arquivo original
    df = pd.read_csv('ufc_gold_dataset_final.csv')
    
    # Corrige as datas e cria as Eras
    df["Event_Date"] = pd.to_datetime(df["Event_Date"])
    bins = [0, 1996, 2000, 2011, 2018, 2099] 
    labels = ['No-Rules Era', 'Dark Ages', 'Zuffa Boom', 'Fox & USADA Era', 'Modern/ESPN Era']
    df["Era"] = pd.cut(df["Event_Date"].dt.year, bins=bins, labels=labels)
    
    # Cria a coluna de minutos calculada corretamente
    df['Total_Fight_Time_Min'] = df['Total_Fight_Time_Sec'] / 60
    
    # Salva o dataset atualizado para os outros scripts usarem
    df.to_csv('ufc_fights_processed.csv', index=False)
    print("Arquivo 'ufc_fights_processed.csv' gerado e atualizado!")
    return df

if __name__ == "__main__":
    # Executa o pipeline se você rodar este arquivo diretamente
    processar_dados_ufc()
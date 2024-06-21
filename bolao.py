import streamlit as st
import pandas as pd
import csv

st.set_page_config(
    page_title="Copa América 2024",
        layout="wide"
)

col1, col2 = st.columns(2)

col1.markdown("## BOLÃO COPA AMÉRICA 2024")
participante = col1.text_input("Parcipante:", value="")
col2.markdown("## ")
col2.markdown("## ")
col2.markdown("## ")
col2.markdown("## ")

col1.markdown("### FASE DE CLASSIFICAÇÃO")


tabelaMestre = []
with open("jogos.csv", "r", encoding='utf-8') as f:
    fileCsv = csv.reader(f, delimiter=";")
    for x in fileCsv:
        tabelaMestre.append({"participante": "Tabela Mestre",
                          "id": x[0],
                          "jogoM": x[1],
                          "imgM": "./app/static/" + x[1] + ".png",
                          "placarM": 0,
                          "placarV": 0,
                          "imgV": "./app/static/" + x[2] + ".png",
                          "jogoV": x[2],
                          "vencedor": "",
                          "grupo": x[3],
                           })


df = col1.data_editor(tabelaMestre, height=900, num_rows = "dynamic",
               column_config={"imgM": st.column_config.ImageColumn(),
                              "imgV": st.column_config.ImageColumn(),
                              "placarM": st.column_config.NumberColumn(format="%d"),
                              "placarV": st.column_config.NumberColumn(format="%d") },
                              

    	        disabled = ["participante","id", "jogoM", "imgM", "imgV", "jogo", "vencedor","grupo"]
)

df2 = pd.DataFrame(tabelaMestre)

dfClass = pd.DataFrame(columns=['selecao','flag','p','v','e','d','gp','gc','sg','grupo'])

dfClass['selecao'] = df2['jogoM'].unique()

dfClass = dfClass.fillna(value=0)

for x in dfClass.loc[:, 'selecao']:    
    dfClass.loc[dfClass['selecao'] == x, 'grupo'] = df2.loc[df2['jogoM'] == x, 'grupo'].unique()
    dfClass.loc[dfClass['selecao'] == x, 'flag'] =  df2.loc[df2['jogoM'] == x, 'imgM'].unique()

for x in enumerate(df):
    if x[1]['placarM'] > x[1]['placarV']:
        dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'p']  += 3

        dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'v']  += 1
        dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'gp'] += x[1]['placarM']
        dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'gc'] += x[1]['placarV']

        dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'd']  += 1
        dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'gp'] += x[1]['placarV']
        dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'gc'] += x[1]['placarM']

        df[x[0]]['vencedor'] =  x[1]['jogoM']    

    elif x[1]['placarM'] == x[1]['placarV']:
            dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'p']  += 1
            dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'p']  += 1
            
            dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'e']  += 1  
            dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'gp'] += x[1]['placarM']
            dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'gc'] += x[1]['placarV']

            dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'e']  += 1  
            dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'gp'] += x[1]['placarV']
            dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'gc'] += x[1]['placarM']

            df[x[0]]['vencedor'] = "Empate"  
    else:
            dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'p']  += 3

            dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'v']  += 1
            dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'gp'] += x[1]['placarM']
            dfClass.loc[dfClass['selecao'] == x[1]['jogoV'], 'gc'] += x[1]['placarV']

            dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'd']  += 1 
            dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'gp'] += x[1]['placarV']
            dfClass.loc[dfClass['selecao'] == x[1]['jogoM'], 'gc'] += x[1]['placarM']
            
            df[x[0]]['vencedor'] =  x[1]['jogoV']        
    
col2.markdown("### CLASSIFICAÇÃO")
col2.data_editor(dfClass[dfClass['grupo'] == 'a'].sort_values(['p','sg','gp'], ascending=False),
                column_config={"flag": st.column_config.ImageColumn()}, hide_index=True)
col2.data_editor(dfClass[dfClass['grupo'] == 'b'].sort_values(['p','sg','gp'], ascending=False),
                column_config={"flag": st.column_config.ImageColumn()},hide_index=True)
col2.data_editor(dfClass[dfClass['grupo'] == 'c'].sort_values(['p','sg','gp'], ascending=False),
                column_config={"flag": st.column_config.ImageColumn()}, hide_index=True)
col2.data_editor(dfClass[dfClass['grupo'] == 'd'].sort_values(['p','sg','gp'], ascending=False),
                column_config={"flag": st.column_config.ImageColumn()}, hide_index=True)

dfQuartas = pd.DataFrame(index=[0,1,2,3], columns=tabelaMestre[0].keys())

dfQuartas.loc[0] = ["Tabela Mestre",1,dfClass[dfClass['grupo'] == 'a'].sort_values(['p','sg','gp'], ascending=False).iloc[0]['selecao'],dfClass[dfClass['grupo'] == 'a'].sort_values(['p','sg','gp'], ascending=False).iloc[0]['flag'],None,None,dfClass[dfClass['grupo'] == 'b'].sort_values(['p','sg','gp'], ascending=False).iloc[1]['flag'],dfClass[dfClass['grupo'] == 'b'].sort_values(['p','sg','gp'], ascending=False).iloc[1]['selecao'],'','quartas']
dfQuartas.loc[1] = ["Tabela Mestre",2,dfClass[dfClass['grupo'] == 'b'].sort_values(['p','sg','gp'], ascending=False).iloc[0]['selecao'],dfClass[dfClass['grupo'] == 'b'].sort_values(['p','sg','gp'], ascending=False).iloc[0]['flag'],None,None,dfClass[dfClass['grupo'] == 'a'].sort_values(['p','sg','gp'], ascending=False).iloc[1]['flag'],dfClass[dfClass['grupo'] == 'a'].sort_values(['p','sg','gp'], ascending=False).iloc[1]['selecao'],'','quartas']
dfQuartas.loc[2] = ["Tabela Mestre",3,dfClass[dfClass['grupo'] == 'c'].sort_values(['p','sg','gp'], ascending=False).iloc[0]['selecao'],dfClass[dfClass['grupo'] == 'c'].sort_values(['p','sg','gp'], ascending=False).iloc[0]['flag'],None,None,dfClass[dfClass['grupo'] == 'd'].sort_values(['p','sg','gp'], ascending=False).iloc[1]['flag'],dfClass[dfClass['grupo'] == 'd'].sort_values(['p','sg','gp'], ascending=False).iloc[1]['selecao'],'','quartas']
dfQuartas.loc[3] = ["Tabela Mestre",4,dfClass[dfClass['grupo'] == 'd'].sort_values(['p','sg','gp'], ascending=False).iloc[0]['selecao'],dfClass[dfClass['grupo'] == 'd'].sort_values(['p','sg','gp'], ascending=False).iloc[0]['flag'],None,None,dfClass[dfClass['grupo'] == 'c'].sort_values(['p','sg','gp'], ascending=False).iloc[1]['flag'],dfClass[dfClass['grupo'] == 'c'].sort_values(['p','sg','gp'], ascending=False).iloc[1]['selecao'],'','quartas']

col1.markdown("### QUARTAS DE FINAL")
dfQuartasEdit = col1.data_editor(dfQuartas,
                column_config={"imgM": st.column_config.ImageColumn(),
                                "imgV": st.column_config.ImageColumn()                          
                                },

                                
                disabled = ["participante","id", "jogoM", "imgM", "imgV", "jogoV", "grupo"], hide_index=True)

try:
    for x in range(0,4):
        if dfQuartasEdit.loc[x]['placarM'] > dfQuartasEdit.loc[x]['placarV']:
            dfQuartasEdit.loc[x]['vencedor'] =  dfQuartasEdit.loc[x]['jogoM']
        elif dfQuartasEdit.loc[x]['placarM'] == dfQuartasEdit.loc[x]['placarV']:
            dfQuartasEdit.loc[x]['vencedor'] =  "Empate"
        else:
            dfQuartasEdit.loc[x]['vencedor'] =  dfQuartasEdit.loc[x]['jogoV']
except:
    pass

if dfQuartasEdit.loc[0]['vencedor'] ==  "Empate":
    dfQuartasEdit.loc[0]['vencedor'] = col2.selectbox("Vencedor do Jogo 1 - Quartas",("Empate", dfQuartasEdit.loc[0]['jogoM'], dfQuartasEdit.loc[0]['jogoV']))

if dfQuartasEdit.loc[1]['vencedor'] ==  "Empate":
    dfQuartasEdit.loc[1]['vencedor'] = col2.selectbox("Vencedor do Jogo 2 - Quartas",("Empate", dfQuartasEdit.loc[1]['jogoM'], dfQuartasEdit.loc[1]['jogoV']))

if dfQuartasEdit.loc[2]['vencedor'] ==  "Empate":
    dfQuartasEdit.loc[2]['vencedor'] = col2.selectbox("Vencedor do Jogo 3 - Quartas",("Empate", dfQuartasEdit.loc[2]['jogoM'], dfQuartasEdit.loc[2]['jogoV']))

if dfQuartasEdit.loc[3]['vencedor'] ==  "Empate":
    dfQuartasEdit.loc[3]['vencedor'] = col2.selectbox("Vencedor do Jogo 4 - Quartas",("Empate", dfQuartasEdit.loc[3]['jogoM'], dfQuartasEdit.loc[3]['jogoV']))


v1Flag = dfClass.loc[dfClass['selecao'] == dfQuartasEdit.loc[0]['vencedor'], 'flag'].unique()
v2Flag = dfClass.loc[dfClass['selecao'] == dfQuartasEdit.loc[1]['vencedor'], 'flag'].unique()
v3Flag = dfClass.loc[dfClass['selecao'] == dfQuartasEdit.loc[2]['vencedor'], 'flag'].unique()
v4Flag = dfClass.loc[dfClass['selecao'] == dfQuartasEdit.loc[3]['vencedor'], 'flag'].unique()

dfSemi = pd.DataFrame(index=[0,1], columns=tabelaMestre[0].keys())

try:
    
    dfSemi.loc[0] = ["Tabela Mestre",1,dfQuartasEdit.loc[0]['vencedor'],v1Flag[0],None,None,v2Flag[0],dfQuartasEdit.loc[1]['vencedor'],'','semi']
    dfSemi.loc[1] = ["Tabela Mestre",2,dfQuartasEdit.loc[2]['vencedor'],v3Flag[0],None,None,v4Flag[0],dfQuartasEdit.loc[3]['vencedor'],'','semi']

    col1.markdown("### SEMIFINAIS")
    dfSemiEdit = col1.data_editor(dfSemi,
                            column_config={"imgM": st.column_config.ImageColumn(),
                                        "imgV": st.column_config.ImageColumn()},
                            disabled = ["participante","id", "jogoM", "imgM", "imgV", "jogoV", "vencedor", "grupo"], hide_index=True)
except:
    pass


dfFinal = pd.DataFrame(index=[0], columns=tabelaMestre[0].keys())
dfTerceiro = pd.DataFrame(index=[0], columns=tabelaMestre[0].keys())

perdedor = []
try:

    for x in range(0,2):
        if dfSemiEdit.loc[x]['placarM'] > dfSemiEdit.loc[x]['placarV']:
            dfSemiEdit.loc[x]['vencedor'] =  dfSemiEdit.loc[x]['jogoM']
            perdedor.append(dfSemiEdit.loc[x]['jogoV'])
        elif dfSemiEdit.loc[x]['placarM'] == dfSemiEdit.loc[x]['placarV']:
            dfSemiEdit.loc[x]['vencedor'] =  "Empate"
        else:
            dfSemiEdit.loc[x]['vencedor'] =  dfSemiEdit.loc[x]['jogoV']
            perdedor.append(dfSemiEdit.loc[x]['jogoM'])

    
    if dfSemiEdit.loc[0]['vencedor'] ==  "Empate":
        dfSemiEdit.loc[0]['vencedor'] = col2.selectbox("Vencedor do Jogo 1 - Semi",("Empate", dfSemiEdit.loc[0]['jogoM'], dfSemiEdit.loc[0]['jogoV']))
        if dfSemiEdit.loc[0]['vencedor'] == (dfSemiEdit.loc[0]['jogoM']):
            perdedor.append(dfSemiEdit.loc[0]['jogoV'])
        else:
            perdedor.append(dfSemiEdit.loc[0]['jogoM'])
            


    if dfSemiEdit.loc[1]['vencedor'] ==  "Empate":
        dfSemiEdit.loc[1]['vencedor'] = col2.selectbox("Vencedor do Jogo 2 - Semi",("Empate", dfSemiEdit.loc[1]['jogoM'], dfSemiEdit.loc[1]['jogoV']))
        if dfSemiEdit.loc[1]['vencedor'] == (dfSemiEdit.loc[1]['jogoM']):
            perdedor.append(dfSemiEdit.loc[1]['jogoV'])
        else:
            perdedor.append(dfSemiEdit.loc[1]['jogoM'])


    v1Flag = dfClass.loc[dfClass['selecao'] == dfSemiEdit.loc[0]['vencedor'], 'flag'].unique()
    v2Flag = dfClass.loc[dfClass['selecao'] == dfSemiEdit.loc[1]['vencedor'], 'flag'].unique()
    v3Flag = dfClass.loc[dfClass['selecao'] == perdedor[0], 'flag'].unique()
    v4Flag = dfClass.loc[dfClass['selecao'] == perdedor[1], 'flag'].unique()

except:
    pass


try:
    dfFinal.loc[0] = ["Tabela Mestre",1,dfSemiEdit.loc[0]['vencedor'],v1Flag[0],None,None,v2Flag[0],dfSemiEdit.loc[1]['vencedor'],'','final']
    dfTerceiro.loc[0] = ["Tabela Mestre",1,perdedor[0],v3Flag[0],None,None,v4Flag[0],perdedor[1],'','terceiro']

    col1.markdown("### FINAL")
    dfFinalEdit = col1.data_editor(dfFinal,
            column_config={"imgM": st.column_config.ImageColumn(),
                            "imgV": st.column_config.ImageColumn()},
            disabled = ["participante","id", "jogoM", "imgM", "imgV", "jogoV", "vencedor", "grupo"],hide_index=True)
    

    if dfFinalEdit.loc[0]['placarM'] > dfFinalEdit.loc[0]['placarV']:
        dfFinalEdit.loc[0]['vencedor'] =  dfFinalEdit.loc[0]['jogoM']          
    elif dfFinalEdit.loc[0]['placarM'] == dfFinalEdit.loc[0]['placarV']:
        dfFinalEdit.loc[0]['vencedor'] =  "Empate"
    else:
        dfFinalEdit.loc[0]['vencedor'] =  dfFinalEdit.loc[0]['jogoV']

    if dfFinalEdit.loc[0]['vencedor'] ==  "Empate":
        dfFinalEdit.loc[0]['vencedor'] = col2.selectbox("CAMPEÃO",("Empate", dfFinalEdit.loc[0]['jogoM'], dfFinalEdit.loc[0]['jogoV']))

    col1.markdown("### TERCEIRO LUGAR")
    dfTerceiroEdit = col1.data_editor(dfTerceiro,
                column_config={"imgM": st.column_config.ImageColumn(),
                                "imgV": st.column_config.ImageColumn()},
                    disabled = ["participante","id", "jogoM", "imgM", "imgV", "jogoV", "vencedor", "grupo"],hide_index=True)
    
    if dfTerceiroEdit.loc[0]['placarM'] > dfTerceiroEdit.loc[0]['placarV']:
        dfTerceiroEdit.loc[0]['vencedor'] =  dfTerceiroEdit.loc[0]['jogoM']          
    elif dfTerceiroEdit.loc[0]['placarM'] == dfTerceiroEdit.loc[0]['placarV']:
        dfTerceiroEdit.loc[0]['vencedor'] =  "Empate"
    else:
        dfTerceiroEdit.loc[0]['vencedor'] =  dfTerceiroEdit.loc[0]['jogoV']
    
    if dfTerceiroEdit.loc[0]['vencedor'] ==  "Empate":
        dfTerceiroEdit.loc[0]['vencedor'] = col2.selectbox("Terceiro Lugar:",("Empate", dfFinalEdit.loc[0]['jogoM'], dfFinalEdit.loc[0]['jogoV']))



except:
    pass


qtdJogos = [x + 1 for x in range(0,32)]

dfTabela = pd.DataFrame(index=qtdJogos, columns=tabelaMestre[0].keys())

dfTabela = df

for x in range(0,4):
    dfTabela.append(dfQuartasEdit.loc[x].to_dict())

try:
    if dfSemiEdit is not None: 
        for x in range(0,2):
            dfTabela.append(dfSemiEdit.loc[x].to_dict())
except:
    pass

try:
    if dfFinalEdit is not None: 
        for x in range(0,1):
            dfTabela.append(dfFinalEdit.loc[x].to_dict())
except:
    pass

try:
    for x in range(0,1):
        dfTabela.append(dfTerceiroEdit.loc[x].to_dict())
except:
    pass

#csvFile = open("c:\\temp\\BolaoCopa.csv", "w")


dfTabelaPart = pd.DataFrame(dfTabela)

dfTabelaPart['participante'] = participante

if col1.button("Salvar Palpites"):  
    csvFile = "BolaoCopaAmerica2024_" + participante + ".csv"
    dfTabelaPart.to_csv(csvFile,sep=';', decimal=',' )
    st.write("**Arquivo: " + csvFile + " gerado com sucesso!**")

    with open(csvFile) as f:
        col1.download_button('Download CSV', f, csvFile)





#---------------------------------------------------------------------
# Comparação ENADE
# Al Richard - IME XXIV
#---------------------------------------------------------------------
# Módulos
#---------------------------------------------------------------------

from typing import List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as pyo

#---------------------------------------------------------------------
# Dados
#---------------------------------------------------------------------

df = pd.read_csv('enade_2019.csv')[['sigla', 'area', 'conceito']]

#---------------------------------------------------------------------
# Plots
#---------------------------------------------------------------------

def plotar_comparacao_estatisticas(a: List, b: List, univ: str) -> None:
    '''
        Recebe as estatísticas de duas universidades e plota
        um gráfico de barras comparando ambas.
    '''
    labels = ['Média', 'Desvio', 'Variância', 'Mediana']

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, a, width, label='IME')
    rects2 = ax.bar(x + width/2, b, width, label=univ)

    ax.set_ylabel('Conceito ENADE')
    ax.set_title('Estatísticas de Conceito ENADE')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    fig.tight_layout()
    plt.show()

def plotar_estrela(nome: str, conceitos_df: pd.DataFrame) -> None:
    '''
        Recebe o nome de uma universidade e um dataframe com
        o conceito ENADE de suas especialidades, e o exibe
        em um gráfico estrelado.
    '''
    categorias = conceitos_df['area'].values.tolist()
    conceitos = conceitos_df['conceito'].values.tolist()
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=conceitos,
        theta=categorias,
        fill='toself',
        name=nome
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 5]
        )),
    showlegend=False
    )

    pyo.plot(fig)

def plotar_histograma(nome: str, conceitos: List) -> None:
    '''
        Recebe o nome de uma universidade e uma lista dos
        conceitos ENADE de suas especialidades, exibindo um
        histograma com os resultados.
    '''
    plt.title(f'Histograma de Conceitos das Engenharias - {nome}')
    plt.hist(conceitos, rwidth=0.9, )
    plt.show()

#---------------------------------------------------------------------
# Entrada
#---------------------------------------------------------------------

print('+------------------------------------------------------+')
print('|                  COMPARADOR ENADE                    |')
print('+------------------------------------------------------+')

univ_invalida = True
while univ_invalida:
    univ = input(' > Sigla da instituição concorrente: ').upper()
    if univ in [str(sigla).upper() for sigla in df['sigla'].values]:
        univ_invalida = False
    else: print('   (!) Universidade desconhecida.')
print('+------------------------------------------------------+')

# Estatísticas da instituição
dupla_df = df.loc[df['sigla'].isin(['IME', univ])]
medias = dupla_df.groupby(['sigla'])['conceito'].mean()
desvios = dupla_df.groupby(['sigla'])['conceito'].std()
variancias = dupla_df.groupby(['sigla'])['conceito'].var()
medianas = dupla_df.groupby(['sigla'])['conceito'].median()
estats_ime = [medias['IME'], desvios['IME'], variancias['IME'], medianas['IME']]
estats_univ = [medias[univ], desvios[univ], variancias[univ], medianas[univ]]

# Estatísticas das especialidades
ime_df = df.loc[df['sigla'] == 'IME']
univ_df = df.loc[df['sigla'] == univ]

# Histogramas
plotar_histograma('IME', ime_df['conceito'].values.tolist())
plotar_histograma(univ, univ_df['conceito'].values.tolist())

# Comparação
plotar_comparacao_estatisticas(estats_ime, estats_univ, univ)

# Estrelas
plotar_estrela('IME', ime_df)
plotar_estrela(univ, univ_df)

#---------------------------------------------------------------------
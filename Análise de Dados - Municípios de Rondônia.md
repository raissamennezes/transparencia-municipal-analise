# Análise de Dados - Municípios de Rondônia

## Projeto: Conformidade e Maturidade em Dados Abertos Orçamentários

**Autora**: Raissa da Silva de Menezes Korehisa  
**Disciplina**: Análise de Dados  
**Programa**: Mestrado em Governança e Transformação Digital

---

## Estrutura do Projeto

### Notebooks Desenvolvidos

#### 1. **01_exploracao_inicial_completo.ipynb**
**Objetivo**: Exploração inicial e segmentação dos municípios de Rondônia

**Conteúdo**:
- Carregamento de dados de população (IBGE 2024) e PIB (IBGE 2021)
- Integração e preparação dos datasets
- Análise exploratória com estatísticas descritivas
- Visualizações da distribuição populacional e econômica
- Criação de rankings por população, PIB e ranking combinado
- **Seleção dos 10 municípios** para análise aprofundada
- Análise de correlação entre população e PIB
- Geração de gráficos e visualizações

**Critério de Seleção**:
Os 10 municípios foram selecionados com base em um **ranking combinado** que considera:
- População (IBGE 2024)
- PIB Municipal (IBGE 2021)

Este critério garante representatividade econômica e demográfica do estado.

**Outputs**:
- `municipios_selecionados.csv`
- `municipios_selecionados_final.csv`
- Gráficos: `distribuicao_populacional.png`, `distribuicao_pib.png`, `top10_populacao.png`, `top10_pib.png`, `populacao_vs_pib.png`, `matriz_correlacao.png`

---

#### 2. **02_coleta_atricon_completo.ipynb**
**Objetivo**: Coleta e análise dos dados de transparência pública (ATRICON)

**Conteúdo**:
- Carregamento dos dados ATRICON (Programa Nacional de Transparência Pública - 2024)
- Filtro de municípios de Rondônia (Poder Executivo)
- Integração com os 10 municípios selecionados
- Análise descritiva dos indicadores de transparência
- Ranking de transparência dos municípios selecionados
- Visualizações comparativas
- Análise de correlação entre indicadores socioeconômicos e transparência
- Comparação dos índices de avaliação, validação e final

**Indicadores ATRICON**:
- **Índice de Avaliação**: Avaliação inicial da transparência
- **Índice de Validação**: Validação dos dados publicados
- **Índice Final**: Índice consolidado de transparência
- **Essenciais**: Percentual de itens essenciais atendidos
- **Nível**: Classificação (Diamante, Ouro, Prata, Intermediário, Básico, Inicial, Inexistente)

**Outputs**:
- `municipios_com_transparencia.csv`
- Gráficos: `ranking_transparencia_atricon.png`, `populacao_vs_transparencia.png`, `pib_vs_transparencia.png`, `matriz_correlacao_completa.png`, `comparacao_indices_atricon.png`

---

## Dados Utilizados

### Fontes de Dados

| Fonte | Descrição | Ano de Referência | Arquivo |
|-------|-----------|-------------------|---------|
| IBGE | Estimativas da População Residente | 2024 | `populacao_rondonia_2024.txt` |
| IBGE/SIDRA | Produto Interno Bruto dos Municípios (Tabela 5938) | 2021 | `pib_municipios_rondonia_2021.csv` |
| ATRICON | Programa Nacional de Transparência Pública | 2024 | `avaliacoes_pntp_2024.csv` |

### Municípios de Rondônia
- **Total**: 52 municípios
- **Selecionados para análise**: 10 municípios

---

## Top 10 Municípios Selecionados

Baseado no ranking combinado (População + PIB):

1. **Porto Velho** - Capital do estado
2. **Ji-Paraná** - Principal polo da região central
3. **Vilhena** - Importante centro do sul do estado
4. **Ariquemes** - Polo regional
5. **Cacoal** - Centro econômico
6. **Jaru** - Município agrícola
7. **Pimenta Bueno** - Centro comercial
8. **Rolim de Moura** - Polo educacional
9. **Guajará-Mirim** - Fronteira com a Bolívia
10. **Ouro Preto do Oeste** - Município agrícola

**Representatividade**:
- População: ~75% da população total do estado
- PIB: ~80% do PIB total do estado

---

## Resultados Preliminares

### Características Demográficas e Econômicas

- **População total de Rondônia**: ~1.746.227 habitantes (2024)
- **PIB total de Rondônia**: ~R$ 51 bilhões (2021)
- **Forte correlação** entre população e PIB (r > 0.95)
- **Porto Velho** representa ~30% da população e ~40% do PIB do estado

### Transparência Pública (ATRICON)

- Variação significativa nos índices de transparência entre os municípios
- Não há correlação direta entre tamanho do município e nível de transparência
- Alguns municípios menores apresentam melhores índices que municípios maiores

---

## Como Executar os Notebooks

### Requisitos

```bash
pip install pandas numpy matplotlib seaborn scipy openpyxl
```

### Ordem de Execução

1. **Notebook 1**: `01_exploracao_inicial_completo.ipynb`
   - Executa a exploração inicial e seleciona os 10 municípios
   - Gera o arquivo `municipios_selecionados_final.csv`

2. **Notebook 2**: `02_coleta_atricon_completo.ipynb`
   - Carrega os municípios selecionados
   - Integra com dados de transparência ATRICON
   - Gera análises comparativas

### Estrutura de Arquivos

```
mestrado_analise/
├── README.md
├── 01_exploracao_inicial_completo.ipynb
├── 02_coleta_atricon_completo.ipynb
├── 03_analise_transparencia.ipynb (a ser desenvolvido)
├── 04_analise_comparativa.ipynb (a ser desenvolvido)
├── avaliacoes_pntp_2024.csv
├── pib_municipios_rondonia_2021.csv
├── populacao_rondonia_2024.txt
├── municipios_selecionados_final.csv (gerado pelo notebook 1)
├── municipios_com_transparencia.csv (gerado pelo notebook 2)
└── [gráficos gerados]
```

---

## Próximos Passos

### Notebook 3: Análise de Transparência
- Avaliação detalhada de conformidade com normas brasileiras
- Análise de aderência aos princípios FAIR
- Identificação de lacunas e barreiras

### Notebook 4: Análise Comparativa
- Comparação entre municípios
- Identificação de padrões e boas práticas
- Proposição de diretrizes para melhoria

---

## Observações Metodológicas

### Limitações dos Dados

1. **PIB Municipal**: Último ano disponível é 2021 (defasagem de 3 anos)
2. **População**: Estimativas do IBGE (não são dados censitários)
3. **Transparência**: Avaliação pontual (ciclo 2024 do PNTP)

### Considerações

- A análise considera apenas o **Poder Executivo Municipal** (Prefeituras)
- Não foram incluídas Câmaras Municipais ou outros poderes
- Os dados de transparência são baseados em avaliação externa (ATRICON)

---

## Referências

- IBGE - Instituto Brasileiro de Geografia e Estatística
- ATRICON - Associação dos Membros dos Tribunais de Contas do Brasil
- Programa Nacional de Transparência Pública (PNTP)
- Lei Complementar 131/2009 (Lei da Transparência)
- Lei 12.527/2011 (Lei de Acesso à Informação)
- Decreto 8.777/2016 (Política de Dados Abertos)

---

## Contato

**Raissa da Silva de Menezes Korehisa**  
Mestranda em Governança e Transformação Digital  
Disciplina: Análise de Dados

---

**Data de criação**: Novembro de 2024  
**Última atualização**: 12/11/2024

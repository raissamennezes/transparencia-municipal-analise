#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
GERADOR DE VISUALIZAÇÕES - CENSO DE MUNICÍPIOS DE RONDÔNIA
═══════════════════════════════════════════════════════════════════════════════

Script para gerar gráficos e visualizações dos dados dos 52 municípios de
Rondônia para a pesquisa sobre dados abertos orçamentários.

Autor: Pesquisa Framework LLM-Ready
Data: Novembro 2025
═══════════════════════════════════════════════════════════════════════════════
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ═══════════════════════════════════════════════════════════════════════════════

CONFIG = {
    'ARQUIVO_ENTRADA': 'Avaliacao_Municipios_Rondonia_Preenchido.xlsx',
    'PASTA_SAIDA': 'graficos_censo',
    'DPI': 300,  # Qualidade das imagens (300 = alta qualidade)
    'FORMATO': 'png',  # Formato: png, jpg, pdf, svg
}

# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE VISUALIZAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

def criar_pasta_saida():
    """Cria pasta para salvar os gráficos"""
    pasta = Path(CONFIG['PASTA_SAIDA'])
    pasta.mkdir(exist_ok=True)
    return pasta

def carregar_dados():
    """Carrega dados da planilha"""
    print("\n" + "="*80)
    print("📊 Carregando dados da planilha...")
    print("="*80)
    
    try:
        df = pd.read_excel(CONFIG['ARQUIVO_ENTRADA'], sheet_name='Fase1_Atributos')
        
        # Extrair mesorregião
        df['Mesorregiao'] = df['Mesorregião / Microrregião'].str.split(' / ').str[0]
        
        print(f"✓ Dados carregados: {len(df)} municípios")
        print(f"✓ População total: {df['População (IBGE/2024)'].sum():,} habitantes")
        
        return df
        
    except FileNotFoundError:
        print(f"\n❌ ERRO: Arquivo '{CONFIG['ARQUIVO_ENTRADA']}' não encontrado!")
        print("   Certifique-se de que a planilha está no mesmo diretório.")
        return None
    except Exception as e:
        print(f"\n❌ ERRO ao carregar dados: {e}")
        return None

def grafico_1_distribuicao_populacional(df, pasta_saida):
    """
    Gráfico 1: Distribuição populacional com maiores e menores municípios
    """
    print("\n📊 Gerando Gráfico 1: Distribuição populacional...")
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle('DISTRIBUIÇÃO POPULACIONAL DOS MUNICÍPIOS DE RONDÔNIA\n' + 
                 'Análise dos Extremos - Dados IBGE 2024',
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Gráfico 1A: 10 Maiores municípios
    ax1 = axes[0]
    df_maiores = df.nlargest(10, 'População (IBGE/2024)')
    cores_maiores = plt.cm.Blues(np.linspace(0.4, 0.9, 10))
    
    bars1 = ax1.barh(df_maiores['Município'], df_maiores['População (IBGE/2024)'], 
                     color=cores_maiores, edgecolor='black', linewidth=0.5)
    
    ax1.set_xlabel('População (habitantes)', fontweight='bold', fontsize=12)
    ax1.set_title('10 MAIORES Municípios por População', fontweight='bold', fontsize=13)
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Adicionar valores nas barras
    for i, (bar, pop) in enumerate(zip(bars1, df_maiores['População (IBGE/2024)'])):
        ax1.text(pop + 5000, bar.get_y() + bar.get_height()/2, 
                f'{pop:,.0f}', va='center', fontsize=9, fontweight='bold')
    
    # Gráfico 1B: 10 Menores municípios
    ax2 = axes[1]
    df_menores = df.nsmallest(10, 'População (IBGE/2024)')
    cores_menores = plt.cm.Oranges(np.linspace(0.4, 0.9, 10))
    
    bars2 = ax2.barh(df_menores['Município'], df_menores['População (IBGE/2024)'], 
                     color=cores_menores, edgecolor='black', linewidth=0.5)
    
    ax2.set_xlabel('População (habitantes)', fontweight='bold', fontsize=12)
    ax2.set_title('10 MENORES Municípios por População', fontweight='bold', fontsize=13)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Adicionar valores nas barras
    for bar, pop in zip(bars2, df_menores['População (IBGE/2024)']):
        ax2.text(pop + 100, bar.get_y() + bar.get_height()/2, 
                f'{pop:,.0f}', va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    arquivo = pasta_saida / f'01_distribuicao_populacional.{CONFIG["FORMATO"]}'
    plt.savefig(arquivo, dpi=CONFIG['DPI'], bbox_inches='tight')
    plt.close()
    
    print(f"✓ Salvo: {arquivo}")

def grafico_2_distribuicao_mesorregiao(df, pasta_saida):
    """
    Gráfico 2: Distribuição por mesorregião (pizza + barras)
    """
    print("\n📊 Gerando Gráfico 2: Distribuição por mesorregião...")
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle('DISTRIBUIÇÃO DOS MUNICÍPIOS POR MESORREGIÃO\n' + 
                 'Estado de Rondônia - 52 Municípios',
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Contar municípios por mesorregião
    contagem = df['Mesorregiao'].value_counts()
    
    # Gráfico 2A: Pizza
    ax1 = axes[0]
    cores = ['#FF9999', '#66B3FF']
    explode = (0.05, 0.05)
    
    wedges, texts, autotexts = ax1.pie(contagem.values, 
                                        labels=contagem.index,
                                        autopct='%1.1f%%',
                                        colors=cores,
                                        explode=explode,
                                        startangle=90,
                                        shadow=True,
                                        textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    # Melhorar visualização dos textos
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
    
    ax1.set_title('Proporção de Municípios por Mesorregião', 
                 fontweight='bold', fontsize=13, pad=20)
    
    # Gráfico 2B: Barras com detalhes
    ax2 = axes[1]
    
    # Calcular população por mesorregião
    pop_mesorregiao = df.groupby('Mesorregiao')['População (IBGE/2024)'].agg(['sum', 'mean', 'count'])
    
    x = np.arange(len(pop_mesorregiao))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, pop_mesorregiao['count'], width, 
                    label='Nº de Municípios', color='#66B3FF', edgecolor='black')
    
    ax2_twin = ax2.twinx()
    bars2 = ax2_twin.bar(x + width/2, pop_mesorregiao['sum']/1000, width,
                         label='População Total (milhares)', color='#FF9999', 
                         edgecolor='black', alpha=0.7)
    
    ax2.set_xlabel('Mesorregião', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Número de Municípios', fontweight='bold', fontsize=12)
    ax2_twin.set_ylabel('População Total (milhares)', fontweight='bold', fontsize=12)
    ax2.set_title('Municípios e População por Mesorregião', 
                 fontweight='bold', fontsize=13)
    ax2.set_xticks(x)
    ax2.set_xticklabels(pop_mesorregiao.index, fontsize=11)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adicionar valores
    for bar in bars1:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    # Legendas
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.tight_layout()
    arquivo = pasta_saida / f'02_distribuicao_mesorregiao.{CONFIG["FORMATO"]}'
    plt.savefig(arquivo, dpi=CONFIG['DPI'], bbox_inches='tight')
    plt.close()
    
    print(f"✓ Salvo: {arquivo}")

def grafico_3_histograma_populacional(df, pasta_saida):
    """
    Gráfico 3: Histograma da distribuição populacional
    """
    print("\n📊 Gerando Gráfico 3: Histograma populacional...")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.suptitle('DISTRIBUIÇÃO POPULACIONAL DOS 52 MUNICÍPIOS\n' + 
                 'Histograma com Medidas de Tendência Central',
                 fontsize=16, fontweight='bold')
    
    # Criar histograma
    n, bins, patches = ax.hist(df['População (IBGE/2024)'], 
                               bins=20, 
                               color='lightgreen', 
                               edgecolor='black',
                               alpha=0.7,
                               linewidth=1.5)
    
    # Colorir barras por gradiente
    cm = plt.cm.RdYlGn
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    # Adicionar linhas de referência
    media = df['População (IBGE/2024)'].mean()
    mediana = df['População (IBGE/2024)'].median()
    
    ax.axvline(media, color='blue', linestyle='--', linewidth=2.5,
              label=f'Média: {media:,.0f} hab', alpha=0.8)
    ax.axvline(mediana, color='red', linestyle='--', linewidth=2.5,
              label=f'Mediana: {mediana:,.0f} hab', alpha=0.8)
    
    # Adicionar área sombreada para 1 desvio padrão
    std = df['População (IBGE/2024)'].std()
    ax.axvspan(media - std, media + std, alpha=0.2, color='yellow',
              label=f'± 1 Desvio Padrão')
    
    ax.set_xlabel('População (habitantes)', fontweight='bold', fontsize=13)
    ax.set_ylabel('Frequência (nº de municípios)', fontweight='bold', fontsize=13)
    ax.set_title('Distribuição de Frequências', fontweight='bold', fontsize=14, pad=20)
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(alpha=0.3, linestyle='--')
    
    # Adicionar texto com estatísticas
    texto_stats = f"""
    ESTATÍSTICAS DESCRITIVAS:
    • Total: {len(df)} municípios
    • Média: {media:,.0f} habitantes
    • Mediana: {mediana:,.0f} habitantes
    • Desvio Padrão: {std:,.0f}
    • Mín: {df['População (IBGE/2024)'].min():,.0f}
    • Máx: {df['População (IBGE/2024)'].max():,.0f}
    """
    
    ax.text(0.98, 0.97, texto_stats,
           transform=ax.transAxes,
           fontsize=10,
           verticalalignment='top',
           horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    arquivo = pasta_saida / f'03_histograma_populacional.{CONFIG["FORMATO"]}'
    plt.savefig(arquivo, dpi=CONFIG['DPI'], bbox_inches='tight')
    plt.close()
    
    print(f"✓ Salvo: {arquivo}")

def grafico_4_boxplot_comparativo(df, pasta_saida):
    """
    Gráfico 4: Boxplot comparativo entre mesorregiões
    """
    print("\n📊 Gerando Gráfico 4: Boxplot comparativo...")
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle('ANÁLISE COMPARATIVA ENTRE MESORREGIÕES\n' + 
                 'Distribuição Populacional - Boxplot e Violin Plot',
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Gráfico 4A: Boxplot
    ax1 = axes[0]
    bp = ax1.boxplot([df[df['Mesorregiao'] == 'Madeira-Guaporé']['População (IBGE/2024)'],
                       df[df['Mesorregiao'] == 'Leste Rondoniense']['População (IBGE/2024)']],
                      labels=['Madeira-Guaporé', 'Leste Rondoniense'],
                      patch_artist=True,
                      notch=True,
                      showmeans=True)
    
    # Colorir boxes
    cores = ['#FF9999', '#66B3FF']
    for patch, cor in zip(bp['boxes'], cores):
        patch.set_facecolor(cor)
        patch.set_alpha(0.7)
    
    ax1.set_ylabel('População (habitantes)', fontweight='bold', fontsize=12)
    ax1.set_title('Boxplot - Comparação de Distribuições', fontweight='bold', fontsize=13)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_yscale('log')  # Escala logarítmica para melhor visualização
    
    # Gráfico 4B: Violin plot
    ax2 = axes[1]
    parts = ax2.violinplot([df[df['Mesorregiao'] == 'Madeira-Guaporé']['População (IBGE/2024)'],
                            df[df['Mesorregiao'] == 'Leste Rondoniense']['População (IBGE/2024)']],
                           positions=[1, 2],
                           showmeans=True,
                           showmedians=True)
    
    # Colorir violins
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(cores[i])
        pc.set_alpha(0.7)
    
    ax2.set_xticks([1, 2])
    ax2.set_xticklabels(['Madeira-Guaporé', 'Leste Rondoniense'])
    ax2.set_ylabel('População (habitantes)', fontweight='bold', fontsize=12)
    ax2.set_title('Violin Plot - Densidade da Distribuição', fontweight='bold', fontsize=13)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_yscale('log')
    
    plt.tight_layout()
    arquivo = pasta_saida / f'04_boxplot_comparativo.{CONFIG["FORMATO"]}'
    plt.savefig(arquivo, dpi=CONFIG['DPI'], bbox_inches='tight')
    plt.close()
    
    print(f"✓ Salvo: {arquivo}")

def grafico_5_ranking_completo(df, pasta_saida):
    """
    Gráfico 5: Ranking completo de todos os 52 municípios
    """
    print("\n📊 Gerando Gráfico 5: Ranking completo...")
    
    fig, ax = plt.subplots(figsize=(12, 20))
    fig.suptitle('RANKING COMPLETO DOS 52 MUNICÍPIOS DE RONDÔNIA\n' + 
                 'Ordenados por População - IBGE 2024',
                 fontsize=16, fontweight='bold')
    
    # Ordenar por população
    df_sorted = df.sort_values('População (IBGE/2024)', ascending=True)
    
    # Criar cores gradientes
    norm = plt.Normalize(df_sorted['População (IBGE/2024)'].min(), 
                        df_sorted['População (IBGE/2024)'].max())
    cores = plt.cm.RdYlGn(norm(df_sorted['População (IBGE/2024)']))
    
    # Criar barras
    bars = ax.barh(range(len(df_sorted)), df_sorted['População (IBGE/2024)'],
                   color=cores, edgecolor='black', linewidth=0.5)
    
    # Configurar eixos
    ax.set_yticks(range(len(df_sorted)))
    ax.set_yticklabels([f"{i+1}. {mun}" for i, mun in enumerate(df_sorted['Município'])],
                       fontsize=8)
    ax.set_xlabel('População (habitantes)', fontweight='bold', fontsize=12)
    ax.set_title('Ordem Crescente de População', fontweight='bold', fontsize=13, pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Adicionar valores
    for i, (bar, pop) in enumerate(zip(bars, df_sorted['População (IBGE/2024)'])):
        ax.text(pop + 2000, bar.get_y() + bar.get_height()/2, 
                f'{pop:,.0f}', va='center', fontsize=7)
    
    plt.tight_layout()
    arquivo = pasta_saida / f'05_ranking_completo.{CONFIG["FORMATO"]}'
    plt.savefig(arquivo, dpi=CONFIG['DPI'], bbox_inches='tight')
    plt.close()
    
    print(f"✓ Salvo: {arquivo}")

def grafico_6_analise_estratificada(df, pasta_saida):
    """
    Gráfico 6: Análise por estratos populacionais
    """
    print("\n📊 Gerando Gráfico 6: Análise estratificada...")
    
    # Criar estratos
    def classificar_porte(pop):
        if pop >= 100000:
            return 'Grande (>100k)'
        elif pop >= 30000:
            return 'Médio (30-100k)'
        elif pop >= 10000:
            return 'Pequeno (10-30k)'
        else:
            return 'Muito Pequeno (<10k)'
    
    df['Porte'] = df['População (IBGE/2024)'].apply(classificar_porte)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('ANÁLISE ESTRATIFICADA POR PORTE POPULACIONAL\n' + 
                 'Classificação dos 52 Municípios',
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Gráfico 6A: Contagem por porte
    ax1 = axes[0, 0]
    contagem_porte = df['Porte'].value_counts()
    ordem = ['Grande (>100k)', 'Médio (30-100k)', 'Pequeno (10-30k)', 'Muito Pequeno (<10k)']
    contagem_porte = contagem_porte.reindex(ordem)
    
    cores_porte = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    bars = ax1.bar(range(len(contagem_porte)), contagem_porte.values,
                   color=cores_porte, edgecolor='black', linewidth=1.5)
    
    ax1.set_xticks(range(len(contagem_porte)))
    ax1.set_xticklabels(contagem_porte.index, rotation=15, ha='right')
    ax1.set_ylabel('Número de Municípios', fontweight='bold')
    ax1.set_title('Distribuição por Porte', fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Adicionar valores
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}\n({int(height)/52*100:.1f}%)',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Gráfico 6B: População por porte
    ax2 = axes[0, 1]
    pop_porte = df.groupby('Porte')['População (IBGE/2024)'].sum().reindex(ordem)
    
    bars2 = ax2.bar(range(len(pop_porte)), pop_porte.values/1000,
                    color=cores_porte, edgecolor='black', linewidth=1.5)
    
    ax2.set_xticks(range(len(pop_porte)))
    ax2.set_xticklabels(pop_porte.index, rotation=15, ha='right')
    ax2.set_ylabel('População Total (milhares)', fontweight='bold')
    ax2.set_title('População Total por Porte', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Adicionar valores
    for bar, pop in zip(bars2, pop_porte.values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{pop/1000:.0f}k\n({pop/df["População (IBGE/2024)"].sum()*100:.1f}%)',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Gráfico 6C: Pizza - proporção populacional
    ax3 = axes[1, 0]
    wedges, texts, autotexts = ax3.pie(pop_porte.values,
                                        labels=[p.replace(' ', '\n') for p in pop_porte.index],
                                        autopct='%1.1f%%',
                                        colors=cores_porte,
                                        startangle=90,
                                        textprops={'fontsize': 9})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax3.set_title('Proporção da População por Porte', fontweight='bold')
    
    # Gráfico 6D: Média populacional por porte
    ax4 = axes[1, 1]
    media_porte = df.groupby('Porte')['População (IBGE/2024)'].mean().reindex(ordem)
    
    bars4 = ax4.bar(range(len(media_porte)), media_porte.values/1000,
                    color=cores_porte, edgecolor='black', linewidth=1.5)
    
    ax4.set_xticks(range(len(media_porte)))
    ax4.set_xticklabels(media_porte.index, rotation=15, ha='right')
    ax4.set_ylabel('População Média (milhares)', fontweight='bold')
    ax4.set_title('Média Populacional por Porte', fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    # Adicionar valores
    for bar, pop in zip(bars4, media_porte.values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{pop/1000:.1f}k',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    arquivo = pasta_saida / f'06_analise_estratificada.{CONFIG["FORMATO"]}'
    plt.savefig(arquivo, dpi=CONFIG['DPI'], bbox_inches='tight')
    plt.close()
    
    print(f"✓ Salvo: {arquivo}")

def grafico_7_dashboard_completo(df, pasta_saida):
    """
    Gráfico 7: Dashboard resumo com principais indicadores
    """
    print("\n📊 Gerando Gráfico 7: Dashboard completo...")
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    fig.suptitle('DASHBOARD - CENSO MUNICIPAL DE RONDÔNIA\n' + 
                 'Visão Geral dos 52 Municípios - IBGE 2024',
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Painel 1: Estatísticas gerais (texto)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    
    stats_text = f"""
    📊 ESTATÍSTICAS GERAIS
    
    Total de Municípios: {len(df)}
    
    População Total: {df['População (IBGE/2024)'].sum():,.0f}
    
    População Média: {df['População (IBGE/2024)'].mean():,.0f}
    
    População Mediana: {df['População (IBGE/2024)'].median():,.0f}
    
    Desvio Padrão: {df['População (IBGE/2024)'].std():,.0f}
    
    Maior Município:
    {df.loc[df['População (IBGE/2024)'].idxmax(), 'Município']}
    ({df['População (IBGE/2024)'].max():,.0f} hab)
    
    Menor Município:
    {df.loc[df['População (IBGE/2024)'].idxmin(), 'Município']}
    ({df['População (IBGE/2024)'].min():,.0f} hab)
    """
    
    ax1.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
            verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Painel 2: Top 5 maiores
    ax2 = fig.add_subplot(gs[0, 1:])
    top5 = df.nlargest(5, 'População (IBGE/2024)')
    ax2.barh(top5['Município'], top5['População (IBGE/2024)'],
            color=plt.cm.Blues(np.linspace(0.4, 0.9, 5)))
    ax2.set_title('Top 5 Maiores Municípios', fontweight='bold', fontsize=12)
    ax2.set_xlabel('População')
    ax2.grid(axis='x', alpha=0.3)
    
    # Painel 3: Distribuição por mesorregião
    ax3 = fig.add_subplot(gs[1, 0])
    contagem = df['Mesorregiao'].value_counts()
    ax3.pie(contagem.values, labels=contagem.index, autopct='%1.1f%%',
           colors=['#FF9999', '#66B3FF'], startangle=90)
    ax3.set_title('Distribuição por Mesorregião', fontweight='bold', fontsize=12)
    
    # Painel 4: Histograma
    ax4 = fig.add_subplot(gs[1, 1:])
    ax4.hist(df['População (IBGE/2024)'], bins=15, color='lightgreen',
            edgecolor='black', alpha=0.7)
    ax4.axvline(df['População (IBGE/2024)'].mean(), color='blue',
               linestyle='--', linewidth=2, label='Média')
    ax4.axvline(df['População (IBGE/2024)'].median(), color='red',
               linestyle='--', linewidth=2, label='Mediana')
    ax4.set_title('Distribuição Populacional', fontweight='bold', fontsize=12)
    ax4.set_xlabel('População')
    ax4.set_ylabel('Frequência')
    ax4.legend()
    ax4.grid(alpha=0.3)
    
    # Painel 5: Ranking top 15
    ax5 = fig.add_subplot(gs[2, :])
    top15 = df.nlargest(15, 'População (IBGE/2024)')
    cores_ranking = plt.cm.viridis(np.linspace(0, 1, 15))
    ax5.barh(range(15), top15['População (IBGE/2024)'], color=cores_ranking)
    ax5.set_yticks(range(15))
    ax5.set_yticklabels([f"{i+1}. {mun}" for i, mun in enumerate(top15['Município'])],
                        fontsize=9)
    ax5.set_title('Top 15 Municípios Mais Populosos', fontweight='bold', fontsize=12)
    ax5.set_xlabel('População')
    ax5.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    arquivo = pasta_saida / f'07_dashboard_completo.{CONFIG["FORMATO"]}'
    plt.savefig(arquivo, dpi=CONFIG['DPI'], bbox_inches='tight')
    plt.close()
    
    print(f"✓ Salvo: {arquivo}")

def gerar_relatorio_texto(df, pasta_saida):
    """
    Gera relatório em texto com estatísticas
    """
    print("\n📝 Gerando relatório textual...")
    
    relatorio = f"""
═══════════════════════════════════════════════════════════════════════════════
RELATÓRIO ESTATÍSTICO - CENSO MUNICIPAL DE RONDÔNIA
═══════════════════════════════════════════════════════════════════════════════

Data: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}
Fonte: IBGE 2024

═══════════════════════════════════════════════════════════════════════════════
1. ESTATÍSTICAS DESCRITIVAS GERAIS
═══════════════════════════════════════════════════════════════════════════════

Total de Municípios: {len(df)}
População Total: {df['População (IBGE/2024)'].sum():,.0f} habitantes

Medidas de Tendência Central:
  • Média: {df['População (IBGE/2024)'].mean():,.2f} habitantes
  • Mediana: {df['População (IBGE/2024)'].median():,.0f} habitantes
  • Moda: {df['População (IBGE/2024)'].mode()[0]:,.0f} habitantes

Medidas de Dispersão:
  • Desvio Padrão: {df['População (IBGE/2024)'].std():,.2f}
  • Variância: {df['População (IBGE/2024)'].var():,.2f}
  • Coeficiente de Variação: {(df['População (IBGE/2024)'].std() / df['População (IBGE/2024)'].mean() * 100):.2f}%

Valores Extremos:
  • Mínimo: {df['População (IBGE/2024)'].min():,.0f} habitantes
  • Máximo: {df['População (IBGE/2024)'].max():,.0f} habitantes
  • Amplitude: {df['População (IBGE/2024)'].max() - df['População (IBGE/2024)'].min():,.0f}

Quartis:
  • Q1 (25%): {df['População (IBGE/2024)'].quantile(0.25):,.0f}
  • Q2 (50%): {df['População (IBGE/2024)'].quantile(0.50):,.0f}
  • Q3 (75%): {df['População (IBGE/2024)'].quantile(0.75):,.0f}
  • IQR: {df['População (IBGE/2024)'].quantile(0.75) - df['População (IBGE/2024)'].quantile(0.25):,.0f}

═══════════════════════════════════════════════════════════════════════════════
2. DISTRIBUIÇÃO POR MESORREGIÃO
═══════════════════════════════════════════════════════════════════════════════

{df.groupby('Mesorregiao').agg({
    'Município': 'count',
    'População (IBGE/2024)': ['sum', 'mean', 'min', 'max']
}).to_string()}

═══════════════════════════════════════════════════════════════════════════════
3. ESTRATIFICAÇÃO POR PORTE POPULACIONAL
═══════════════════════════════════════════════════════════════════════════════

"""
    
    # Classificar por porte
    def classificar_porte(pop):
        if pop >= 100000:
            return 'Grande (>100k)'
        elif pop >= 30000:
            return 'Médio (30-100k)'
        elif pop >= 10000:
            return 'Pequeno (10-30k)'
        else:
            return 'Muito Pequeno (<10k)'
    
    df['Porte'] = df['População (IBGE/2024)'].apply(classificar_porte)
    
    relatorio += df.groupby('Porte').agg({
        'Município': 'count',
        'População (IBGE/2024)': ['sum', 'mean']
    }).to_string()
    
    relatorio += f"""

═══════════════════════════════════════════════════════════════════════════════
4. TOP 10 MAIORES MUNICÍPIOS
═══════════════════════════════════════════════════════════════════════════════

{df.nlargest(10, 'População (IBGE/2024)')[['Município', 'População (IBGE/2024)', 'Mesorregiao']].to_string(index=False)}

═══════════════════════════════════════════════════════════════════════════════
5. TOP 10 MENORES MUNICÍPIOS
═══════════════════════════════════════════════════════════════════════════════

{df.nsmallest(10, 'População (IBGE/2024)')[['Município', 'População (IBGE/2024)', 'Mesorregiao']].to_string(index=False)}

═══════════════════════════════════════════════════════════════════════════════
FIM DO RELATÓRIO
═══════════════════════════════════════════════════════════════════════════════
"""
    
    arquivo = pasta_saida / 'RELATORIO_ESTATISTICO.txt'
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print(f"✓ Salvo: {arquivo}")

# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal - gera todos os gráficos"""
    
    print("\n" + "="*80)
    print(" "*20 + "GERADOR DE VISUALIZAÇÕES")
    print(" "*15 + "Censo Municipal de Rondônia")
    print("="*80)
    
    # Criar pasta de saída
    pasta_saida = criar_pasta_saida()
    print(f"\n✓ Pasta de saída criada: {pasta_saida}")
    
    # Carregar dados
    df = carregar_dados()
    if df is None:
        return
    
    print("\n" + "="*80)
    print("🎨 Gerando visualizações...")
    print("="*80)
    
    try:
        # Gerar cada gráfico
        grafico_1_distribuicao_populacional(df, pasta_saida)
        grafico_2_distribuicao_mesorregiao(df, pasta_saida)
        grafico_3_histograma_populacional(df, pasta_saida)
        grafico_4_boxplot_comparativo(df, pasta_saida)
        grafico_5_ranking_completo(df, pasta_saida)
        grafico_6_analise_estratificada(df, pasta_saida)
        grafico_7_dashboard_completo(df, pasta_saida)
        
        # Gerar relatório textual
        gerar_relatorio_texto(df, pasta_saida)
        
        print("\n" + "="*80)
        print("✅ TODOS OS GRÁFICOS FORAM GERADOS COM SUCESSO!")
        print("="*80)
        print(f"\n📂 Arquivos salvos em: {pasta_saida.absolute()}")
        print("\n📊 Gráficos gerados:")
        print("   1. Distribuição populacional (maiores e menores)")
        print("   2. Distribuição por mesorregião")
        print("   3. Histograma populacional")
        print("   4. Boxplot comparativo")
        print("   5. Ranking completo dos 52 municípios")
        print("   6. Análise estratificada por porte")
        print("   7. Dashboard completo")
        print("   + Relatório estatístico (TXT)")
        
        print("\n💡 Próximos passos:")
        print("   • Abrir os gráficos gerados")
        print("   • Incluir nos slides de apresentação")
        print("   • Usar no artigo científico")
        print("   • Compartilhar com orientador")
        
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO ao gerar gráficos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

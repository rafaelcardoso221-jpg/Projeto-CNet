# Projeto-CNet — Carteira de R$ 5.000 a partir do AUVP11

Estudo de caso: transformar a composição do ETF **AUVP11** (BTG Pactual / AUVP, índice IAFD) em uma carteira enxuta de ações brasileiras de aproximadamente **R$ 5.000**, com análise crítica ativo por ativo e leitura do cenário eleitoral de outubro de 2026.

**Data-base:** 19-20/10/2026 · **Segundo turno:** 25/10/2026 (Flávio Bolsonaro x Lula)

## Entregável principal

📄 **[docs/carteira-5000-AUVP11.md](docs/carteira-5000-AUVP11.md)** — análise completa:
1. O que o ETF realmente é (e as 5 críticas à sua construção)
2. Screening das 34 posições
3. Análise das 9 empresas escolhidas
4. Carteira final de R$ 5.000 (quantidades, preços, pesos)
5. Cenários eleitorais e impacto por ativo
6. Plano de execução em 3 tranches
7. Riscos, calendário e gatilhos de saída

## Resumo da carteira

| Ticker | Empresa | Setor | Peso | Valor |
|---|---|---|---:|---:|
| ITUB4 | Itaú Unibanco | Bancos | 14,8% | R$ 738,30 |
| PETR4 | Petrobras | Petróleo e gás | 11,6% | R$ 578,60 |
| WEGE3 | WEG | Bens de capital | 9,7% | R$ 483,90 |
| BBDC4 | Bradesco | Bancos | 9,6% | R$ 478,40 |
| ABEV3 | Ambev | Bebidas | 9,8% | R$ 488,94 |
| SBSP3 | Sabesp | Saneamento | 9,2% | R$ 459,34 |
| CPFE3 | CPFL Energia | Energia elétrica | 9,1% | R$ 456,57 |
| PSSA3 | Porto Seguro | Seguros | 8,4% | R$ 420,64 |
| TOTS3 | TOTVS | Software | 7,6% | R$ 378,54 |
| — | Caixa / reserva | — | 10,3% | R$ 516,77 |
| | **Total** | | **100%** | **R$ 5.000,00** |

Indicadores ponderados (excluindo caixa): **P/L ~13,4x · ROE ~23,2% · DY trailing ~5,4%**

## Estrutura do repositório

```
data/
  auvp11_composicao_2026-10-19.csv   # ponta comprada do ETF (34 papéis)
  analise_ativos_2026-10-20.csv      # screening: fundamentos, decisão e motivo
scripts/
  montar_carteira.py                 # reproduz a carteira e as 3 tranches
output/
  carteira_5000.csv                  # carteira final (ticker, qtd, preço, valor, peso)
  tranches.csv                       # quantidades por tranche
docs/
  carteira-5000-AUVP11.md            # análise completa
  fontes.md                          # links e qualidade das fontes
```

## Como reproduzir

```bash
python3 scripts/montar_carteira.py
```

O script lê a composição do ETF, calcula a concentração por grupo econômico, monta a carteira com quantidades inteiras e gera os CSVs em `output/`.

## Metodologia (resumo)

- **Fontes:** composição do fundo (planilha de 19/10/2026), Fundamentus (balanços até 30/06/2026), Yahoo Finance (cotações de 20/10/2026), B3/ETFs Brasil (dados do fundo), notícias e relatórios de BTG, XP, Genial, Safra, JPMorgan e Citi, pesquisas eleitorais (Datafolha, AtlasIntel, PoderData, Real Time Big Data, Quaest, Alfa, Gerp) e TSE.
- **Critérios:** qualidade (ROE, margem, alavancagem, governança), preço (P/L, P/VP, EV/EBITDA, DY), liquidez, diversificação real e risco específico.
- **Regra de bolso:** 9 ativos, nenhum setor acima de 25%, nenhum ativo acima de 16%, 10% em caixa para a semana eleitoral.

## Aviso

Material educacional. Não é recomendação personalizada de investimento. Rentabilidade passada não garante retorno futuro. Preços de 20/10/2026 são intradiários (~14h30) e podem mudar. Confira os dados antes de executar qualquer ordem.

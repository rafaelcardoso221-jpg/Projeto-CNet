#!/usr/bin/env python3
"""
Monta a carteira de R$ 5.000 a partir da composição do AUVP11 (19/10/2026).

Etapas:
1. Lê a composição do ETF (apenas a ponta comprada; as linhas de empréstimo
   e os itens contábeis do relatório original se anulam e foram descartados).
2. Confere o valor total e a concentração efetiva por grupo econômico.
3. Aplica a análise crítica (data/analise_ativos_2026-10-20.csv) e monta a
   carteira com 9 ativos, quantidades inteiras e R$ 5.000 no total.
4. Gera output/carteira_5000.csv, output/tranches.csv e imprime o resumo.
"""
import csv
import os
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = os.path.join(BASE, "data", "auvp11_composicao_2026-10-19.csv")
ANALISE = os.path.join(BASE, "data", "analise_ativos_2026-10-20.csv")
OUT = os.path.join(BASE, "output", "carteira_5000.csv")
OUT_TRANCHES = os.path.join(BASE, "output", "tranches.csv")

TOTAL = 5000.00

# Pesos-alvo (definidos na análise crítica; somam 90% do total)
ALVOS = [
    ("ITUB4", 0.16),
    ("PETR4", 0.12),
    ("WEGE3", 0.10),
    ("BBDC4", 0.09),
    ("ABEV3", 0.09),
    ("SBSP3", 0.09),
    ("CPFE3", 0.09),
    ("PSSA3", 0.08),
    ("TOTS3", 0.08),
]

# Preços de referência de 20/10/2026 (~14h30, intradiário)
PRECOS = {
    "ITUB4": 49.22, "PETR4": 57.86, "WEGE3": 48.39, "BBDC4": 20.80,
    "ABEV3": 16.86, "SBSP3": 32.81, "CPFE3": 50.73, "PSSA3": 52.58,
    "TOTS3": 42.06,
}

# Quantidades inteiras que melhor aproximam os pesos-alvo
# (resolvidas por busca exaustiva local; ver histórico do script)
QUANTIDADES = {
    "ITUB4": 15, "PETR4": 10, "WEGE3": 10, "BBDC4": 23, "ABEV3": 29,
    "SBSP3": 14, "CPFE3": 9, "PSSA3": 8, "TOTS3": 9,
}

# Três tranches de compra (somam as quantidades acima)
TRANCHES = {
    "ITUB4": (5, 5, 5), "PETR4": (4, 3, 3), "WEGE3": (3, 4, 3),
    "BBDC4": (8, 8, 7), "ABEV3": (10, 10, 9), "SBSP3": (5, 5, 4),
    "CPFE3": (3, 3, 3), "PSSA3": (3, 3, 2), "TOTS3": (3, 3, 3),
}


def brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def carregar_composicao():
    with open(COMP, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def carregar_analise():
    with open(ANALISE, encoding="utf-8") as f:
        return {r["ticker"]: r for r in csv.DictReader(f, delimiter=";")}


def main():
    comp = carregar_composicao()
    analise = carregar_analise()

    total_pl = sum(float(r["financeiro_brl"]) for r in comp)
    pesos = sorted((float(r["peso_pct"]) for r in comp), reverse=True)

    print("=" * 80)
    print("COMPOSIÇÃO AUVP11 — 19/10/2026 (ponta comprada)")
    print("=" * 80)
    print(f"Papéis na ponta comprada : {len(comp)}")
    print(f"Valor da ponta comprada  : {brl(total_pl)}")
    print("PL de referência do ETF  : R$ 253,4 milhões (etfsbrasil, 16/10)")
    print(f"Top 3 papéis             : {sum(pesos[:3]):.2f}% do PL")
    print(f"Top 10 papéis            : {sum(pesos[:10]):.2f}% do PL")

    grupos = defaultdict(float)
    mapa = {
        "ITUB3": "Itaú (ITUB4+ITUB3+ITSA4)", "ITUB4": "Itaú (ITUB4+ITUB3+ITSA4)",
        "ITSA4": "Itaú (ITUB4+ITUB3+ITSA4)",
        "PETR3": "Petrobras (PETR3+PETR4)", "PETR4": "Petrobras (PETR3+PETR4)",
        "BBDC3": "Bradesco (BBDC3+BBDC4)", "BBDC4": "Bradesco (BBDC3+BBDC4)",
        "SAPR4": "Sanepar (SAPR11+SAPR4)", "SAPR11": "Sanepar (SAPR11+SAPR4)",
        "CYRE3": "Cyrela (CYRE3+CYRE4)", "CYRE4": "Cyrela (CYRE3+CYRE4)",
    }
    for r in comp:
        grupos[mapa.get(r["ticker"], r["empresa"])] += float(r["peso_pct"])
    print("\nMaiores exposições por grupo econômico (% do PL do ETF):")
    for nome, peso in sorted(grupos.items(), key=lambda x: -x[1])[:10]:
        print(f"  {nome:<36} {peso:5.2f}%")

    print("\n" + "=" * 80)
    print("CARTEIRA PROPOSTA — R$ 5.000")
    print("=" * 80)
    print(f"{'Ticker':<7}{'Empresa':<17}{'Setor':<22}{'Alvo':>6}{'Qtd':>4}{'Preço':>8}{'Valor':>9}{'Peso':>7}")
    linhas, custo = [], 0.0
    for t, w in ALVOS:
        a = analise[t]
        q = QUANTIDADES[t]
        valor = q * PRECOS[t]
        custo += valor
        linhas.append({
            "ticker": t, "empresa": a["empresa"], "setor": a["setor"],
            "peso_alvo_pct": round(w * 100, 2), "quantidade": q,
            "preco_ref": f"{PRECOS[t]:.2f}", "preco_teto": f"{PRECOS[t]*1.02:.2f}",
            "valor_brl": f"{valor:.2f}", "peso_real_pct": round(valor / TOTAL * 100, 2),
        })
        print(f"{t:<7}{a['empresa']:<17}{a['setor']:<22}{w*100:>5.0f}%{q:>4}{PRECOS[t]:>8.2f}{valor:>9.2f}{valor/TOTAL*100:>6.1f}%")
    caixa = TOTAL - custo
    print("-" * 80)
    print(f"{'TOTAL EM AÇÕES':<55}{custo:>10.2f}{custo/TOTAL*100:>6.1f}%")
    print(f"{'CAIXA (reserva)':<55}{caixa:>10.2f}{caixa/TOTAL*100:>6.1f}%")
    print(f"{'TOTAL':<55}{TOTAL:>10.2f}{100.0:>6.1f}%")

    # estatísticas ponderadas
    def ponderado(col):
        num = den = 0.0
        for t, _ in ALVOS:
            v = analise[t][col]
            if v not in ("n/d", ""):
                num += float(v) * QUANTIDADES[t] * PRECOS[t]
                den += QUANTIDADES[t] * PRECOS[t]
        return num / den if den else None

    print("\nIndicadores ponderados da carteira (pelos pesos reais):")
    print(f"  P/L médio ponderado  : {ponderado('pl'):.1f}x")
    print(f"  DY médio ponderado   : {ponderado('dy_pct'):.1f}%")
    print(f"  ROE médio ponderado  : {ponderado('roe_pct'):.1f}%")

    # tranches
    print("\nPlano de execução em 3 tranches:")
    totais = [0.0, 0.0, 0.0]
    for i, (titulo, quando) in enumerate([
        ("T1 — agora (21/10)", "antes da eleição"),
        ("T2 — 26/10", "depois do resultado"),
        ("T3 — até 30/11", "com o caixa restante / oportunidade"),
    ]):
        for t, _ in ALVOS:
            totais[i] += TRANCHES[t][i] * PRECOS[t]
        print(f"  {titulo:<22} {brl(totais[i]):>12}  ({totais[i]/TOTAL*100:4.1f}% do total) — {quando}")
    print(f"  Soma das tranches     : {brl(sum(totais))}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(linhas)
    with open(OUT_TRANCHES, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["ticker", "qtd_t1_21-10", "qtd_t2_26-10", "qtd_t3_ate_30-11", "total"])
        for t, _ in ALVOS:
            w.writerow([t, *TRANCHES[t], sum(TRANCHES[t])])
    print(f"\nArquivos gerados:\n  {OUT}\n  {OUT_TRANCHES}")


if __name__ == "__main__":
    main()

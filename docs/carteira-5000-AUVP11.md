# Carteira de R$ 5.000 a partir do AUVP11

**Análise crítica da composição do ETF AUVP11 (base 19/10/2026) e construção de uma carteira enxuta de ações para R$ 5.000.**

> **Data da análise:** 20/10/2026 (preços de referência por volta de 14h30, horário de Brasília)
> **Base de composição:** planilha do fundo fornecida pelo usuário, posição de 19/10/2026 (PL de referência: R$ 253,4 milhões)
> **Fontes:** B3/ETF Brasil, Fundamentus (balanços até 30/06/2026), Yahoo Finance (cotações), InfoMoney, Valor, Estadão, Folha, Exame, Money Times, Seu Dinheiro, BTG Pactual, XP, Genial, Safra, JPMorgan, Citi, TSE e pesquisas eleitorais citadas ao longo do texto.
> **Natureza do material:** estudo educacional. Não é recomendação personalizada de investimento. Rentabilidade passada não garante retorno futuro.

---

## 1. Resumo executivo

O AUVP11 é um ETF de ações brasileiras que replica o índice **IAFD (Teva Ações Fundamentos)**, com filtros quantitativos de qualidade (lucro em 5 anos, ROE > 10%, margem líquida > 8%, dívida líquida/EBITDA < 3, valor de mercado > R$ 3 bi, free float > 15%, liquidez mínima) e exclusão setorial de varejo, proteína animal e transporte aéreo. É um produto coerente e barato (taxa de 0,49% a.a.), mas **não é uma carteira de "melhores empresas" com pesos iguais**: a ponderação é por valor de mercado, e isso produz uma concentração bem maior do que o número de 34 papéis sugere.

Os números da carteira do fundo em 19/10/2026:

| Métrica | Valor |
|---|---|
| Papéis na ponta comprada | 34 |
| **Top 3 papéis** | **45,2% do PL** (ITUB4 15,7% + PETR4 15,7% + PETR3 13,8%) |
| **Top 10 papéis** | **83,3% do PL** |
| Exposição ao grupo Petrobras (PETR3 + PETR4) | 29,4% |
| Exposição ao grupo Itaú (ITUB4 + ITUB3 + ITSA4) | 22,8% |
| Exposição ao grupo Bradesco (BBDC3 + BBDC4) | 8,3% |
| Papéis com peso abaixo de 0,35% | 12 papéis, somando ~2,1% do PL |

Ou seja: **o ETF é, na prática, uma aposta de 45% em três papéis e de 83% em dez**. Para quem tem R$ 5.000, replicar os 34 ativos é impossível (vários pesos virariam R$ 5 a R$ 30 por ação) e, mais importante, **não faria sentido**: a cauda longa não diversifica nada e só adiciona ruído.

Depois de aplicar filtros de qualidade, valuation, liquidez e — principalmente — **diversificação real** (evitando comprar a mesma empresa duas ou três vezes), cheguei a **9 ativos**:

| Ticker | Empresa | Setor | Peso | Valor | Qtd |
|---|---|---|---:|---:|---:|
| ITUB4 | Itaú Unibanco | Bancos | 14,8% | R$ 738,30 | 15 |
| PETR4 | Petrobras (PN) | Petróleo e gás | 11,6% | R$ 578,60 | 10 |
| WEGE3 | WEG | Bens de capital | 9,7% | R$ 483,90 | 10 |
| BBDC4 | Bradesco (PN) | Bancos | 9,6% | R$ 478,40 | 23 |
| ABEV3 | Ambev | Bebidas | 9,8% | R$ 488,94 | 29 |
| SBSP3 | Sabesp | Saneamento | 9,2% | R$ 459,34 | 14 |
| CPFE3 | CPFL Energia | Energia elétrica | 9,1% | R$ 456,57 | 9 |
| PSSA3 | Porto Seguro | Seguros | 8,4% | R$ 420,64 | 8 |
| TOTS3 | TOTVS | Software | 7,6% | R$ 378,54 | 9 |
| **Ações** | | | **89,7%** | **R$ 4.483,23** | |
| **Caixa** | Reserva tática | | **10,3%** | **R$ 516,77** | |
| **Total** | | | **100%** | **R$ 5.000,00** | |

**Indicadores ponderados da carteira (excluindo o caixa):** P/L ~13,4x, ROE ~23,2%, dividend yield trailing ~5,4% (com a Petrobras tendendo a elevar esse número no forward, por conta do payout elevado).

**A tese em uma frase:** manter a espinha dorsal de qualidade do ETF (bancos, Petrobras, WEG, Ambev, utilities e software), cortar a concentração excessiva em Petrobras (de 29% para 12%), eliminar as duplicidades de classes de ação e trocar a cauda longa por nomes líquidos e diversificadores — com **entrada em 3 tranches**, porque o mercado está em máxima histórica a cinco dias do segundo turno.

---

## 2. O que o AUVP11 realmente é (e o que ele não é)

### 2.1 Ficha do produto

| Item | AUVP11 |
|---|---|
| Nome | BTG Pactual Teva AUVP Ações Fundamentos Fundo de Índice |
| Índice | IAFD — Índice Teva Ações Fundamentos |
| Gestor / Administrador | BTG Pactual Asset Management / BTG Pactual DTVM |
| Início | 24-25/06/2025 |
| Taxa de administração | 0,49% a.a. |
| PL | R$ 253,4 milhões (16/10/2026) |
| Cotistas | 27.316 |
| Cotação | R$ 153,15 (20/10, intraday) — 52 semanas: R$ 102,01 a R$ 153,91 |
| Rendimentos | Não distribui; reinveste os dividendos recebidos |
| Retorno | +31,5% em 2026 e +47,1% em 12 meses (até 16/10) |
| Liquidez | volume médio diário na casa de R$ 3 milhões; spread pode ser relevante para ordens grandes |

### 2.2 Como o índice seleciona (e onde ele falha)

O IAFD é transparente e bem-intencionado: exige cinco anos de lucro, ROE acima de 10%, margem líquida acima de 8%, dívida líquida/EBITDA abaixo de 3, valor de mercado acima de R$ 3 bi, free float mínimo de 15% e liquidez mínima. Exclui varejo, proteína animal e aviação. O problema não está nos filtros — está em **o que eles não capturam**:

1. **O filtro é retrospectivo.** "Lucro nos últimos cinco anos" e "ROE > 10%" olham para trás. Uma empresa pode passar no filtro e estar entrando em um ciclo de deterioração (commodities, estatais, empresas alavancadas).
2. **A ponderação é por valor de mercado, não por qualidade.** Quanto maior a empresa, maior o peso — independentemente do preço ou do risco. É por isso que a Petrobras, uma estatal com risco político estrutural, ocupa 29% do fundo.
3. **O número de ativos engana.** São 34 papéis, mas 10 respondem por 83% e 3 por 45%. A cauda longa (Sanepar, Bradsaúde, ABC Brasil, Intelbras, Mahle, Marcopolo, Cury, Direcional, JHSF, EZ TEC...) tem pesos de 0,1% a 0,6% — irrelevantes para o retorno e impossíveis de replicar com R$ 5.000.
4. **Há duplicidades de classe.** O mesmo emissor aparece em ON, PN e unit: Itaú em 3 papéis (22,8%), Petrobras em 2 (29,4%), Bradesco em 2 (8,3%), Sanepar em 2, Cyrela em 2. O fundo "parece" mais diversificado do que é.
5. **O custo existe.** 0,49% a.a. não é caro para um ETF, mas sobre R$ 5.000 são ~R$ 24,50 por ano — valor que você não paga se comprar as ações diretamente em um broker de corretagem zero.

**O que o ETF faz bem:** entrega em uma única cota uma carteira filtrada por fundamentos, com regra pública, sem stock picking discricionário, e com histórico curto mas bom (+47% em 12 meses, acima do Ibovespa). Para quem não quer escolher ações e vai aportar todo mês, é um produto defensável. O ponto aqui é outro: o usuário pediu uma **carteira de R$ 5.000 com ativos realmente bons**, e isso exige ir além do ETF.

### 2.3 O que o relatório do fundo mostra (e o que ele esconde)

A planilha de 19/10/2026 tem uma particularidade: além das posições compradas, ela traz linhas de **"Empréstimo"** e posições **vendidas** nos mesmos tickers, que se anulam par a par (ex.: PETR4 −491.523 e Empréstimo +491.523; WEGE3 −183.074 e +183.074). É o registro contábil do programa de empréstimo de ações (BTC) do fundo — as ações são "entregues" ao tomador e reaparecem como direito a receber. **A exposição econômica do fundo é a ponta comprada**, e é ela que soma ~R$ 249,6 milhões, compatível com o PL de R$ 253,4 milhões. As linhas de "Outros" são despesas, juros sobre capital próprio a receber e provisões, sem efeito sobre a tese. Alguns tickers aparecem zerados ou em pares de +3/−3 que se anulam (EGIE3, CYRE4, ISAE4): estão no universo do índice, mas sem posição econômica na data.

Também chama atenção uma posição de **5.000 cotas do próprio AUVP11 (0,3% do PL)**, com uma linha vendida de mesmo tamanho. É um resíduo operacional (provável artefato de formação de mercado/tesouraria), não uma tese de investimento.

---

## 3. Metodologia da análise crítica

Cada uma das 34 posições foi olhada com cinco perguntas:

1. **Qualidade do negócio:** ROE, margem, geração de caixa, alavancagem, consistência histórica, governança e controle (privado vs. estatal).
2. **Preço:** P/L, P/VP, EV/EBITDA e dividend yield contra a própria história e contra os pares. Empresa boa em preço ruim não entra.
3. **Liquidez:** volume médio diário compatível com uma ordem de R$ 300-800 sem impacto relevante.
4. **Diversificação:** a posição adiciona uma exposição nova ou é a segunda/terceira classe da mesma empresa?
5. **Risco específico:** político, regulatório, câmbio, commodity, ciclo de crédito, execução.

A régua final foi: **9 a 10 ativos, no máximo 25% em um único setor, nenhum ativo acima de 16%, todos com liquidez alta e tese compreensível em uma frase.**

---

## 4. Análise ativo por ativo: as 34 posições do ETF

### 4.1 Os 9 escolhidos

#### ITUB4 — Itaú Unibanco | 14,8% | R$ 738,30 (15 ações)

- **Números:** P/L 11,3x; P/VP 2,54; ROE 22,4%; DY 6,5%; valor de mercado R$ 528 bi; +23,9% em 2026.
- **Por que entra:** é o banco mais rentável e consistente da bolsa brasileira. No 2T26 lucrou R$ 12,4 bi (+7,8% a/a), ROE de 24,3%, carteira de crédito de R$ 1,52 tri (+9,6%) e inadimplência acima de 90 dias estável em 1,9%. É o papel que o mercado compra primeiro quando quer exposição a banco e o último que vende quando quer sair.
- **Preço:** P/VP de 2,54x não é barato, mas é o preço histórico de um banco com ROE de 24%. O papel caiu 4,7% entre 6 e 16/10 e recuperou parte nesta terça-feira (20/10).
- **Insight:** o 3T26 sai em **3-4/11**; o consenso é lucro de ~R$ 12,7 bi e ROE de ~23,8%. Além disso, o Itaú **antecipou o dividendo extraordinário para dezembro/2026** por causa das novas regras de tributação de dividendos — um evento de caixa concreto no fim do ano.
- **Risco:** inadimplência em alta no 3T26 (o mercado já espera resultados mais fracos para os bancos); competição de fintechs; Selic mais alta por mais tempo.

#### PETR4 — Petrobras | 11,6% | R$ 578,60 (10 ações)

- **Números:** P/L 5,6x; EV/EBITDA 3,3x; P/VP 1,55; ROE 27,7%; DY trailing 6,3%; +98,3% em 2026; 52 semanas entre R$ 29,47 e R$ 59,68.
- **Por que entra:** é a ação mais barata da carteira em múltiplos e a principal fonte de dividendos. O 2T26 veio forte (EBITDA de US$ 19 bi, dívida líquida/EBITDA de 1,1x) e o consenso (BTG, Itaú BBA e Safra) projeta dividend yield de ~10% para 2027 com Brent a US$ 70. O BTG tem preço-alvo de R$ 65.
- **O que mudou:** a equipe de Flávio Bolsonaro sinalizou que **Petrobras e Banco do Brasil continuam estatais** — ou seja, o "trade de privatização" não é o cenário-base. O upside de uma vitória do PL vem de risco fiscal menor e juros menores, não de privatização.
- **Insight:** a própria planilha do fundo já carrega **~R$ 314 mil de proventos a receber** da Petrobras (R$ 0,674 por ação), metade dos R$ 1,348/ação aprovados em agosto. Os pagamentos estão previstos para novembro e dezembro. Para quem compra agora, é um dos maiores yields do mercado.
- **Risco:** é o ativo mais sensível à eleição. Uma vitória de Lula pode trazer de volta o risco de interferência em preços/política de dividendos e derrubar o papel 8-15%. Além disso, +98% no ano significa que boa parte do rali já aconteceu, e o petróleo (Brent ~US$ 97 no 2T26) está alto — uma correção do Brent para US$ 70 corta o lucro de forma relevante.

#### WEGE3 — WEG | 9,7% | R$ 483,90 (10 ações)

- **Números:** P/L 32,0x; P/VP 10,6; ROE 33,2%; ROIC 24,3%; DY 4,2%; caixa líquido de R$ 3,7 bi; -1,2% em 2026 e -7,8% em 30 dias.
- **Por que entra:** é a empresa de qualidade mais consistente da bolsa: cresce receita em dólar, tem caixa líquido, margem EBITDA de ~22% e ROIC de 24%. É a única exposição industrial da carteira e um hedge natural contra o risco Brasil (receita externa relevante).
- **Preço:** P/L de 32x ainda é caro em termos absolutos, mas está bem abaixo dos 40-50x que a ação costumava pagar, e o papel está 11% abaixo da máxima de 52 semanas enquanto o Ibovespa está no recorde. É um raro caso de "qualidade em desconto relativo".
- **Insight:** o JPMorgan estima que um **reembolso de tarifas dos EUA** pode gerar ganho extraordinário de R$ 166-234 milhões no 3T26, elevando a margem EBITDA para 23,6-24,2% contra 21,9% de consenso. As tarifas de 37,5% sobre motores atingem só 2-3% da receita, e a produção local/EUA/México mitiga o resto. O BTG tem alvo de R$ 65.
- **Risco:** tarifas americanas, câmbio (real mais forte reduz receita), desaceleração do capex industrial global e o múltiplo ainda alto.

#### BBDC4 — Bradesco | 9,6% | R$ 478,40 (23 ações)

- **Números:** P/L 9,1x; P/VP 1,28; ROE 14,1%; DY 7,6%; +16,4% em 2026.
- **Por que entra:** é o banco grande mais barato da bolsa (P/VP 1,28 contra 2,54 do Itaú) e está em recuperação de rentabilidade. Se o ROE convergir para 17%, o desconto fecha. O DY de 7,6% remunera a espera.
- **Insight:** o **3T26 sai em 22/10 (quinta-feira, após o fechamento)** — é o primeiro catalisador da carteira. O consenso é lucro de ~R$ 7,1 bi (+15% a/a) e ROE de ~15,9%. O aumento de capital de ~R$ 10 bi dilui o ROE temporariamente; o mercado vai olhar principalmente para provisões e inadimplência.
- **Risco:** ROE estruturalmente limitado (o JPMorgan vê teto de 17%), inadimplência de 4,3% na carteira, execução da virada e concorrência.

#### ABEV3 — Ambev | 9,8% | R$ 488,94 (29 ações)

- **Números:** P/L 15,8x; P/VP 2,90; ROE 18,4%; DY 5,2%; caixa líquido de R$ 15,4 bi; +20,2% em 2026; máxima de 52 semanas a R$ 17,04.
- **Por que entra:** é a defensiva clássica da bolsa: demanda estável, caixa líquido, marca forte, payout consistente e receita diversificada na América Latina. Serve para reduzir o beta da carteira em um cenário eleitoral ruim.
- **Insight:** o 3T26 sai no fim de outubro (28-29/10). O consenso é lucro +20% a/a (~R$ 3,9 bi) e EBITDA +3%, com volumes ainda fracos (+0,7%). O papel está no topo da faixa de 52 semanas — há risco de "sell the news" se o volume vier abaixo do esperado. O Safra tem recomendação de venda; Bradesco BBI, XP e Itaú BBA estão mais construtivos.
- **Risco:** volumes fracos, custos de insumos, impostos (cerveja no imposto seletivo) e concorrência.

#### SBSP3 — Sabesp | 9,2% | R$ 459,34 (14 ações)

- **Números:** P/L 14,1x; P/VP 2,51; ROE 17,8%; DY 2,1%; EV/EBITDA 9,7x; dívida líquida/PL 0,76; +21,4% em 2026.
- **Por que entra:** é a maior empresa de saneamento da América Latina, privatizada em 2024, com metas contratuais de universalização até 2029 e um pipeline de capex de R$ 70-100 bi. É crescimento com receita regulada — uma exposição de infraestrutura que o ETF só tem em 4,3%.
- **Insight:** o 2T26 foi fraco (lucro ajustado -41,2% a/a, EBITDA -3,2%) porque a empresa está no pico do ciclo de investimento (R$ 20 bi de capex em 2026, +31,6%). O BTG tem preço-alvo de R$ 31, **abaixo** do preço atual — ou seja, o mercado já pagou parte da tese. É uma posição de longo prazo, não de resultado trimestral.
- **Risco:** execução do capex, revisão tarifária, crise hídrica, custos de construção e o fato de o papel ter subido 19% em um mês.

#### CPFE3 — CPFL Energia | 9,1% | R$ 456,57 (9 ações)

- **Números:** P/L 9,5x; EV/EBITDA 6,1x; ROE 26,4%; DY 7,6%; dívida líquida/PL 1,21; +0,1% em 2026 (bem atrás do Ibovespa).
- **Por que entra:** é a "âncora de renda" da carteira. Energia elétrica privada (controlada pela State Grid), receita previsível, margem alta e um dos maiores dividend yields entre as empresas de qualidade analisadas. A ação ficou parada em 2026 enquanto a bolsa subiu 27% — o que melhora o ponto de entrada.
- **Insight:** com juros futuros caindo em um cenário de vitória do Flávio, as utilities (bond proxies) tendem a se beneficiar duas vezes: pelo dividend yield e pela queda da taxa de desconto. É uma das posições mais assimétricas da carteira.
- **Risco:** alavancagem (dívida líquida de R$ 27,6 bi; dívida líquida/PL de 1,21), hidrologia, revisão tarifária e regulação.

#### PSSA3 — Porto Seguro | 8,4% | R$ 420,64 (8 ações)

- **Números:** P/L 9,0x; P/VP 2,06; ROE 22,8%; DY 5,8%; +11,1% em 2026; 52 semanas entre R$ 45,09 e R$ 55,72.
- **Por que entra:** é uma seguradora diversificada (auto, saúde, residencial, vida e banco) com ROE de 22,8% e P/L de 9x — uma combinação rara de qualidade e preço. Tem diversificado a receita para saúde, auto e serviços financeiros (Porto Bank), reduzindo a dependência do seguro de automóvel.
- **Insight:** é a posição com menor beta eleitoral entre os financeiros: o negócio é de prêmios e sinistralidade, não de crédito ou de juros. Em um cenário de estresse, tende a sofrer menos que os bancos.
- **Risco:** sinistralidade, concorrência em auto, regulação de saúde e o fato de o setor de seguros estar cada vez mais competitivo.

#### TOTS3 — TOTVS | 7,6% | R$ 378,54 (9 ações)

- **Números:** P/L 16,6x; P/VP 4,33; ROE 26,1%; DY 1,7%; EV/EBITDA 9,3x; -1,9% em 2026.
- **Por que entra:** é a maior empresa de software da América Latina, com **92,8% da receita recorrente**, ARR de R$ 7,74 bi (+14%) e 30 trimestres consecutivos de crescimento de dois dígitos na receita recorrente. O P/L de 16,6x é o mais baixo em anos para uma empresa que costumava negociar a 25-35x.
- **Insight:** a XP elevou o alvo para R$ 47 (potencial de ~12%) e vê reprecificação com a monetização de IA — os "habilitadores de IA" já respondem por um terço da receita recorrente incremental. O 3T26 sai em 4/11.
- **Risco:** desaceleração do crescimento, integração de aquisições (Linx, RD Station), concorrência e o múltiplo ainda exigente para um crescimento de 13-15%.

### 4.2 Os 25 deixados de fora (e o motivo)

| Grupo | Ativos | Motivo |
|---|---|---|
| **Duplicidade de classe** (6) | ITUB3, ITSA4, PETR3, BBDC3, SAPR4, CYRE4 | É a mesma empresa. Comprar duas classes não diversifica; só aumenta custo e complica o rebalanceamento. ITSA4 é uma ótima alternativa para quem quer mais DY (7,3%) e desconto de holding, mas substituiria o ITUB4, não se somaria a ele. |
| **Cauda longa / liquidez** (13) | SAPR11, CYRE3, CMIN3, CURY3, DIRR3, JHSF3, EZTC3, POMO4, LEVE3, ABCB4, INTB3, SAUD3, AUVP11 | Pesos de 0,1% a 0,6% no ETF; com R$ 5.000, virariam R$ 5 a R$ 30 por ativo. Não movem o retorno, têm liquidez limitada e, no caso de construtoras e commodities, adicionam beta a juros/China sem prêmio proporcional. AUVP11 é posição residual do próprio fundo. |
| **Boas empresas, mas caras ou redundantes** (6) | B3SA3, BPAC11, BBSE3, RDOR3, CMIG4, TIMS3 | B3 (P/L 21x, +70% no ano) e BTG (P/VP 3,8, +51%) são negócios excelentes, mas o preço já embutiu a recuperação. BBSE3 tem DY de 11,3%, porém crescimento baixo e dependência do BB/agro. RDOR3 tem P/L 20x e R$ 51 bi de dívida bruta. CMIG4 é barata (P/L 7,2, DY 8,8%), mas é estatal mineira, com risco político e passivos judiciais. TIMS3 tem múltiplos distorcidos por evento societário e está na mínima de 52 semanas. |

**Sobre a TIM:** os dados de P/L e receita TTM no Fundamentus estão claramente distorcidos (P/L de 3.269x e receita trimestral maior que a anual), o que indica evento societário ou erro de consolidação. Sem entender o evento, não entra — e a ação está 33% abaixo da máxima de 52 semanas, o que sugere que o mercado sabe de algo que os números não mostram.

---

## 5. A carteira de R$ 5.000

### 5.1 Composição final

| Ticker | Empresa | Setor | Sensibilidade à eleição | Peso | Qtd | Preço ref. | Valor |
|---|---|---|---|---:|---:|---:|---:|
| ITUB4 | Itaú | Bancos | Alta | 14,8% | 15 | R$ 49,22 | R$ 738,30 |
| PETR4 | Petrobras | Petróleo e gás | Alta | 11,6% | 10 | R$ 57,86 | R$ 578,60 |
| WEGE3 | WEG | Bens de capital | Baixa/Média | 9,7% | 10 | R$ 48,39 | R$ 483,90 |
| BBDC4 | Bradesco | Bancos | Alta | 9,6% | 23 | R$ 20,80 | R$ 478,40 |
| ABEV3 | Ambev | Bebidas | Baixa/Média | 9,8% | 29 | R$ 16,86 | R$ 488,94 |
| SBSP3 | Sabesp | Saneamento | Média | 9,2% | 14 | R$ 32,81 | R$ 459,34 |
| CPFE3 | CPFL | Energia elétrica | Média | 9,1% | 9 | R$ 50,73 | R$ 456,57 |
| PSSA3 | Porto Seguro | Seguros | Média | 8,4% | 8 | R$ 52,58 | R$ 420,64 |
| TOTS3 | TOTVS | Software | Média/Alta | 7,6% | 9 | R$ 42,06 | R$ 378,54 |
| — | **Caixa / reserva** | — | — | 10,3% | — | — | R$ 516,77 |
| | **Total** | | | **100%** | | | **R$ 5.000,00** |

**Distribuição setorial:** bancos 24,3% · petróleo 11,6% · bebidas 9,8% · bens de capital 9,7% · saneamento 9,2% · energia elétrica 9,1% · seguros 8,4% · software 7,6% · caixa 10,3%. Nenhum setor acima de 25%, nenhum ativo acima de 15%.

### 5.2 Por que 9 ativos e não 34

- **Concentração que funciona:** 9 posições de R$ 380-740 são grandes o suficiente para importar e pequenas o suficiente para não quebrar a carteira se uma delas cair 30%.
- **Diversificação real, não cosmética:** cada ativo traz um driver diferente (crédito, petróleo, indústria/exportação, consumo defensivo, saneamento, energia, seguros, software). No ETF, 29% é Petrobras e 23% é Itaú — dois drivers.
- **Custo e simplicidade:** 9 ordens em vez de 34; rebalanceamento factível; acompanhamento trimestral possível.
- **Liquidez:** todos os 9 têm volume médio diário acima de R$ 90 milhões (a maioria acima de R$ 200 milhões), então uma ordem de R$ 500 não move o preço.

### 5.3 Por que 10% em caixa

Não é "medo": é **gestão de timing em uma semana binária**. O Ibovespa está em máxima histórica (208.748 pontos em 20/10, recorde de 209.714), o mercado já precifica vitória de Flávio Bolsonaro (pesquisas de 19-20/10 dão 51-53% a 47-49%, e os mercados de previsão davam 85-88% de chance ao PL), e o segundo turno é em **25/10**. Comprar 100% antes do resultado é aceitar uma assimetria ruim: se Flávio ganhar, o upside adicional é limitado (já está no preço); se Lula virar, a queda pode ser de 8-15% em poucos dias.

Os R$ 516,77 são a munição para (a) completar a terceira tranche a preços melhores ou (b) comprar mais dos mesmos ativos em um eventual "Lula panic". Se até 30/11 não houver oportunidade, o caixa pode ser investido nos ativos que estiverem mais baratos ou mantido como reserva de liquidez.

---

## 6. O cenário atual e as eleições: o que realmente importa para os próximos dias

**Resposta curta: sim, a eleição pode mexer com o preço das ações nos próximos dias — mas muito mais pelo humor do mercado do que pelo valor intrínseco das empresas.** E há um detalhe que muda tudo: o mercado já precificou a vitória de Flávio Bolsonaro. Isso significa que o risco é assimétrico para quem compra agora: uma vitória do PL tende a confirmar o preço (com pouco upside adicional), enquanto uma vitória de Lula tende a provocar uma correção relevante. É por isso que a entrada é feita em três tranches.

### 6.1 O quadro eleitoral

- **Primeiro turno (4/10):** Flávio Bolsonaro (PL) 47,03% x Lula (PT) 45,16% dos votos válidos — uma diferença de ~2,2 milhões de votos.
- **Segundo turno:** 25/10/2026.
- **Pesquisas de 19-20/10:**
  - Real Time Big Data (20/10): Flávio 52% x Lula 48% (votos válidos; empate técnico no limite da margem de 2 p.p.).
  - AtlasIntel/Bloomberg (19/10): 51,1% x 48,9%.
  - PoderData (19/10): 52% x 48%.
  - Datafolha (15/10): 51% x 49%.
  - Alfa (20/10): 51,5% x 48,5%.
  - Gerp (20/10): 53% x 47%.
- **Datafolha final:** divulgação em 22/10 (campo de 20 a 22/10) — é o último grande evento antes da votação.
- **Base histórica:** desde 1989, **nenhum candidato que ficou em segundo lugar no primeiro turno virou no segundo**.
- **Cuidado com as pesquisas:** no primeiro turno, a maioria das pesquisas apontava pequena vantagem de Lula e o resultado deu Flávio à frente. As pesquisas deste segundo turno estão dentro da margem de erro, e um erro de 2-3 p.p. é suficiente para mudar o vencedor.
- **Mercado:** a Eurasia Group elevou a probabilidade de vitória de Flávio para 80%; os mercados de previsão chegaram a ~88%.

### 6.2 O que o mercado já precificou

O Ibovespa saiu de ~192 mil pontos antes do primeiro turno para **206.911 no dia seguinte (+7,7%)** e renovou recordes sucessivos, chegando a **209.714 pontos** em 9/10. O dólar caiu para ~R$ 4,98 e os juros futuros recuaram. No mês, Itaú subiu 13,2%, Bradesco 14,7%, B3 25,7% e Petrobras 18,1%.

**Isso é a informação mais importante deste relatório:** o mercado não está "esperando" a eleição — ele já comprou o resultado. O BTG estima que uma vitória de Flávio pode levar a bolsa a 11-45% de alta adicional, mas parte desse potencial já foi realizada. A assimetria, hoje, é **desfavorável para quem compra tudo antes do dia 25**.

### 6.3 Cenários para os próximos dias (estimativas qualitativas, não previsões)

| Cenário | Prob. implícita | Ibovespa | Dólar | Juros futuros | Bancos (ITUB4/BBDC4) | PETR4 | Utilities (SBSP3/CPFE3) | WEGE3/ABEV3 |
|---|---|---|---:|---|---|---|---|---|
| **Flávio vence com folga (>5 p.p.)** | ~35% | +3% a +8% | R$ 4,80-4,95 | queda | +5% a +10% | +3% a +6% | +3% a +6% | +1% a +3% |
| **Flávio vence apertado (<3 p.p.)** | ~40% | -2% a +2% (sell the news) | R$ 5,00-5,10 | estável | -3% a +2% | -2% a +2% | 0% a +3% | 0% a +2% |
| **Lula vira** | ~20-25% | -8% a -15% | R$ 5,30-5,50 | alta | -10% a -15% | -8% a -15% | -5% a -10% | -2% a -6% |

As probabilidades são uma leitura das pesquisas e dos mercados de previsão, não um modelo. Os intervalos de preço são ordens de grandeza históricas para choques eleitorais, não projeções.

**Leitura por ativo:**

- **ITUB4 e BBDC4** são o coração do "trade Flávio": bancos domésticos, sensíveis a juros e a risco fiscal. Em uma vitória do PL, são os primeiros a subir; em uma vitória de Lula, os primeiros a cair. O Itaú é a versão "qualidade" (menos beta), o Bradesco a versão "desconto" (mais beta).
- **PETR4** é o ativo mais binário. A boa notícia é que o dividend yield alto e o P/L de 5,6x criam um piso relativo; a má é que uma mudança de governo pode reabrir o risco de interferência em preços e na política de dividendos. O mercado já sabe disso — o papel subiu 98% no ano.
- **SBSP3 e CPFE3** são "bond proxies": sofrem com juros altos e se beneficiam de queda de juros. Não são o centro do trade eleitoral, mas sentem o efeito pela taxa de desconto.
- **WEGE3 e ABEV3** têm menor sensibilidade ao risco Brasil: a WEG é exportadora e o risco dela é tarifa americana/câmbio; a Ambev é defensiva e doméstica, mas de demanda estável. São o "amortecedor" da carteira.
- **TOTS3 e PSSA3** são domésticas e de qualidade, com beta médio. A TOTVS sofre mais com juros altos (growth), a Porto menos (seguros).

### 6.4 O que fazer, na prática

1. **Não compre tudo agora.** Execute a **T1 (31% do total)** em 21/10, com ordens limitadas.
2. **Espere o resultado.** A **T2 (31%)** entra em 26/10, o primeiro pregão após a apuração, **independentemente do resultado** — se Flávio ganhar e o mercado subir, você paga mais caro, mas mantém o plano; se Lula ganhar e o mercado cair, você compra mais barato, que é exatamente o que quer.
3. **Guarde a T3 (27%) + o caixa.** Execute até 30/11, ou antes se houver uma queda de 8-10% no Ibovespa.
4. **Não venda no pânico.** Se Lula ganhar e a carteira cair 10-15%, a tese das 9 empresas não muda em uma semana. O pior erro seria vender no fundo e perder a recuperação.
5. **Não persiga o rali.** Se Flávio ganhar e o Ibovespa abrir +5%, não aumente a mão: o risco/retorno de comprar no auge de um rali eleitoral é ruim.

### 6.5 O que o resultado NÃO muda

O resultado da eleição muda o **preço de entrada** e a **taxa de desconto**, não o fluxo de caixa de longo prazo da Ambev, da WEG, da Sabesp, da CPFL, da TOTVS ou da Porto. Para a Petrobras e os bancos, há efeitos reais (política de preços, crédito, juros), mas eles são de segunda ordem no horizonte de 3-5 anos. **A eleição é um evento de timing, não de tese.**

---

## 7. Plano de execução

### 7.1 As três tranches

| Tranche | Data | Valor | % do total | O que comprar |
|---|---|---:|---:|---|
| **T1** | 21/10 (antes da eleição) | R$ 1.557,87 | 31,2% | 5 ITUB4, 4 PETR4, 3 WEGE3, 8 BBDC4, 10 ABEV3, 5 SBSP3, 3 CPFE3, 3 PSSA3, 3 TOTS3 |
| **T2** | 26/10 (depois do resultado) | R$ 1.548,40 | 31,0% | 5 ITUB4, 3 PETR4, 4 WEGE3, 8 BBDC4, 10 ABEV3, 5 SBSP3, 3 CPFE3, 3 PSSA3, 3 TOTS3 |
| **T3** | até 30/11 | R$ 1.376,96 | 27,5% | 5 ITUB4, 3 PETR4, 3 WEGE3, 7 BBDC4, 9 ABEV3, 4 SBSP3, 3 CPFE3, 2 PSSA3, 3 TOTS3 |
| **Caixa** | — | R$ 516,77 | 10,3% | Reserva para oportunidade/liquidez |

### 7.2 Regras de ordem

- **Use ordens limitadas**, com preço-teto de +2% sobre a referência (coluna `preco_teto` no CSV): ITUB4 R$ 50,20; PETR4 R$ 59,02; WEGE3 R$ 49,36; BBDC4 R$ 21,22; ABEV3 R$ 17,20; SBSP3 R$ 33,47; CPFE3 R$ 51,74; PSSA3 R$ 53,63; TOTS3 R$ 42,90.
- **Evite os primeiros 15 minutos e os últimos 5 minutos** do pregão: o spread é maior e o preço é mais volátil.
- **Corretagem:** se o seu broker cobra R$ 10 por ordem, 9 ordens custam R$ 90 (1,8% da carteira) — nesse caso, vale mais a pena concentrar em 4-5 ativos ou usar o próprio ETF no primeiro ano. Com corretagem zero, a carteira direta é mais barata que os 0,49% a.a. do ETF já no primeiro ano.
- **Emolumentos B3:** ~0,03% por lado, irrelevantes para R$ 5.000.

### 7.3 Rebalanceamento e monitoramento

- **Rebalanceamento:** anual, ou quando um ativo se afastar mais de 5 p.p. do peso-alvo. Não rebalanceie a cada mês — o custo não compensa.
- **Revisão trimestral da tese:** resultados, guidance, mudanças de controle/regulação, alavancagem.
- **Gatilhos de saída (quebra de tese, não de preço):**
  - **PETR4:** mudança na política de preços ou interferência política na diretoria; Brent abaixo de US$ 60 por dois trimestres.
  - **BBDC4:** ROE abaixo de 13% por dois trimestres ou inadimplência acima de 5%.
  - **ITUB4:** ROE abaixo de 18% ou deterioração relevante da carteira de crédito.
  - **WEGE3:** margem EBITDA abaixo de 18% ou perda de participação nos EUA.
  - **SBSP3:** atraso relevante nas metas de universalização ou revisão tarifária adversa.
  - **CPFE3:** alavancagem acima de 3,5x EBITDA ou revisão tarifária negativa.
  - **ABEV3:** perda estrutural de volume/share no Brasil.
  - **TOTS3:** crescimento de receita recorrente abaixo de 10% por dois trimestres.
  - **PSSA3:** sinistralidade muito acima do histórico.

---

## 8. Calendário dos próximos 40 dias

| Data | Evento | Ativo | Por que importa |
|---|---|---|---|
| 22/10 | Resultado do 3T26 do Bradesco | BBDC4 | Primeiro catalisador; provisões e ROE |
| 22/10 | Datafolha final | Carteira | Última pesquisa antes do voto |
| **25/10** | **2º turno** | Carteira | Evento binário; define o timing das tranches 2 e 3 |
| 28-29/10 | Resultado do 3T26 da Ambev | ABEV3 | Volumes e margem |
| 03-04/11 | Resultado do 3T26 do Itaú | ITUB4 | Qualidade de crédito e ROE |
| 04/11 | Resultado do 3T26 da TOTVS | TOTS3 | ARR, margem e IA |
| 10/11 | Resultado do 3T26 da Petrobras | PETR4 | Produção, Brent, dividendos |
| Nov-Dez | Pagamento de dividendos da Petrobras | PETR4 | R$ 1,348/ação em duas parcelas |
| Dez/2026 | Dividendo extraordinário do Itaú | ITUB4 | Antecipado por causa da nova tributação |

---

## 9. Riscos e limitações

**Riscos da carteira:**

1. **Risco eleitoral (curto prazo):** uma vitória de Lula pode derrubar a carteira 10-15% em poucos dias, com bancos e Petrobras liderando a queda.
2. **Risco de crédito (3T26):** a inadimplência está em alta e os bancos devem reportar resultados mais fracos no 3º trimestre. Itaú e Bradesco são 24% da carteira.
3. **Risco de commodity:** a Petrobras é 11,6% da carteira e depende do Brent (~US$ 97 no 2T26). Uma queda para US$ 70 reduz lucro e dividendos.
4. **Risco de juros:** utilities (18,3% da carteira) e growth (TOTVS, 7,6%) são sensíveis à curva de juros.
5. **Risco de concentração:** 9 ativos é uma carteira concentrada por definição. Se um deles quebrar a tese, o impacto é de 8-15%.
6. **Risco regulatório:** Sabesp (tarifas), CPFL (tarifas), bancos (regulação), Petrobras (política de preços).
7. **Risco de execução:** o preço de 20/10 é intradiário e pode mudar; as quantidades foram calculadas com esses preços.

**Limitações dos dados:**

- Os fundamentos (P/L, P/VP, DY, ROE) são do Fundamentus com base nos balanços até 30/06/2026 e preços de 19/10/2026.
- Os preços de referência são de 20/10/2026, por volta de 14h30 — podem ter mudado até o fechamento.
- As notícias e projeções de casas (BTG, XP, JPMorgan, Citi, Safra) são opiniões de terceiros, não minhas.
- As probabilidades eleitorais são uma leitura das pesquisas e dos mercados de previsão; não são garantia de resultado.
- **Este material não é recomendação personalizada.** Antes de investir, considere seu perfil de risco, horizonte, necessidade de liquidez e situação tributária. Para valores acima de R$ 50 mil por mês em dividendos de uma mesma empresa, há retenção de 10% de IRRF desde 2026 (Lei 15.270/2025) — para R$ 5.000, essa regra não se aplica.

---

## 10. Conclusão

O AUVP11 é um bom produto, mas **não é uma carteira de "melhores empresas"**: é uma carteira de 34 papéis ponderada por tamanho, com 45% em três nomes e 83% em dez. Para R$ 5.000, replicá-lo seria caro, complicado e ilusório.

A carteira proposta mantém o que há de melhor no ETF — Itaú, Petrobras, WEG, Ambev, Sabesp, CPFL, Porto e TOTVS, além do Bradesco —, corta a concentração em Petrobras de 29% para 12%, elimina as duplicidades de classes e troca a cauda longa por diversificação real. O resultado é uma carteira de 9 ativos, P/L ~13x, ROE ~23%, DY ~5,4%, com 10% em caixa para atravessar a semana eleitoral.

**A decisão mais importante não é qual ação comprar, e sim como comprar:** em três tranches, com ordens limitadas, sem pressa e sem pânico. O mercado está em máxima histórica e já precifica a vitória de Flávio; a assimetria de comprar tudo antes do dia 25 é ruim. Quem compra bem não é quem acerta a eleição — é quem não precisa acertar.

---

### Arquivos deste projeto

- `data/auvp11_composicao_2026-10-19.csv` — composição do ETF (ponta comprada, 34 papéis)
- `data/analise_ativos_2026-10-20.csv` — screening com fundamentos, decisão e motivo
- `scripts/montar_carteira.py` — script que reproduz a carteira e as tranches
- `output/carteira_5000.csv` — carteira final com preços, quantidades e pesos
- `output/tranches.csv` — plano de execução em 3 tranches

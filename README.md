# BaseBot — rotina visual no emulador Windows

Automação pessoal por **capturas de tela, OCR e mouse/teclado**. Não lê memória, não usa ADB, não modifica o app e não faz login. Use apenas onde você tem autorização e respeite as regras do aplicativo.

## Comece em 3 passos

1. **Prepare a pasta e o computador.** Extraia o ZIP inteiro para uma pasta sua, por exemplo `Documentos\BaseBot` — não execute dentro do ZIP. O pacote compilado deve conter `BaseBot.exe`, `INICIAR.bat`, `CALIBRAR.bat` e os dois arquivos `.ini`. Instale o **Tesseract para Windows** seguindo a seção abaixo. Deixe o emulador no monitor principal, inteiramente visível, com o app aberto na sua conta, personagem pronto, joystick e coordenadas na tela. Desative suspensão/bloqueio automático durante a rotina. Não minimize, redimensione nem altere o zoom do emulador.
2. **Configure e calibre uma vez.** Abra `config.ini` no Bloco de Notas: ajuste `alvo_x`, `alvo_y`, `hora_inicio`, `minutos_permanencia`, `tolerancia` e o **título exato da janela**. Salve sem mudar a extensão `.ini`. Dê duplo clique em **CALIBRAR.bat**. Com a janela do emulador em foco, apenas posicione o mouse: **F1** no canto superior esquerdo de toda a leitura X/Y; **F2** no canto inferior direito; **F3** no centro do joystick; **F4** na borda útil do joystick. Não clique. Uma tela exibe a leitura viva e o recorte por aproximadamente **10 segundos**. Compare com o app e confirme **Sim somente se os números estiverem corretos**. O assistente salva `calibracao.ini`. Recalibre se mudar máquina, resolução, DPI, zoom ou layout do app.
3. **Inicie a rotina com dois cliques.** Faça primeiro o teste curto do [checklist](CHECKLIST_TESTES.md). Depois, dê duplo clique em **INICIAR.bat** e deixe o console aberto. Ele conta até o horário, navega até o alvo, mantém a posição pelo tempo escolhido, avisa e encerra. **Não interaja com mouse/teclado durante a execução. F12 ou mover o mouse para (0,0), o canto superior esquerdo do monitor principal, interrompe a automação.**

**Se der erro, envie o arquivo de log** mais recente da pasta `logs` para quem presta suporte. Não envie o webhook do Discord nem o `config.ini` contendo esse segredo. Em caso de erro, a janela fica aberta para você ler a mensagem; a conclusão normal fecha o processo. O programa não fecha o emulador nem desliga o computador.

> **Se o ZIP não contém `BaseBot.exe`, você recebeu os fontes, não o pacote executável.** Peça a quem forneceu para compilá-lo seguindo [EMPACOTAMENTO.md](EMPACOTAMENTO.md), ou use Python conforme abaixo. Não há binário Windows validado incluído neste repositório.

## Instalar o Tesseract (uma vez)

- Consulte a documentação oficial: <https://github.com/tesseract-ocr/tesseract#installing-tesseract>.
- A documentação aponta para builds de Windows, como o projeto UB Mannheim: <https://github.com/UB-Mannheim/tesseract/wiki>. Obtenha o instalador pela origem indicada, não de sites aleatórios.
- Na instalação, mantenha os dados do idioma **English / eng**. O OCR usa `eng`, mesmo que o app esteja em português, porque lê números e os rótulos X/Y.
- O local habitual é `C:\Program Files\Tesseract-OCR\tesseract.exe`. O BaseBot tenta encontrar nesse local, no `PATH` e em `%LOCALAPPDATA%\Tesseract-OCR`. Se não encontrar, preencha `caminho_tesseract` no `config.ini`, **sem aspas**.
- Diagnóstico opcional no Prompt de Comando: `"C:\Program Files\Tesseract-OCR\tesseract.exe" --version`.

**O executável único inclui Python e as bibliotecas Python, mas não o Tesseract nem o emulador.** O executável e os INIs precisam permanecer juntos em uma pasta gravável. Não é necessário executar como administrador; prefira bot e emulador ambos sem elevação.

## O que configurar

Todos os parâmetros estão comentados no próprio `config.ini`. Valores decimais usam **ponto**, nunca vírgula decimal. Uma faixa de segundos é `minimo,maximo`, por exemplo `0.5,0.9`. Não coloque comentários no fim das linhas dos valores.

| Parâmetro | Significado |
|---|---|
| `alvo_x`, `alvo_y` | Coordenadas do readout, não pixels da tela. |
| `hora_inicio` | `HH:MM` no relógio local do Windows. Se passou, agenda amanhã; se está no mesmo minuto, começa agora. |
| `minutos_permanencia` | Conta a partir da primeira chegada. Inclui tempo de correção e reconexão; não promete N minutos ininterruptos dentro da tolerância. |
| `tolerancia` | Cada eixo deve satisfazer `abs(erro) <= tolerancia`. Comece com `5`. |
| `inverter_y` | `sim` se o Y do app cresce para cima; `nao` se cresce para baixo. X é assumido crescente para a direita. |
| `titulo` | Título exato da janela. Se houver duas iguais, o bot não escolhe às cegas. |
| `caminho_emulador` | Opcional, EXE sem argumentos. Abre no horário se a janela não existir; **não abre o app, não desbloqueia e não autentica sua conta**. |
| `webhook_discord` | Opcional, URL do webhook do seu canal. Sem isso, há mensagem no console, log e sinal sonoro do terminal. |
| `pulso`, `pulso_perto` | Longe do alvo: 0,5–0,9 s; perto: 0,08–0,18 s no exemplo. Reduza perto se oscilar. |
| `jitter_angular_graus` | Desvio aleatório máximo na direção. Padrão zero; jitter excessivo piora a precisão. A duração já varia pela faixa. |
| `verificacao_posicao` | Relê/corrige a cada 20–45 s **após a última verificação/correção**. |
| `keep_alive.habilitado` | Desligado por segurança. Ligue só depois de testar uma tecla inofensiva ao app. Não garante evitar desconexão. |

As faixas controlam todas as esperas operacionais. Limites de navegação, validação, reconexão e permanência são **prazos/durações**, não intervalos fixos. O limite curto de encerramento do logger é uma proteção de segurança, não uma pausa operacional.

## Como a segurança funciona

- F12 é observado por um listener global; outra thread verifica o canto `(0,0)` e o foco. O watchdog usa 20–50 ms por padrão, no máximo configurável 100 ms.
- Em emergência, solta o botão esquerdo/tecla via API nativa do Windows e encerra o processo com código `130`, **sem esperar o OCR ou o webhook**. O PyAutoGUI FAILSAFE também fica habilitado. A confirmação de encerramento no BAT pode exigir uma tecla, mas nenhum input continua sendo enviado.
- **Alvo de resposta: menos de 1 segundo. Não é garantia de tempo real do Windows.** Precisa ser medido no PC real, incluindo sob carga, durante arraste, OCR, espera e rede. Computador travado, hooks bloqueados, sessão bloqueada/UAC e diferenças de privilégio podem impedir automação/atalhos. Não aprove o teste noturno se qualquer parada falhar.
- Perda de foco, minimização, fechamento ou movimento da janela durante input solta o mouse e suspende novos inputs. O programa tenta restaurar/ativar a janela aproximadamente a cada 30 s por até 10 min. O Windows pode negar a ativação; nesse caso ele espera, não clica em outra janela.
- A calibração é relativa à área cliente: mover a janela é recuperável; **mudar seu tamanho requer recalibrar**. Mantenha tudo no monitor principal.
- Não cubra o readout com menus, tooltips, notificações ou overlays (especialmente janelas “sempre no topo”). Screenshots veem o que está realmente na tela; o programa não detecta toda possível sobreposição interna/externa.
- Três falhas de OCR consecutivas, coordenadas ambíguas, timeout ou falta de progresso encerram a rotina sem inputs às cegas. Não há desvio de obstáculos nem planejamento de caminho.
- Uma trava por sessão do Windows impede duas instâncias do bot/calibração ao mesmo tempo. Ela é liberada automaticamente quando o processo termina.

## Se o OCR não ler direito

Marque **somente a linha X/Y**, incluindo seus dois valores por completo e espaço para dígitos maiores/negativos. A pipeline é: cinza → inversão opcional → threshold → ampliação 2× → Tesseract `--psm 7`. Ajuste `threshold` e `inverter_imagem` e refaça a validação.

A whitelist padrão inclui dígitos e **`XYxy:-`** para preservar os dois campos. É possível usar somente `0123456789`, mas alguns readouts ficam concatenados: `510732`. Isso é rejeitado propositalmente; o programa não tenta inferir onde separar X de Y. Também rejeita campos trocados, lixo adicional e valores fora dos limites configurados. OCR pode produzir um número errado porém plausível: calibração visual, limites de coordenadas e testes de direção continuam indispensáveis.

Se o personagem anda na direção errada, interrompa, ajuste `inverter_y` e confirme o centro/raio. Se oscila, reduza `pulso_perto` e mantenha jitter angular zero. Jitter sozinho não elimina overshoot. Apps com câmera rotativa, eixos não alinhados, aceleração forte ou mapas com obstáculos podem exigir um controlador diferente.

## Logs e conclusão

`logs/exec_AAAA-MM-DD_HH-MM.log` contém modo, leitura bruta do OCR, coordenadas, deltas, direção/duração dos pulsos, correções, perda/recuperação de janela e erros. Execuções iniciadas no mesmo minuto acrescentam ao mesmo arquivo, com cabeçalhos separados. Não salva screenshots por padrão.

O aviso `concluído às HH:MM` é emitido somente ao terminar a rotina normalmente. Erros/paradas não enviam esse aviso. O webhook é uma tentativa com timeout, sem redirecionamentos nem envio automático repetido. Falhas são registradas sem expor a URL; `falha_fatal = sim` faz a falha do aviso retornar código de erro mesmo após a rotina física ter terminado. O som do terminal depende das configurações do Windows.

A emergência prioriza soltar o mouse e encerrar; a última linha do log pode faltar se o disco/logger estiver bloqueado. Guarde os logs de testes, revise dados pessoais antes de compartilhar e exclua logs antigos manualmente.

## Executar a partir dos fontes (opcional, para quem tem Python)

No Windows, instale Python **3.10+**, com Tcl/Tk e o launcher `py`. Abra um terminal na pasta e execute:

```bat
py -3 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python basebot.py --validar-config
.venv\Scripts\python basebot.py --dry-run
```

Depois use os dois BATs: eles preferem `BaseBot.exe`; se não existir, usam o Python de `.venv`, ou o launcher `py`. Não instalam dependências automaticamente.

`--dry-run` roda também em Linux/macOS com Python, sem instalar dependências. Ignora horário e calibração, usa relógio virtual e simula chegada/deriva/correção. Não acessa mouse, Tesseract ou rede; **não testa F12 real nem a precisão do app**. Para coordenadas/extremos não usuais ou tolerância muito estreita, os parâmetros podem precisar de ajuste mesmo na simulação.

Validação completa: [CHECKLIST_TESTES.md](CHECKLIST_TESTES.md). Compilação e ZIP para distribuir: [EMPACOTAMENTO.md](EMPACOTAMENTO.md).

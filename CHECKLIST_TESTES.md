# Checklist de aceite — BaseBot

Marque somente o que foi executado. **A simulação não substitui testes Windows/emulador.** Faça os testes curtos acompanhado, em local sem risco de perda de itens/progresso. Para cada teste guarde o log, resultado, versão do Windows/emulador, tamanho da janela e escala DPI. Não inclua senhas/webhooks no relatório.

## A — Dry-run sem app (primeiro)

- [ ] Em Python 3.10+: `python -m unittest discover -s tests -v` passa sem dependências gráficas.
- [ ] `python basebot.py --validar-config` retorna zero com o exemplo.
- [ ] `python basebot.py --dry-run` retorna zero: aparecem chegada, `deriva aplicada`, novos pulsos/correção e conclusão. Não há movimento do mouse, acesso à rede, abertura de app nem espera de 30 minutos reais.
- [ ] O log informa explicitamente `SIMULAÇÃO`; não confundir com uma rotina real concluída.
- [ ] Em cópia do INI, horário `25:00`, faixa invertida `0.9,0.5` e watchdog acima de `0.1` geram erro claro. Não altere o arquivo de produção para testar.
- [ ] `calibracao.ini` de exemplo (`calibrado = nao`) impede inputs reais.
- [ ] Executar de outra pasta usando caminho absoluto continua encontrando os arquivos ao lado do script/EXE.
- [ ] No Windows, compilar com `empacotar.ps1`; smoke tests do EXE e ZIP terminam sem erro.
- [ ] Extrair o ZIP executável em PC Windows sem Python: `BaseBot.exe --dry-run` funciona. Verificar que o pacote não contém webhook, logs ou calibração ativa.

**Cobertura automatizada incluída:** parsing estrito X/Y; rejeição de leitura incompleta/concatenada; limites; faixas e config; geometria/calibração atômica; hoje/amanhã/mesmo minuto; inversão de Y; tolerância por eixo; pulsos próximos; chegada/deriva/keep-alive simulados; retry/falha OCR; estagnação; timeout inclusive após OCR lento; reconexão e falha; cancelamento de espera; liberação de mouse/tecla em exceção; proteção de foco; ausência de rede em dry-run. Não mede latência física de hooks/mouse.

## B — Teste curto acompanhado (Windows + app real)

### Preparação e calibração

- [ ] Tesseract responde `--version`; idioma `eng` instalado. Bot/emulador com o mesmo nível de privilégio (preferencialmente sem administrador).
- [ ] Configurar alvo próximo, caminho livre, tolerância inicial 5, permanência de **2 minutos** e início no minuto atual. Desativar keep-alive inicialmente.
- [ ] F1/F2 enquadram os dois campos, com folga para todos os dígitos. F3/F4 enquadram centro/raio real do joystick. Confirmar que a área é relativa à janela, não à tela inteira.
- [ ] Durante os 10 s de validação, todos os valores X/Y exibidos coincidem com o app. Testar fonte clara/escura, limites de tamanho dos números e valores negativos, se aplicáveis. Não confirmar leitura errada plausível.
- [ ] O painel de validação não cobre a região OCR. Fechar/cancelar o painel não salva nova calibração.
- [ ] Reabrir o assistente e recusar confirmação: a calibração válida anterior não é sobrescrita.

### Navegação e manutenção

- [ ] Duplo clique em INICIAR inicia sem novas perguntas; contagem regressiva e aviso visíveis.
- [ ] Um deslocamento em X e outro em Y confirmam direção correta. Ajustar `inverter_y` se necessário.
- [ ] Chegada satisfaz **ambos** `abs(dx) <= tolerancia` e `abs(dy) <= tolerancia`. Não há oscilações persistentes; reduzir `pulso_perto` se necessário.
- [ ] Durante a permanência, provocar **uma deriva controlada** no próprio app. Como exceção supervisionada ao aviso de não interagir, deslocar somente com o joystick solto, sem input simultâneo do bot, ou usar uma condição natural de deriva. Depois não tocar mais nos controles. Verificar que a próxima manutenção (20–45 s após o último ciclo, mais OCR/correção) detecta e corrige sozinha.
- [ ] Posição parada/obstáculo causa falta de progresso ou timeout, não arrastes eternos.
- [ ] Habilitar keep-alive só após confirmar que a tecla escolhida não abre menus, não move o personagem nem tem efeito indesejado. Confirmar pelo comportamento real do app se conta como atividade.

### Emergência — obrigatória antes do noturno

Para **cada condição abaixo**, medir o tempo entre F12/mouse atingir `(0,0)` e liberação efetiva do joystick/último input. Pode usar gravação de tela a 60 fps; conte quadros, não só timestamps do log (a linha de emergência pode faltar em pane). Critério: **menos de 1 segundo**, sem o joystick continuar preso. Repetir sob carga do emulador.

- [ ] F12 durante a contagem regressiva.
- [ ] F12 **durante mouseDown/arraste**, não só entre pulsos.
- [ ] F12 durante processamento OCR lento.
- [ ] Mouse no canto `(0,0)` durante arraste.
- [ ] F12 durante a espera longa de permanência/keep-alive.
- [ ] F12 durante tentativa de reconexão.
- [ ] F12 durante envio de webhook/rede lenta.
- [ ] Após parada, o processo retornou `130` (ou FAILSAFE do PyAutoGUI abortou), não há bot ativo nem input preso. O BAT pode apenas aguardar uma tecla após o erro.
- [ ] Nunca houve aviso Discord de sucesso após abortar.

**Se qualquer teste passar de 1 s ou não soltar o input: não aprove execução desacompanhada.** A arquitetura é projetada para parada rápida, mas esse aceite só pode ser confirmado no ambiente real.

### Falhas e recuperação

- [ ] Alt+Tab/minimização durante pulso solta o mouse; nenhum novo arraste vai para outra janela. O bot recupera a janela quando possível.
- [ ] Fechar/reabrir emulador com mesmo título e tamanho: reconexão aproximadamente a cada 30 s, por no máximo 10 min, sem cliques enquanto indisponível. Usar um timeout temporariamente menor em cópia do config para testar o caminho de falha rápida.
- [ ] Mover janela sem redimensionar: recupera origem relativa e continua com ROI/joystick corretos.
- [ ] Redimensionar: erro explicando necessidade de restaurar tamanho/recalibrar. Janela fora do monitor principal: recusa segura.
- [ ] Readout ilegível/encoberto: três falhas OCR com pausa levam ao encerramento, mouse solto. O log mostra tentativas e motivo.
- [ ] Duas janelas com o título idêntico causam erro; dois BaseBots simultâneos são impedidos.
- [ ] Retirar/renomear Tesseract (apenas em instalação de teste): mensagem de instalação clara, sem inputs.
- [ ] Ao concluir, mensagem `concluído às HH:MM` e webhook opcional recebidos. URL inválida/rede indisponível: diagnóstico sem token, sem novo movimento.

## C — Teste noturno completo (somente depois de B)

- [ ] Calibração e config definitivas revisadas; registrar os parâmetros não secretos usados.
- [ ] Horário futuro correto no relógio local, sem suspensão, bloqueio, reinício programado, UAC pendente ou acesso remoto que altere resolução.
- [ ] Computador ligado à energia; emulador/app já prontos. A abertura opcional do EXE não substitui login/carregamento do app.
- [ ] INICIAR aberto antecipadamente, apenas uma instância. Contagem correta até o horário.
- [ ] Chegada inicial registrada e N minutos contados a partir dela; durante esse período, leituras periódicas e correções observadas no log.
- [ ] Nenhuma oscilação persistente, joystick preso ou janela errada recebeu input.
- [ ] Conclusão normal enviada no horário esperado; processo encerrado, emulador permanece aberto.
- [ ] Verificar retenção/exclusão dos logs antigos e revisar privacidade antes de pedir suporte.

## Registro de aprovação

```text
Data / responsável:
Windows / escala DPI:
Emulador / versão / título / tamanho cliente:
Versão Tesseract:
Commit/build do BaseBot:
Dry-run e testes unitários: PASS / FAIL
Teste curto + deriva: PASS / FAIL
Maior latência F12 medida (s) e condição:
Maior latência canto (0,0) medida (s) e condição:
Perda de janela / falha OCR: PASS / FAIL
Teste noturno: PASS / FAIL
Logs anexados (sem segredos):
Observações e ajustes:
```

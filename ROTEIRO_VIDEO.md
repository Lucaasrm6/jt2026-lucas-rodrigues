# Roteiro de vídeo — até 3 minutos, compartilhando a tela

**Meta:** 2min35–2min50.  
**Formato:** GitHub aberto no `README.md`; sem slides.

## Antes de gravar

Deixe estas abas já abertas:

1. `README.md` no topo;
2. seção Q1/Q2;
3. seção Q3;
4. `ai-log/01_ai_log.md` em “Auditoria do Checkpoint 4”;
5. `scripts/consistency_gate_final.py` ou o resultado `PASS (14/14)`.

Use zoom 110–125%. Feche notificações, histórico de terminal e qualquer aba pessoal.

---

## 0:00–0:17 — decisão

**Tela:** topo do README.

> “Se a Seazone tivesse que decidir hoje, eu colocaria **Morretes, dois quartos**, no topo da diligência de aquisição. Não como compra automática: existe uma condição objetiva que pode inverter essa decisão.”

---

## 0:17–0:50 — Q1 e Q2

**Tela:** “As quatro respostas”.

> “Eu separei duas perguntas que parecem iguais: quem cobra mais e quem usa melhor o capital. **4+ quartos** têm o maior preço-noite, cerca de **R$1.065**, mas **1–2 quartos** são mais eficientes porque o preço de compra cresce mais rápido que a diária.
>
> Em localização, **Meia Praia** lidera o agregado robusto, com **R$600**. Mas controlando tipologia, em dois quartos o Centro cobra **R$580**, Morretes **R$498** e Meia Praia **R$460**. Então parte do resultado agregado era composição de quartos.”

---

## 0:50–1:12 — Q3

**Tela:** seção Q3.

> “Para os drivers, usei **911 anúncios**, com erro clusterizado por proprietário. O modelo estrutural explica cerca de **33%** da variação; com variáveis operacionais chega a **40%**. Um quarto adicional aparece associado a **19%** e operador profissional a **23%** no preço exibido. Associação, não causalidade.”

---

## 1:12–1:48 — Q4 e condição de reversão

**Tela:** tabela “O que eu compraria hoje” e depois o bloco de reversão.

> “Morretes dois quartos combina **R$498 de preço-noite exibido** com **R$790 mil de preço-pedido mediano** e mais de mil ofertas válidas de venda. O CE90 de **3,1%** é apenas um cenário de 90 dias a 55% hipotéticos; não é ROI observado.
>
> O ponto decisivo é este: **se Morretes tiver ocupação mais de 20% abaixo do Centro, eu mudo para Centro dois quartos**. A base não mostra ocupação, então minha confiança é moderada.”

---

## 1:48–2:02 — tese interna

**Tela:** “Posição sobre a tese de compactos no Centro”.

> “Sobre a tese interna: **studio no Centro é inconclusivo**, porque faltam observações comparáveis. Um quarto no Centro é eficiente, mas não lidera o screen. Eu não transformei ausência de dado em confirmação nem rejeição.”

---

## 2:02–2:32 — como usei IA

**Tela:** `ai-log/01_ai_log.md` em “Auditoria do Checkpoint 4”; depois mostre o gate.

> “No uso de IA, eu separei execução, crítica e auditoria. Isso encontrou um bug **OR versus AND** na regra de amostra e rebaixou um proxy temporal que estava forte demais. No freeze final, a auditoria encontrou que o Consistency Gate dizia PASS com checks hard-coded. Eu interrompi o freeze, corrigi também a regressão e só aceitei depois de um gate programático passar **14 de 14 verificações**.”

---

## 2:32–2:50 — mais uma semana

**Tela:** diligência / limitações no README.

> “Com mais uma semana eu validaria primeiro **ocupação real por bairro e fora da alta temporada**, depois preço efetivo de transação e custos operacionais. A ocupação sozinha já testa o limiar que pode inverter a recomendação.”

---

## 2:50–2:57 — fechamento

**Tela:** volte ao topo do README.

> “Hoje, portanto: **diligenciar Morretes dois quartos primeiro; se a ocupação relativa falhar, migrar para Centro dois quartos**.”

---

## Checklist de gravação

- 1080p;
- navegador em 110–125% de zoom;
- feche abas pessoais e notificações;
- deixe README, Q3, AI log e gate já abertos;
- não mostre chaves, caminhos pessoais ou histórico do terminal;
- faça um teste cronometrado antes da tomada final;
- arquivo final abaixo de 3:00;
- Google Drive em **qualquer pessoa com o link**;
- teste o link em janela anônima antes de enviar.

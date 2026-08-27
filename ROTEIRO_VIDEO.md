# Roteiro do vídeo — 2min45 a 2min55

## Preparação da tela

Deixar abertas, nesta ordem:

1. `README.md`;
2. tabela final da recomendação;
3. seção com as quatro perguntas;
4. `ai-log/01_ai_log.md` na parte do C4.1;
5. resultado do Consistency Gate.

Não gastar tempo rolando código de análise. O vídeo deve mostrar a decisão, a evidência e um exemplo concreto de como a IA foi auditada.

---

## 0:00–0:18 — decisão primeiro

**Tela:** README com a recomendação executiva.

**Fala:**

> “Se a Seazone tivesse que alocar capital hoje com essa base, minha primeira busca seria por um apartamento de dois quartos em Morretes. Mas eu não trato isso como uma resposta absoluta: é uma recomendação condicional, porque a variável que mais pode inverter a decisão — ocupação real — não existe nos dados.”

---

## 0:18–0:50 — por que Morretes

**Tela:** tabela final.

**Fala:**

> “O segmento tem preço-noite exibido mediano de 498 reais e preço-pedido mediano de 790 mil. Para comparar aquisição e operação sem fingir que conheço ocupação, usei primeiro um índice simples: preço-noite dividido pelo capital de aquisição. Em um cenário mecânico de 90 dias a 55% de ocupação hipotética, isso equivale a 3,1% do preço de compra. Não é ROI observado e não é forecast.”

---

## 0:50–1:15 — perguntas 1 e 2

**Tela:** respostas Q1/Q2.

**Fala:**

> “Os dados também mostram por que não dá para responder o case com um único ranking. Imóveis de quatro quartos ou mais têm o maior potencial absoluto de diária; os de um e dois quartos são mais eficientes por capital. E, entre bairros com amostra robusta, Meia Praia lidera a mediana agregada, enquanto o Centro melhora quando controlo o mix de quartos. Localização e perfil estavam confundidos no agregado.”

---

## 1:15–1:38 — tese do Centro

**Tela:** bloco da tese interna.

**Fala:**

> “Eu também testei a hipótese de compactos no Centro sem tratá-la como âncora. Para studio, a resposta é simples: a amostra comparável é zero, então eu não inventei um veredito. Para um quarto, há evidência favorável à eficiência, mas não suficiente para superar Morretes dois quartos na decisão final.”

---

## 1:38–2:15 — uso de IA com um caso concreto

**Tela:** AI log na parte do C4.1 e depois o Consistency Gate.

**Fala:**

> “Eu usei IA em ciclos separados de execução e revisão. O caso mais útil aconteceu no último freeze. A primeira versão declarou Consistency Gate 14 de 14. Na revisão do código eu encontrei que os checks estavam hardcoded como `True`. A mesma auditoria encontrou dois problemas na regressão: interpretação de coeficientes log-lineares e uma referência de bairro com amostra muito pequena. Eu rejeitei o freeze, rodei um patch específico e só aceitei a versão final depois de transformar o gate em verificação programática.”

---

## 2:15–2:36 — condição de reversão

**Tela:** threshold de 20%.

**Fala:**

> “A decisão tem um ponto objetivo de quebra: se Morretes operar mais de 20% abaixo do Centro, o ranking de eficiência se inverte. A base não permite dizer se esse limiar acontece. É por isso que minha confiança é moderada, não alta.”

---

## 2:36–2:52 — mais uma semana

**Tela:** limitações / próximos dados.

**Fala:**

> “Com mais uma semana, eu começaria por três validações: ocupação real por bairro e tipologia, preço efetivo de transação e doze meses de sazonalidade. Eu começaria pela ocupação porque ela sozinha pode mudar a compra recomendada.”

---

## 2:52–2:57 — fechamento

**Tela:** volta para a recomendação.

**Fala:**

> “O resultado não é só quem ficou em primeiro na planilha. É saber exatamente o que precisa acontecer para eu mudar de ideia.”

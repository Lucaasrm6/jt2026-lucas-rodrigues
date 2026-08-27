# Roteiro do vídeo — até 3 minutos

Se eu escolhesse pela maior diária, compraria um imóvel grande em Meia Praia. Se apenas aceitasse a tese inicial, compraria um compacto no Centro. Os dados não sustentaram nenhuma dessas respostas.

Comecei verificando o que os arquivos realmente permitiam afirmar. O `Price_AV` não traz receita realizada, e o VivaReal traz preço pedido, não preço de transação. Dos 4.441 anúncios do Airbnb, somente 999 têm preço. Portanto, tratei o problema como decisão sob incerteza, não como previsão.

Depois, separei monetização absoluta de eficiência de capital. Imóveis com quatro quartos ou mais têm a maior diária, mas o custo de aquisição cresce ainda mais. Entre os grupos comparáveis, dois quartos oferece o melhor equilíbrio.

Meia Praia lidera o preço-noite agregado entre os bairros com amostra robusta. Porém, comparando o mesmo número de quartos, o Centro cobra mais. A média do bairro estava misturando localização com o tipo de imóvel disponível.

Juntando preço-noite, aquisição e robustez da amostra, minha prioridade de diligência é Morretes, dois quartos: 498 reais de preço-noite exibido para um preço pedido mediano de 790 mil reais.

Em quatro mil reamostragens por proprietário e anunciante, Morretes ficou em primeiro em 69,8% das vezes entre os cinco finalistas e superou Centro, dois quartos, em 94,7% das comparações. Isso mede estabilidade amostral, não probabilidade de sucesso.

Também testei o que derrubaria a escolha. O movimento do calendário é desfavorável a Morretes e não pode ser chamado de ocupação. Se a ocupação real ficar mais de 20% abaixo da do Centro, eu mudo para Centro, dois quartos. Por isso a confiança é moderada.

A tese de studio no Centro ficou inconclusiva. Centro, um quarto, é eficiente, mas possui somente 21 ofertas válidas e não supera Morretes.

Usei o Antigravity para organizar agentes, handoffs e checkpoints, e o Claude Code para implementar e testar. Em vez de pedir uma resposta pronta, separei execução e revisão. Assim corrigi uma regra que usava `OR` no lugar de `AND`, uma interpretação da regressão e um sinal de calendário que parecia mais forte do que realmente era. O pipeline termina com 20 verificações automáticas.

Minha conclusão não é “compre Morretes”. É: coloque Morretes, dois quartos, no topo da diligência, mantenha Centro como alternativa e só comprometa capital depois de validar ocupação, custos e os imóveis da buy box. O ponto principal é mostrar não apenas por que eu escolheria Morretes, mas qual evidência me faria mudar de ideia.

# Cury Company Delivery :pizza:

<p align="left">
  <img src="img.jpg"  title="Cury Delivery">
</p>

# 1. Problema de negócio
    
A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas. Através desse aplicativo, é possível realizar o pedido de uma refeição, em qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por um entregador também cadastrado no aplicativo da Cury Company.

A empresa realiza negócios entre restaurantes, entregadores e pessoas, e gera muitos dados sobre entregas, tipos de pedidos, condições climáticas, avaliação dos entregadores e etc. Apesar do número de entregas estar crescendo, o CEO não tem visibilidade completa dos KPIs de crescimento da empresa.

A Cury Company possui um modelo de negócio chamado Marketplace, que faz o intermédio do negócio entre três clientes principais: restaurantes, entregadores e pessoas compradoras. Para acompanhar o crescimento desses negócios, o CEO gostaria de ver as seguintes métricas de crescimento:

**Do lado da empresa:**
  1. Quantidade de pedidos por dia.
  2. Quantidade de pedidos por semana.
  3. Distribuição dos pedidos por tipo de tráfego.
  4. Comparação do volume de pedidos por cidade e tipo de tráfego.
  5. A quantidade de pedidos por entregador por semana.
  6. A localização central de cada cidade por tipo de tráfego.

**Do lado do entregador:**
  1. A menor e maior idade dos entregadores.
  2. A pior e a melhor condição de veículos.
  3. A avaliação média por entregador.
  4. A avaliação média e o desvio padrão por tipo de tráfego.
  5. A avaliação média e o desvio padrão por condições climáticas.
  6. Os 10 entregadores mais rápidos por cidade.
  7. Os 10 entregadores mais lentos por cidade.

**Do lado do restaurantes:**
  1. A quantidade de entregadores únicos.
  2. A distância média dos restaurantes e dos locais de entrega.
  3. O tempo médio e o desvio padrão de entrega por cidade.
  4. O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.
  5. O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
  6. O tempo médio de entrega durantes os Festivais.

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.
    
# 2. Premissas do negócio
  1. A análise foi realizada com dados entre 11/02/2022 e 06/04/2022.
  2. Marketplace foi o modelo de negócio assumido.
  3. As 3 principais visões do negócio foram: visão transação de pedidos, visão restaurante e visão entregadores.
   
# 3. Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa:
  1. Visão do crescimento da empresa.
  2. Visão do crescimento dos restaurantes.
  3. Visão do crescimento dos entregadores.

Cada visão é representada pelo seguinte conjunto de métricas:

1. Visão do crescimento da empresa
    1. Pedidos por dia.
    2. Porcentagem de pedidos por condições de trânsito.
    3. Quantidade de pedidos por tipo de tráfego e por cidade.
    4. Pedidos por semana.
    5. Pedidos por entregador por semana.
    
2. Visão do crescimento dos restaurantes
    1. Quantidade de entregadores.
    2. Distância média percorrida.
    3. Tempo médio de entrega durante o festival e dias normais.
    4. Desvio padrão do tempo de entrega durante festivais e dias normais.
    5. Tempo de entrega médio por cidade.
    6. Distribuição do tempo médio de entrega por cidade.
    7. Tempo médio de entrega por tipo de pedido.
    
3. Visão do crescimento dos entregadores
    1. Idade do entregador mais velho e do mais novo.
    2. Avaliação do melhor e do pior veículo.
    3. Avaliação média por entregador.
    4. Avaliação média por condições de trânsito.
    5. Avaliação média por condições climáticas.
    6. Tempo médio do entregador mais rápido por cidade.
        
# 4. Top 3 Insights de dados
  1. A sazonalidade da quantidade de pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em dia sequenciais.
  2. As cidades do tipo “Semi-Urban” não possuem condições baixas de trânsito.
  3. O tempo médio de entrega mais alto é no tipo de cidade “Semi-Urban”.
    
# 5. O produto final do projeto    
Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.    
O painel pode ser acessado através desse link: https://cury-delivery.streamlit.app/
    
# 6. Conclusão    
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.    
Da visão da empresa, podemos concluir que o número de pedidos cresceu entre a semana 06 e a semana 13 do ano de 2022.
    
# 7. Próximo passos
  1. Reduzir o número de métricas.
  2. Criar novos filtros.
  3. Adicionar novas visões de negócio.

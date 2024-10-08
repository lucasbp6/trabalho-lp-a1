Hipótese2 - relatorio
=====================

As equipes que possuem os pit stops mais rápidos são as que geralmente se tornam campeãs
----------------------------------------------------------------------------------------

Para conduzir esta análise, foi necessário realizar uma limpeza e pré-processamento dos dados. 
O primeiro passo envolveu a criação de funções específicas para filtrar e organizar as informações 
de acordo com os parâmetros desejados, uma vez que a análise seria realizada por ano. Para isso, 
foi crucial descobrir as pontuações de cada equipe ao longo dos anos, estabelecendo uma correlação 
entre os IDs das corridas e os resultados obtidos pelas equipes.

Um dos principais desafios enfrentados foi agrupar os pit stops, uma vez que o ID da construtora 
não estava diretamente disponível no arquivo CSV dos pit stops. Para superar esse obstáculo, 
foi necessário cruzar dados entre múltiplos conjuntos, como os de resultados e corridas, a fim 
de obter a associação correta entre os pit stops e suas respectivas equipes. Essa etapa exigiu 
um entendimento cuidadoso da estrutura dos dados e das relações entre as diferentes tabelas.

Outro desafio significativo foi identificar e descartar dados de pit stops que apresentavam 
inconsistências. Por exemplo, tempos de pit stops excessivamente longos poderiam ser indicativos 
de punições ou incidentes que não refletiam a performance normal das equipes. Essa etapa foi crucial, 
pois nossa análise buscava verificar se a eficiência e a velocidade dos pit stops das equipes 
influenciavam suas chances de vitória no campeonato.

Conclusão da analise de dados da hipótese:
------------------------------------------

.. image:: ../images/hipotese2.png

A análise apresentada no gráfico revela uma relação inversa entre a média de pit stops e a 
pontuação dos construtores ao longo dos anos. Os dados indicam que, em geral, as equipes que 
mantêm uma média de pit stops mais rápidos tendem a acumular maior pontuação no campeonato.

Observa-se que, embora existam algumas exceções, a maioria dos pontos no gráfico segue a 
tendência de que equipes com pit stops mais eficientes alcançam melhores resultados. Essa 
correlação sugere que a eficiência nas paradas é um fator crítico para o desempenho das equipes, 
impactando diretamente suas chances de vitória e consistência ao longo das temporadas.

Além disso, a variação dos pontos ao longo dos anos, representada pelas cores, indica que 
essa tendência se mantém relevante em diferentes temporadas, reforçando a importância de 
otimizações nos pit stops para a competitividade das equipes na Fórmula 1.

No entanto, é fundamental considerar que outros fatores também influenciam o desempenho das 
equipes, como a qualidade do carro, a estratégia de corrida e a habilidade dos pilotos. 
Portanto, a análise deve ser vista como parte de um conjunto mais amplo de dados que ajudam 
a compreender a dinâmica da competição.

Hipótese2 - documentação
========================

.. currentmodule:: hipotese2

Documentação do módulo hipotese2.

.. automodule:: hipotese2
   :members:
   :undoc-members:
   :show-inheritance:

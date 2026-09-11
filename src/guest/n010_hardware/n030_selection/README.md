# Selection

## Responsabilidade

`Selection` reúne estruturas combinacionais do GUEST nas quais um sinal controla qual entre outros sinais é propagado para uma saída.

Sua fronteira é a seleção de dados em hardware combinacional. Essas estruturas não introduzem branching, instruções, program counter ou estado, nem transferem ao HOST a decisão sobre qual sinal deve prevalecer.

## Conceitos

### Seleção controlada por dado

Um mesmo `Bit` pode participar de uma composição com diferentes papéis. Em uma estrutura de seleção, um dos sinais atua como controle e determina causalmente qual entre outros sinais será propagado para a saída.

Esse papel não cria um novo tipo de dado nem representa uma escolha de caminho de execução Python. O sinal de controle participa da própria composição lógica.

Para duas entradas `A` e `B`, um seletor `SELECT` pode definir:

| SELECT | OUTPUT |
| ------ | ------ |
| 0      | A      |
| 1      | B      |

Essa relação descreve o comportamento da seleção, mas não concede uma tabela de consulta ao GUEST. A saída deve emergir da composição de capacidades pertencentes ao passado causal.

### Multiplexador

Um **Mux** recebe duas entradas de dados e um bit de seleção. Quando `SELECT = 0`, a saída corresponde a `A`; quando `SELECT = 1`, corresponde a `B`.

O Mux não introduz controle de fluxo. Todos os caminhos lógicos existem simultaneamente na estrutura combinacional; o valor de `SELECT` determina causalmente qual sinal contribui para a saída.

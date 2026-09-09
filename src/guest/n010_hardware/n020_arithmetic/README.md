# Arithmetic

## Responsabilidade

`Arithmetic` reúne estruturas do GUEST que interpretam bits como partes de uma computação aritmética. Sua fronteira é atribuir significado de soma, resultado e carry a sinais lógicos já existentes.

## Conceitos

### Soma combinacional

Uma soma combinacional produz suas saídas apenas pela composição causal das entradas presentes. Ela não armazena resultados, não lembra computações anteriores e não decide caminhos de execução: seu comportamento emerge dos gates e estruturas aritméticas que já existem em seu passado causal.

### Resultado e carry

Ao somar dois bits, uma única saída lógica não é suficiente para representar todos os resultados possíveis. O caso `1 + 1`, por exemplo, produz o valor binário `10`.

Por isso, a soma de uma posição produz duas saídas:

* `SUM`: o bit de resultado da posição atual;
* `CARRY`: o bit que representa valor a ser propagado para a próxima posição, quando tal composição maior existir.

| A | B | CARRY | SUM |
| - | - | ----- | --- |
| 0 | 0 | 0     | 0   |
| 0 | 1 | 0     | 1   |
| 1 | 0 | 0     | 1   |
| 1 | 1 | 1     | 0   |

Essa estrutura é o **Half Adder**: um somador de um bit que recebe apenas os dois bits que deseja somar. Ele não recebe carry de uma posição anterior.

A relação acima revela que `SUM` possui o comportamento de `XOR(A, B)`, enquanto `CARRY` possui o comportamento de `AND(A, B)`. A aritmética não concede essas operações diretamente: ela reutiliza capacidades lógicas já derivadas e passa a interpretá-las como partes de uma soma.

### Carry de entrada

O Half Adder é suficiente quando não existe valor vindo de uma posição anterior. Em uma soma com múltiplas posições, porém, cada posição posterior também precisa considerar o carry produzido pela anterior.

Surge então uma terceira entrada, `CARRY_IN`. Uma estrutura capaz de somar `A`, `B` e `CARRY_IN` é chamada **Full Adder**:

| A | B | CARRY_IN | CARRY_OUT | SUM |
| - | - | -------- | --------- | --- |
| 0 | 0 | 0        | 0         | 0   |
| 0 | 0 | 1        | 0         | 1   |
| 0 | 1 | 0        | 0         | 1   |
| 0 | 1 | 1        | 1         | 0   |
| 1 | 0 | 0        | 0         | 1   |
| 1 | 0 | 1        | 1         | 0   |
| 1 | 1 | 0        | 1         | 0   |
| 1 | 1 | 1        | 1         | 1   |

Enquanto o **Half Adder** soma dois bits sem considerar uma posição anterior, o **Full Adder** incorpora o `CARRY_IN` e produz um novo `CARRY_OUT`.

`CARRY_OUT` pode então alimentar `CARRY_IN` de uma posição posterior. É essa propagação que permitirá que Full Adders sejam encadeados para realizar somas de palavras binárias maiores.

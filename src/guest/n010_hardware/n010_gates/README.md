# Gates

## Responsabilidade

`Gates` reúne funções lógicas derivadas pela composição de NAND e de gates causalmente anteriores. Um gate pertence a este domínio quando representa uma transformação lógica de bits sem atribuir a essa transformação um significado computacional de nível superior, como aritmética ou armazenamento.

## Conceitos

### Derivação lógica

NAND é uma primitiva da Trusted Base. Os demais gates não são primitivos: seu comportamento deve surgir exclusivamente da composição de estruturas lógicas causalmente anteriores.

Como NAND é suficiente para expressar as demais funções lógicas deste domínio, um novo gate não amplia o poder lógico fundamental disponível ao Zero. Ele torna explícita uma função lógica derivada que poderá ser reutilizada causalmente por estruturas posteriores.

### Truth-table

Uma truth-table descreve o comportamento de uma função lógica para todas as combinações possíveis de suas entradas.

No GUEST, ela pode servir para compreender e verificar um gate, mas não para implementá-lo. Declarar diretamente a truth-table de um gate derivado substituiria sua derivação causal pelo resultado que deveria emergir dela.

### Gates fundamentais derivados

A partir de NAND, o Zero deriva progressivamente algumas funções lógicas que passam a compor o vocabulário disponível para estruturas posteriores.

#### NOT

`NOT` inverte um bit.

| A | NOT |
| - | --- |
| 0 | 1   |
| 1 | 0   |

#### AND

`AND` produz `1` somente quando ambas as entradas são `1`.

| A | B | AND |
| - | - | --- |
| 0 | 0 | 0   |
| 0 | 1 | 0   |
| 1 | 0 | 0   |
| 1 | 1 | 1   |

#### OR

`OR` produz `1` quando pelo menos uma das entradas é `1`.

| A | B | OR |
| - | - | -- |
| 0 | 0 | 0  |
| 0 | 1 | 1  |
| 1 | 0 | 1  |
| 1 | 1 | 1  |

#### XOR

`XOR` produz `1` quando as entradas são diferentes.

| A | B | XOR |
| - | - | --- |
| 0 | 0 | 0   |
| 0 | 1 | 1   |
| 1 | 0 | 1   |
| 1 | 1 | 0   |

#### NOR

`NOR` é a negação de `OR`: produz `1` somente quando ambas as entradas são `0`.

| A | B | NOR |
| - | - | --- |
| 0 | 0 | 1   |
| 0 | 1 | 0   |
| 1 | 0 | 0   |
| 1 | 1 | 0   |

#### XNOR

`XNOR` é a negação de `XOR`: produz `1` quando as entradas são iguais.

| A | B | XNOR |
| - | - | ---- |
| 0 | 0 | 1    |
| 0 | 1 | 0    |
| 1 | 0 | 0    |
| 1 | 1 | 1    |

# Gates

## Responsabilidade

`Gates` reúne funções lógicas derivadas pela composição de NAND e de gates causalmente anteriores. Uma gate pertence a este domínio quando representa uma transformação lógica de bits sem atribuir a essa transformação um significado computacional de nível superior, como aritmética ou armazenamento.

## Conceitos

### Derivação lógica

NAND é uma primitiva da Trusted Base. Os demais gates não são primitivos: seu comportamento deve surgir exclusivamente da composição de estruturas lógicas causalmente anteriores. Um novo gate não introduz uma nova capacidade fundamental no universo do Zero; ele oferece uma nova expressão para uma função lógica que já pode ser construída a partir de NAND.

### Truth-table

Uma truth-table descreve o comportamento esperado de uma função lógica para todas as combinações possíveis de suas entradas. No GUEST, ela pode servir para compreender e verificar um gate, mas não para implementá-lo. Declarar diretamente a truth-table de um gate derivado substituiria sua derivação causal pelo resultado que deveria emergir dela.

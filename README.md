# ZERO - Construindo um computador pelos seus axiomas lógicos

## 1. Visão

**Zero** é um projeto para construir um computador a partir de seus axiomas lógicos mínimos, acompanhando explicitamente o surgimento de cada abstração computacional. O objetivo não é construir um computador a partir do zero físico. Zero roda sobre uma máquina real, um sistema operacional, um interpretador Python e todas as abstrações necessárias para hospedar a simulação. O objetivo é chegar ao ZERO LÓGICO.

Dentro do universo construído pelo projeto, nenhuma abstração computacional relevante deve existir sem ter sido explicitamente derivada de primitivas anteriores. No início, existem apenas:

- dois estados lógicos: `0` e `1` (Bit);
- uma operação lógica fundamental: `NAND`.

A partir daí, todo o restante deve surgir progressivamente. Conceitualmente:

1. NAND
2. gates
3. circuitos combinacionais
4. aritmética
5. estado
6. memória
7. arquitetura
8. CPU
9. machine code
10. assembly
11. runtime
12. linguagem
13. estruturas de dados
14. programas

O projeto deve tornar possível responder, para qualquer abstração construída: "de onde isso veio?", e ser capaz de seguir sua cadeia de dependências até `NAND`.

## 2. Motivação

Zero nasce da vontade de compreender computação em um nível inferior ao assembly, já que assembly ainda pressupõe que muitas coisas já existam:

- instruções;
- registradores;
- memória;
- program counter;
- operações aritméticas;
- jumps;
- uma arquitetura;
- uma CPU capaz de interpretar tudo isso.

Aqui, pretendemos atravessar essas abstrações na direção contrária. Em vez de começar com uma máquina e escrever software para ela, o projeto começa praticamente sem máquina alguma e pergunta, progressivamente, o que precisa existir para que a próxima coisa possa existir. O valor principal desse projeto está mais em vivenciar o nascimento das abstrações do que no resultado final, e a árvore de commits do Git reflete muito bem isso ao longo do projeto.

Quando um loop existir, deve ser possível compreender como ele emerge de jumps e branches; quando uma função existir, deve ser possível compreender como ela emerge de memória, stack, convenções e controle de fluxo; quando uma lista existir, deve ser possível compreender sua representação em memória; quando uma classe existir, deve ser possível compreender quais abstrações anteriores tornam objetos e métodos possíveis. O projeto deve permitir observar concretamente o momento em que lógica deixa de parecer apenas lógica e começa a parecer software.

## 3. Objetivo de longo prazo

O primeiro grande marco é executar um simples `Hello World!` em uma máquina construída pelo próprio Zero. Contudo, esse marco não é o objetivo final - ele representa apenas o momento em que hardware suficiente, arquitetura suficiente e software suficiente passaram a existir para produzir um programa reconhecível. Depois disso, o sistema deve continuar sendo extensível. Possíveis evoluções incluem:

- assembler;
- stack;
- funções;
- calling conventions;
- runtime;
- heap;
- arrays;
- listas;
- strings;
- linguagem estruturada;
- compilador;
- biblioteca padrão;
- filesystem;
- multitarefa;
- operating-system-like abstractions;
- self-hosting parcial ou completo.

Zero deve ser tratado como um "motor computacional extensível", e não como um experimento descartável cujo único propósito seja alcançar `Hello, World!`.

## 4. Os dois universos

Zero é dividido conceitualmente em dois universos: HOST e GUEST. Essa separação é fundamental.

### 4.1. HOST

O HOST é o universo hospedeiro, ele existe fora da máquina Zero. Atualmente, Python é a principal tecnologia usada para implementá-lo. O HOST pode utilizar livremente recursos da linguagem hospedeira, incluindo:

- funções;
- classes;
- listas;
- dicionários;
- loops;
- condicionais;
- exceções;
- AST;
- bibliotecas;
- pytest;
- estruturas auxiliares;
- ferramentas de visualização;
- debugger;
- tracing.

O HOST não precisa ser construído a partir de NAND, ele é a infraestrutura que permite que o universo Zero exista. Entre suas responsabilidades podem estar:

- definir os axiomas fundamentais;
- representar elementos necessários à simulação;
- construir e conectar componentes;
- executar a simulação;
- modelar tempo quando isso se tornar necessário;
- observar o estado da máquina;
- depurar;
- visualizar;
- verificar as regras do GUEST.

Uma formulação central é: "o HOST pode construir, simular, observar e verificar o universo".

### 4.2. GUEST

O GUEST é a máquina que está sendo construída. Tudo que possui SEMÂNTICA COMPUTACIONAL DENTRO DA MÁQUINA deve emergir das primitivas disponíveis em camadas inferiores. O GUEST não pode utilizar uma capacidade do Python simplesmente porque Python já sabe realizá-la. Por exemplo: o GUEST não pode utilizar diretamente o `and` do Python para obter um AND lógico. Também não pode considerar que loops, listas, funções, classes ou inteiros arbitrários existam apenas porque Python os possui. Essas abstrações somente passam a existir dentro do GUEST quando forem construídas.

Uma formulação central é: "o GUEST só pode possuir abstrações que tenham sido explicitamente derivadas das primitivas e componentes já existentes abaixo delas".

## 5. Python como linguagem de descrição

O código do GUEST pode ser escrito utilizando sintaxe Python, mas isso não significa que todas as abstrações sintáticas utilizadas para DESCREVER a máquina passam a existir dentro da máquina. É necessário distinguir "construction time" de "execution time". Por exemplo: uma estrutura Python utilizada pelo HOST para descrever a topologia de um circuito não implica que a máquina Zero possua aquela estrutura. Algo conceitualmente parecido com:

```python
Circuit(
    components=[
        NandGate("a", "b", "n1"),
        NandGate("n1", "n1", "out"),
    ]
)
```

pode ser válido mesmo que o GUEST ainda não possua:

- listas;
- strings;
- classes;
- chamadas de função.

Nesse caso, essas construções pertencem ao MECANISMO DE DESCRIÇÃO UTILIZADO PELO HOST. O resultado computacional continua sendo determinado exclusivamente pelos componentes do GUEST. Portanto, o Python pode estruturar a descrição da máquina, mas não pode fornecer a semântica computacional que a máquina deveria construir. Essa fronteira deve ser preservada rigorosamente.

## 6. Trusted Base

Existe inevitavelmente um ponto abaixo do qual o projeto deixa de derivar as coisas, e essa é a TRUSTED BASE do Zero. Inicialmente ela contém apenas o domínio lógico e o axioma lógico fundamental.

### 6.1. Bit

O domínio fundamental é:

```
Bit ∈ {0, 1}
```

`Bit` existe no HOST porque é necessário definir o domínio sobre o qual o axioma opera. A responsabilidade de `Bit` é representar a existência de exatamente dois valores lógicos possíveis, e ele deve permanecer extremamente pequeno. Ele não deve incorporar comportamentos apenas para impedir usos indevidos de Python pelo GUEST. Por exemplo, regras como:

- não utilizar `if bit`;
- não modificar `bit.value`;
- não utilizar operadores nativos;
- não chamar APIs Python arbitrárias;

não pertencem necessariamente a `Bit`. Essas restrições pertencem à fronteira de verificação entre HOST e GUEST (que falaremos sobre daqui a pouco).

O princípio aqui é: "Tipos fundamentais do kernel devem implementar suas invariantes intrínsecas; Restrições sobre como o GUEST pode manipulá-los pertencem ao sistema de verificação".

### 6.2. NAND

`NAND` é o axioma lógico do Zero. Conceitualmente:

```
NAND : Bit × Bit → Bit
```

e:

| (A, B) | NAND |
|--------|------|
| (0, 0) | 1    |
| (0, 1) | 1    |
| (1, 0) | 1    |
| (1, 1) | 0    |

Sua implementação reside no HOST, e ela não precisa ser derivada de alguma operação anterior (essa é precisamente sua condição axiomática). Preferencialmente, a implementação deve tornar essa condição explícita, por exemplo através de uma truth table, em vez de representar NAND como combinação de operadores booleanos do Python. Não porque usar esses operadores no HOST fosse tecnicamente proibido, mas porque uma declaração direta da truth table comunica melhor a natureza fundacional da primitive.
NAND é privilegiado, tudo que surgir posteriormente não é.

## 7. Princípio da derivação

Toda abstração computacional do GUEST deve possuir uma cadeia de derivação. Exemplo:

```
AND
└── NAND
```

Posteriormente:

```
HalfAdder
├── XOR
│   └── NAND
└── AND
    └── NAND
```

Muito mais tarde:

```
for
└── transformação da linguagem
    └── branches / jumps
        └── ISA
            └── CPU
                └── circuitos
                    └── gates
                        └── NAND
```

Outro exemplo:

```
list
└── representação de runtime
    └── operações de memória
        └── RAM
            └── lógica sequencial
                └── NAND
```

E:

```
function
└── calling convention
    ├── stack
    ├── memory
    └── control flow
        └── CPU
            └── NAND
```

Essa rastreabilidade é parte central da identidade do projeto, e não é simplesmente "desejável".

## 8. Princípio das camadas

O GUEST evolui em camadas. Uma camada pode utilizar:

1. primitivas de descrição explicitamente fornecidas pelo HOST;
2. componentes computacionais definidos em camadas anteriores.

Uma camada não pode depender computacionalmente de camadas posteriores. A regra geral é: `Layer N pode depender apenas de Layer < N`. Não é necessário limitar artificialmente uma camada a depender apenas da imediatamente anterior - uma camada aritmética, por exemplo, pode usar diretamente gates fundamentais de uma camada inferior quando isso fizer sentido. A arquitetura deve formar um DAG de dependências orientado para os axiomas.

## 9. Mapa conceitual de camadas

A sequência abaixo funciona como uma ideia para um "mapa de evolução", não como obrigação de criar imediatamente todas essas abstrações.

### Hardware

0. axioma lógico
  - NAND

1. gates fundamentais
  - NOT
  - AND
  - OR
  - XOR
  - ...

2. circuitos combinacionais
  - MUX
  - DEMUX
  - decoders
  - selectors
  - ...

3. aritmética
  - Half Adder
  - Full Adder
  - Adders
  - ...
     
4. lógica sequencial
  - estado
  - latch
  - flip-flop
  - registers
  - counters
  - ...

5. memória
  - register banks
  - RAM
  - addressing
  - ...

6. arquitetura
  - ALU
  - buses
  - register file
  - program counter
  - ...

7. CPU
  - instruction decoder
  - control unit
  - ISA
  - CPU
  - ...

8. máquina
  - ROM
  - RAM
  - CPU
  - I/O
  - memory map
  - ...

### Software

```
00 - machine code
01 - assembly
02 - runtime
03 - linguagem
04 - biblioteca padrão
05 - programas
```

Os nomes e limites exatos podem mudar quando a experiência prática revelar uma divisão melhor (o que não deve mudar é o princípio de derivação progressiva).

## 10. Não criar abstrações antes da necessidade

Uma das regras metodológicas mais importantes do Zero é a de que nenhuma abstração nova deve ser criada antes de existir um problema concreto que exija sua existência. Por exemplo, não devemos criar antecipadamente:

- `Wire`;
- `Signal`;
- `Circuit`;
- `Clock`;
- `Register`;
- `Memory`;
- `Component`;

apenas porque sabemos, pela arquitetura tradicional de computadores, que provavelmente serão úteis. Primeiro deve surgir o problema, e depois procuramos a menor abstração capaz de resolvê-lo. Isso permite compreender o MOTIVO para cada conceito existir. Se em determinado ponto ficar difícil representar a conexão entre componentes, talvez `Wire` passe a ser necessário; se surgir a necessidade de representar valores que mudam no tempo, talvez `Signal` faça sentido; se ambos representarem a mesma coisa, talvez uma das abstrações nem precise existir.

O projeto não deve reproduzir automaticamente arquiteturas conhecidas, ele deve descobrir sua própria arquitetura enquanto os problemas aparecem.

## 11. Repetição antes da abstração

Zero não deve eliminar imediatamente toda repetição. Em determinados momentos, repetir manualmente uma estrutura é pedagogicamente valioso. Por exemplo, antes de introduzir algo como:

```
Adder(width=16)
```

pode ser desejável construir explicitamente várias instâncias equivalentes. O objetivo é perceber concretamente o que está sendo repetido, qual informação varia, qual abstração está faltando e se a abstração pertence ao HOST ou ao GUEST. Somente depois disso deve ser considerada uma conveniência como `width`.

Ou seja, em princípio: antes de automatizar uma repetição importante, compreenda exatamente qual estrutura está sendo repetida e por quê.

## 12. Meta-abstrações versus abstrações computacionais

Essa distinção deve orientar muitas decisões futuras.

### Meta-abstrações

Existem para permitir que o HOST descreva, construa, simule ou observe o GUEST. Exemplos possíveis:

- Circuit;
- Component;
- representação de conexões;
- graph structures;
- construction helpers;
- debugger;
- tracer;
- simulation engine.

Elas não precisam ser derivadas de NAND.

### Abstrações computacionais

Existem dentro da máquina e afetam sua capacidade computacional. Exemplos:

- AND;
- XOR;
- adder;
- register;
- memory;
- instruction;
- branch;
- function;
- list;
- class.

Essas DEVEM ser derivadas. Uma pergunta útil para qualquer nova abstração é: "se eu removesse o HOST após construir a máquina, essa coisa precisaria existir para a computação continuar acontecendo?" Se a resposta for sim, provavelmente é uma abstração do GUEST. Se serve apenas para construir, descrever, simular ou observar o sistema, provavelmente pertence ao HOST.

## 13. Tempo e estado

NAND é funcionalmente completo para lógica booleana combinacional. Porém, construir uma máquina requer eventualmente enfrentar:

- feedback;
- estado;
- passagem de tempo;
- propagação;
- ciclos;
- memória.

Até a introdução desses conceitos, componentes podem ser tratados aproximadamente como:

```
output = f(input)
```

Com estado, passamos para algo conceitualmente parecido com:

```
output(t) = f(input(t), state(t-1))
```

Nesse momento, o HOST provavelmente precisará fornecer uma noção mínima de simulação temporal, mas isso não significa que o HOST deve fornecer memória pronta. O HOST pode fornecer o equivalente às leis físicas necessárias para que estado seja simulável, enquanto o GUEST deve construir memória a partir dessas condições. Em outras palavras, o HOST pode fornecer as condições de existência do tempo, e o GUEST deve construir as abstrações computacionais que usam o tempo. A modelagem exata deve ser decidida somente quando o problema surgir concretamente.

## 14. Validator

Zero deve possuir um mecanismo de verificação capaz de impedir que o GUEST utilize acidentalmente semântica computacional nativa de Python, e essa verificação pertence ao HOST. Seu objetivo não é proteger Python de programadores maliciosos, mas sim garantir a integridade epistemológica do experimento. Exemplos de violações que o validator poderá detectar:

- `a and b` quando AND ainda não tiver sido construído;
- `a + b` quando soma ainda não existir;
- `if bit:` quando branching ainda não existir no universo;
- `a == b` quando comparação estiver sendo realizada pelo Python em vez de um componente derivado;
- atribuições ou mutações não autorizadas;
- imports arbitrários;
- chamadas a funções Python que executem computação que pertence ao GUEST;
- dependências entre camadas inválidas.

O validator deve evoluir conforme o GUEST evoluir, e nunca devemos tentar antecipar todas as regras possíveis no início do projeto. O princípio é que uma regra de verificação surja quando existir uma maneira concreta de violar um princípio do Zero.

## 15. Verificação arquitetural

Idealmente, executar os testes do projeto deve verificar duas dimensões independentes:

### 15.1. Correção

Se o componente produz o comportamento esperado.

Exemplo:

```
NAND(0,0) -> 1
NAND(0,1) -> 1
NAND(1,0) -> 1
NAND(1,1) -> 0
```

### 15.2. Pureza

Se o componente foi construído apenas utilizando os mecanismos permitidos naquela camada. Um AND que devolve corretamente a truth table mas utiliza o `and` de Python está correto comportamentalmente e incorreto arquiteturalmente (o Zero considera ambos os critérios necessários).

## 16. A interface humana pertence ao HOST

O projeto pode possuir uma entrada humana como:

```
main.py
```

ou, no futuro:

```
zero run
zero inspect
zero trace
zero verify
```

Essa interface pertence ao HOST, e ela serve para:

- instanciar experimentos;
- carregar máquinas;
- executar simulações;
- observar resultados;
- imprimir estados;
- depurar.

Um `print()` Python utilizado pela interface HOST não significa que o GUEST já saiba imprimir. O verdadeiro output do GUEST somente existirá quando mecanismos de I/O, representação de dados e software suficiente tiverem sido construídos.

## 17. O significado de "do zero"

Zero não pretende alegar que eliminou todas as dependências externas; isso seria impossível dentro do escopo do projeto. Existem:

- Python;
- interpretador;
- sistema operacional;
- CPU física;
- transistores;
- eletricidade.

O projeto delimita conscientemente sua fronteira. "Do zero", para nós, significa que nenhuma abstração computacional pertencente ao universo do Zero é considerada existente apenas porque o computador hospedeiro já a possui. Essa é a definição operacional de ZERO LÓGICO.

## 18. Elegância e minimalismo

O core do Zero deve ser deliberadamente pequeno: quanto mais fundamental uma camada, maior deve ser a resistência a adicionar conveniências. A Trusted Base deve permanecer especialmente fácil de compreender integralmente. Idealmente, alguém deve conseguir abrir os arquivos mais fundamentais e entender exatamente quais estados existem, quais primitivas existem e quais suposições são feitas. Não devemos adicionar comportamento apenas porque é idiomático em Python, não devemos adicionar métodos apenas porque podem ser úteis algum dia e não devemos adicionar abstrações apenas porque projetos semelhantes tradicionalmente as possuem. É um princípio que, no core, a ausência de funcionalidade seja preferível a funcionalidade sem necessidade demonstrada.

## 19. Descoberta em vez de reprodução

Projetos e materiais como [Nand2Tetris](https://www.nand2tetris.org/) podem servir como referência conceitual. Zero não deve, porém, se transformar simplesmente em uma reimplementação de uma arquitetura previamente definida. Quando possível, devemos permitir que problemas concretos conduzam às decisões. Questões como:

- largura de palavra;
- modelo de registradores;
- stack machine versus register machine;
- organização da memória;
- formato da ISA;
- calling convention;
- linguagem;
- runtime;

não devem ser decididas apenas porque uma arquitetura convencional normalmente funciona daquela maneira. É desejável compreender o problema antes de importar a solução tradicional. É um princípio que o conhecimento prévio possa informar uma decisão, mas não deve substituir a descoberta do problema que justifica a decisão.

## 20. Arquitetura conhecida versus necessidade atual

O projeto possui um mapa aproximado do futuro, mas o filesystem deve refletir preferencialmente o que já existe. Não é necessário criar antecipadamente diretórios vazios para gates, arithmetic, sequential, memory, cpu, runtime, language etc apenas porque sabemos que provavelmente existirão. A árvore do repositório pode servir como registro arqueológico do nascimento da máquina.

Primeiro:

```
HOST
├── Bit
└── NAND
```

Depois o primeiro componente derivado. Depois o próximo, e assim sucessivamente.

## 21. Critério para novas funcionalidades

Antes de introduzir uma nova abstração, helper ou mecanismo, responder:

1. Qual problema concreto apareceu?
2. Esse problema pertence ao HOST ou ao GUEST?
3. A nova abstração possui semântica computacional?
4. Se possui, de quais componentes anteriores ela deriva?
5. Estamos usando Python apenas para descrição ou Python está resolvendo o problema?
6. A abstração precisa existir agora?
7. Existe uma solução menor que preserve os mesmos princípios?
8. Estamos aprendendo por que essa abstração existe ou apenas reproduzindo algo conhecido?

Se essas perguntas não puderem ser respondidas claramente, a implementação provavelmente é prematura.

## 22. Critério para componentes do GUEST

Para cada novo componente computacional deve ser possível registrar conceitualmente:

- Nome
- Responsabilidade
- Inputs
- Outputs
- Dependências permitidas
- Implementação estrutural
- Comportamento esperado
- Testes de correção
- Testes de pureza

Exemplo conceitual:

```
NOT

Input:
    a

Output:
    out

Dependências:
    NAND

Definição:
    out = NAND(a, a)
```

Essa disciplina deve tornar a cadeia de construção explícita.

## 23. Filosofia dos testes

Testes não servem apenas para evitar regressões. No Zero, testes funcionam como PROVAS EXECUTÁVEIS DAS PROPRIEDADES DO UNIVERSO. Um teste de `Bit` demonstra quais valores podem existir. Um teste de `NAND` demonstra a truth table do axioma. Um futuro teste de `NOT` deverá demonstrar tanto sua truth table, quanto sua derivação exclusivamente a partir de componentes permitidos. À medida que o projeto evoluir, a suíte de testes deve se tornar uma forma executável de descrever as leis do universo Zero. E é fortemente recomendado que o projeto não evolua com a suíte de testes quebrada ou com cobertura incompleta.

## 24. Marcos conceituais

A evolução pode ser entendida em eras (essas eras são conceituais, não um cronograma rígido):

### Era 0 - Lógica fundamental

Existem:

- Bit
- NAND

Nada mais deve ser presumido.

### Era 1 - Composição lógica

Começam a surgir componentes derivados:

- NOT
- AND
- OR
- XOR
- ...

É provável que apareça a necessidade de uma representação estrutural de circuitos.

### Era 2 - Computação combinacional

Surgem estruturas maiores:

- MUX
- decoders
- adders
- ALU-like components
- ...

### Era 3 - Tempo e estado

A máquina deixa de ser puramente combinacional. Surgem:

- feedback
- state
- registers
- memory

### Era 4 - Máquina programável

Surgem:

- program counter
- control
- instructions
- ISA
- CPU
- memory model
- I/O

### Era 5 - Software

Bits passam a representar programas. Surgem progressivamente:

- machine code
- assembly
- runtime
- functions
- structured control flow
- language
- data structures
- applications

### Era 6 - Autonomia

Possíveis objetivos futuros:

- self-hosting
- assembler rodando no próprio Zero
- compiler rodando no próprio Zero
- programas cada vez menos dependentes do HOST

## 25. Princípios canônicos

As seguintes afirmações devem ser tratadas como princípios centrais do projeto.

### P1 - Zero lógico

O projeto busca zero lógico, não zero físico.

### P2 - NAND é o axioma lógico

NAND é fornecido pela Trusted Base e não precisa ser derivado.

### P3 - Tudo que é computação no GUEST deve ser derivado

Nenhuma capacidade computacional deve aparecer pronta apenas porque Python a possui.

### P4 - HOST e GUEST são universos distintos

O HOST fornece infraestrutura. O GUEST constitui a máquina.

### P5 - Sintaxe de descrição não implica capacidade computacional

Usar Python para descrever uma estrutura não significa que a máquina possua as abstrações utilizadas por Python para descrevê-la.

### P6 - Abstrações devem nascer de problemas

Não criar abstrações antes de existir necessidade concreta.

### P7 - Repetição pode preceder generalização

É válido repetir manualmente para compreender qual abstração deve surgir.

### P8 - Cada abstração computacional deve possuir ancestralidade

Deve ser possível rastrear sua construção até NAND.

### P9 - Correção não basta

Um componente deve ser correto e construído somente com mecanismos permitidos.

### P10 - O validator protege a fronteira

As regras contra uso indevido da linguagem hospedeira devem ser centralizadas preferencialmente na infraestrutura de verificação, em vez de contaminar os tipos fundamentais.

### P11 - O core deve permanecer pequeno

Elementos fundamentais só devem possuir comportamento essencial à própria definição.

### P12 - Descobrir é mais importante que reproduzir

Arquiteturas conhecidas são referências, não roteiros obrigatórios.

### P13 - Conveniência precisa ser conquistada

Toda abstração poderosa deve surgir depois de compreendermos a complexidade que ela esconde.

## 26. Considerações sobre o desenvolvimento

Durante o desenvolvimento, não avançar automaticamente para a próxima peça conhecida de uma arquitetura de computadores: primeiro observar o estado atual. Depois, identificar o menor problema concreto que impede o próximo avanço, e trabalhar apenas nesse problema. Deve-se evitar grandes scaffolds antecipatórios, não adicionar APIs "para o futuro" e não transformar o HOST silenciosamente em executor da computação do GUEST. Quando houver dúvida, favorecer menos abstração, mais explicitude, mais rastreabilidade e mais entendimento.

A pergunta permanente deve ser: "esta capacidade realmente existe no universo Zero, ou estamos deixando a máquina hospedeira fazê-la por nós?". Se a resposta for a segunda, a implementação deve ser reconsiderada.

## 27. Definição resumida

Zero pode ser resumido como: 

**Um computador construído progressivamente a partir de NAND, em que cada abstração computacional precisa demonstrar como emerge das anteriores, enquanto Python atua somente como universo hospedeiro para construir, simular, observar e verificar essa evolução.**

O sucesso do projeto não será apenas chegar a um programa complexo, será chegar até ele sem perder a capacidade de apontar para cada camada intermediária e explicar: **Foi assim que isso passou a existir.**

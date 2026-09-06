# ZERO - Construindo um computador pelos seus axiomas lógicos

## 1. Visão

**Zero** é um projeto para construir um computador a partir de seus axiomas lógicos mínimos, acompanhando explicitamente o surgimento de cada abstração computacional. O objetivo não é construir um computador a partir do zero físico. Zero roda sobre uma máquina real, um sistema operacional, um interpretador Python e todas as abstrações necessárias para hospedar a simulação. O objetivo é chegar ao ZERO LÓGICO.

Dentro do universo computacional construído pelo projeto, nenhuma abstração pertencente ao GUEST deve existir sem ter sido explicitamente derivada de primitivas anteriores. Do ponto de vista do GUEST, no início existem apenas:

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
- visualizar.

Uma formulação central é: "o HOST pode construir, simular e observar o universo".

### 4.2. GUEST

O GUEST é a máquina que está sendo construída. Tudo que possui SEMÂNTICA COMPUTACIONAL DENTRO DA MÁQUINA deve emergir da Trusted Base ou de componentes que já existam causalmente antes dele. O GUEST não pode utilizar uma capacidade do Python simplesmente porque Python já sabe realizá-la. Por exemplo: o GUEST não pode utilizar diretamente o `and` do Python para obter um AND lógico. Também não pode considerar que loops, listas, funções, classes ou inteiros arbitrários existam apenas porque Python os possui. Essas abstrações somente passam a existir dentro do GUEST quando forem construídas. Uma formulação central é: "o GUEST só pode possuir abstrações que tenham sido explicitamente derivadas da Trusted Base e de componentes que já existiam causalmente antes delas".

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

## 6. Trusted Base e kernel do HOST

A arquitetura do HOST distingue deliberadamente duas responsabilidades fundamentais: a `trusted_base` e o `kernel`. Elas podem ser pequenas e até parecer relacionadas em determinados momentos, mas não representam o mesmo conceito. A estrutura fundamental é:

```
src/host/
├── kernel/
└── trusted_base/
    ├── bit.py
    └── NAND.py
```

A separação existe para que a estrutura do projeto torne explícito o que é axioma concedido ao GUEST e o que é mecanismo interno do universo hospedeiro.

### 6.1. Trusted Base

Existe inevitavelmente um ponto abaixo do qual o projeto deixa de derivar capacidades computacionais, e essa é a TRUSTED BASE do Zero. A Trusted Base é a superfície axiomática explicitamente concedida ao GUEST. Tudo que estiver em `src/host/trusted_base/` pode ser utilizado diretamente pelo GUEST sem precisar ser derivado de componentes anteriores. Por isso, adicionar qualquer elemento a essa pasta é uma decisão epistemológica fundamental: significa declarar que aquela capacidade passa a existir no universo Zero sem precisar ser conquistada. Inicialmente, a Trusted Base contém somente:

- o domínio lógico `Bit`;
- o axioma lógico `NAND`.

A Trusted Base deve permanecer mínima, explícita e fácil de compreender integralmente.

#### 6.1.1. Bit

O domínio fundamental é:

```
Bit ∈ {0, 1}
```

`Bit` reside em `src/host/trusted_base/` porque é necessário definir o domínio sobre o qual o axioma opera. Sua responsabilidade é representar a existência de exatamente dois valores lógicos possíveis, e ele deve permanecer extremamente pequeno. Ele não deve incorporar comportamentos apenas para impedir usos indevidos de Python pelo GUEST. Por exemplo, regras como:

- não utilizar `if bit`;
- não modificar `bit.value`;
- não utilizar operadores nativos;
- não chamar APIs Python arbitrárias;

não pertencem necessariamente a `Bit`. Essas restrições pertencem à suíte de conformance, responsável por provar que o código do GUEST respeita as leis do universo Zero. O princípio aqui é: "Tipos fundamentais da Trusted Base devem implementar suas invariantes intrínsecas; restrições sobre como o código do GUEST pode utilizar a linguagem hospedeira pertencem aos testes de conformance".

#### 6.1.2. NAND

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

Sua implementação reside em `src/host/trusted_base/`, e ela não precisa ser derivada de alguma operação anterior - essa é precisamente sua condição axiomática. Preferencialmente, a implementação deve tornar essa condição explícita, por exemplo através de uma truth table, em vez de representar NAND como combinação de operadores booleanos do Python. Não porque usar esses operadores no HOST fosse tecnicamente proibido, mas porque uma declaração direta da truth table comunica melhor a natureza fundacional da primitive.

NAND é privilegiado; tudo que surgir posteriormente no GUEST não é.

### 6.2. Kernel

O `kernel` é o núcleo interno do HOST: o conjunto de mecanismos fundamentais necessários para implementar, operar ou simular o universo hospedeiro, mas que não são automaticamente concedidos ao GUEST como capacidades computacionais. Um mecanismo pode ser fundamental para o HOST sem ser um axioma do GUEST. Por exemplo, se a simulação precisar de mecanismos internos de propagação, agendamento de eventos ou estado de simulação, essas capacidades podem pertencer ao `kernel` sem se tornarem acessíveis ao GUEST. Portanto:

- trusted_base/ (capacidades axiomáticas expostas ao GUEST)
- kernel/ (mecanismos internos fundamentais do HOST)

O GUEST pode acessar `src.host.trusted_base.*`. O GUEST não pode acessar `src.host.kernel.*`. Essa distinção é deliberadamente estrutural. Ela impede que adicionar uma nova infraestrutura fundamental ao HOST aumente silenciosamente a superfície privilegiada disponível ao GUEST.

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

## 8. Princípio da ordem causal

As categorias conceituais do GUEST - gates, circuitos combinacionais, aritmética, memória, CPU etc. - servem para organizar abstrações relacionadas, mas não determinam sozinhas quais dependências são permitidas. Dois componentes da mesma categoria podem possuir uma relação causal entre si. O que governa dependências é a ORDEM CAUSAL. Cada unidade arquitetural do GUEST possui uma posição causal explícita em seu caminho, representada por prefixos no formato `nDDD_`. Por exemplo:

```
n010_hardware/
└── n010_gates/
    ├── n010_NOT.py
    ├── n020_AND.py
    └── n030_OR.py
```

Uma unidade do GUEST pode depender apenas de unidades cuja posição causal seja estritamente anterior à sua. Formalmente, para uma dependência `A -> B`, `position(B) < position(A)`. Portanto:

```
n020_AND -> n010_NOT    permitido
n020_AND -> n020_AND    proibido
n020_AND -> n030_OR     proibido
```

A comparação considera a posição causal completa representada pelo caminho. Assim, componentes pertencentes à mesma categoria podem reutilizar componentes anteriores da própria categoria, enquanto componentes de categorias posteriores podem reutilizar qualquer componente que pertença ao seu passado causal. Essa regra faz com que todas as dependências computacionais do GUEST apontem para trás e, consequentemente, impede ciclos por construção. Os prefixos representam exclusivamente ordem causal. Não representam importância, versão, estabilidade ou prioridade.

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

## 10. Não criar abstrações computacionais do GUEST antes da necessidade

Uma das regras metodológicas mais importantes do Zero é que nenhuma nova abstração COMPUTACIONAL DO GUEST deve ser criada antes de existir um problema concreto que exija sua existência. Por exemplo, não devemos introduzir antecipadamente no GUEST:

- `Wire`;
- `Signal`;
- `Circuit`;
- `Clock`;
- `Register`;
- `Memory`;
- `Component`;

apenas porque sabemos, pela arquitetura tradicional de computadores, que provavelmente serão úteis. Primeiro deve surgir o problema computacional, e depois procuramos a menor abstração capaz de resolvê-lo. Isso permite compreender o MOTIVO para cada conceito existir. Se em determinado ponto ficar difícil representar a conexão entre componentes, talvez `Wire` passe a ser necessário; se surgir a necessidade de representar valores que mudam no tempo, talvez `Signal` faça sentido; se ambos representarem a mesma coisa, talvez uma das abstrações nem precise existir. O projeto não deve reproduzir automaticamente arquiteturas conhecidas; o GUEST deve descobrir sua própria arquitetura enquanto os problemas computacionais aparecem. Esse princípio não exige que a ESTRUTURA DO PROJETO seja improvisada da mesma forma. Boundaries entre HOST, GUEST, Trusted Base, kernel e conformance podem e devem ser pensadas preventivamente quando isso torna violações conceituais futuras mais difíceis. Estrutura arquitetural preventiva não concede novas capacidades computacionais ao GUEST.

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

Nesse momento, o HOST provavelmente precisará fornecer uma noção mínima de simulação temporal, mas isso não significa que o HOST deve fornecer memória pronta. O HOST pode fornecer o equivalente às leis físicas necessárias para que estado seja simulável, enquanto o GUEST deve construir memória a partir dessas condições. Em outras palavras, o HOST pode fornecer as condições de existência do tempo, e o GUEST deve construir as abstrações computacionais que usam o tempo. Se esses mecanismos temporais forem apenas infraestrutura interna da simulação, eles pertencem ao `kernel`, não à Trusted Base, e permanecem inacessíveis ao GUEST. Somente uma decisão explícita de promover alguma capacidade à Trusted Base poderia torná-la axiomática. A modelagem exata deve ser decidida quando o problema surgir concretamente.

## 14. Conformance do GUEST

Além dos testes que verificam o comportamento dos componentes, Zero possui uma suíte de CONFORMANCE responsável por provar estaticamente que o código do GUEST respeita as leis fundamentais de construção do universo. Essa verificação pertence ao ambiente de desenvolvimento, não ao HOST nem ao GUEST. Sua estrutura conceitual inicial é deliberadamente pequena:

```
tests/conformance/
├── test_causal_dependencies.py
├── test_guest_language.py
└── test_host_boundary.py
```

Cada arquivo corresponde a uma das três leis fundamentais. As leis são deliberadamente poucas e estáveis; o que pode crescer, especialmente na primeira, é a sofisticação necessária para detectar novas formas de violação.

### 14.1. L1 - Pureza da linguagem hospedeira

O código do GUEST não pode utilizar semântica computacional nativa de Python para realizar trabalho que deveria pertencer ao próprio Zero. Contudo, Python pode continuar sendo utilizado como uma linguagem restrita de descrição e composição. Construções como `def`, chamadas de componentes, `return`, imports permitidos, type annotations e nomes temporários podem representar a estrutura da máquina sem implicar que essas abstrações existam computacionalmente dentro dela. O que não pode acontecer é Python produzir o resultado computacional no lugar do GUEST. Entre as formas proibidas estão, inicialmente:

- `True` e `False`;
- `and`, `or` e `not`;
- `if`, `for` e `while`;
- operadores aritméticos;
- comparações nativas;
- builtins ou APIs Python que realizem computação pelo GUEST;
- leitura ou mutação da representação interna de objetos para contornar componentes derivados.

Se uma construção nativa de Python for necessária futuramente apenas para construir, gerar ou simular uma estrutura, essa lógica pertence ao HOST, e não deve ser introduzida como atalho dentro do código do GUEST. A lei é estável: Python não pode computar pelo GUEST. O que pode crescer ao longo do projeto é apenas o catálogo de construções capazes de violá-la e a precisão da análise necessária para detectá-las.

### 14.2. L2 - Dependência causal

Uma unidade do GUEST só pode depender de unidades do GUEST que pertençam estritamente ao seu passado causal. Formalmente:

```
A -> B  somente se  position(B) < position(A)
```

A própria estrutura de prefixos causais deve ser válida, não ambígua e suficiente para determinar essa ordem. Prefixos ausentes, inválidos ou duplicados também tornam a relação causal inválida, porque impedem que a lei seja determinada de forma inequívoca.

### 14.3. L3 - Fronteira com o HOST

O GUEST não pode acessar arbitrariamente o HOST nem qualquer biblioteca hospedeira. Sua única passagem privilegiada para fora do próprio GUEST é a Trusted Base. A própria estrutura do projeto materializa essa regra:

```
GUEST -> src.host.trusted_base.*    permitido
GUEST -> src.host.kernel.*          proibido
GUEST -> qualquer outro src.host.*  proibido
GUEST -> stdlib / third-party       proibido
```

Portanto, um componente do GUEST pode depender somente de:

1. componentes pertencentes ao seu passado causal;
2. elementos pertencentes a `src/host/trusted_base/`.

Qualquer outro acesso é uma violação de conformance. Essas três leis formam o contrato fundamental do código do GUEST. Novas técnicas de detecção podem surgir ao longo do projeto, especialmente para L1, sem que isso implique o surgimento contínuo de novas leis fundamentais.

## 15. Dimensões de verificação

A suíte de testes do Zero deve verificar duas dimensões independentes:

### 15.1. Correção

Se o componente produz o comportamento esperado.

Exemplo:

```
NAND(0,0) -> 1
NAND(0,1) -> 1
NAND(1,0) -> 1
NAND(1,1) -> 0
```

### 15.2. Conformidade

Se o componente foi construído respeitando as leis do GUEST. Um AND que devolve corretamente sua truth table mas utiliza o `and` de Python está correto comportamentalmente e inválido quanto à conformance. Correção responde: "O componente produz o resultado esperado?", e Conformance responde: "O componente chegou a esse resultado apenas por meios legítimos dentro do universo Zero?" - Zero exige ambas.

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

## 18. Elegância, minimalismo e solidez estrutural

O núcleo COMPUTACIONAL do Zero deve ser deliberadamente pequeno: quanto mais fundamental uma capacidade do GUEST, maior deve ser a resistência a adicionar conveniências. A Trusted Base merece resistência ainda maior, porque tudo que entra nela passa a existir axiomaticamente e deixa de precisar de derivação. Idealmente, alguém deve conseguir abrir `src/host/trusted_base/` e compreender integralmente quais estados existem, quais primitivas foram concedidas e quais suposições computacionais o GUEST recebeu sem conquistar. Não devemos adicionar comportamento a essas primitivas apenas porque é idiomático em Python, não devemos adicionar métodos apenas porque podem ser úteis algum dia e não devemos conceder abstrações computacionais apenas porque projetos semelhantes tradicionalmente as possuem. Na Trusted Base e nas camadas fundamentais do GUEST, ausência de funcionalidade é preferível a funcionalidade sem necessidade demonstrada. Essa preferência por minimalismo computacional não significa minimalismo ingênuo na ESTRUTURA DO PROJETO. A estrutura de diretórios, boundaries e suítes de verificação deve ser suficientemente robusta para tornar erros conceituais difíceis de introduzir. Separações como `host/trusted_base`, `host/kernel`, `guest` e `tests/conformance` podem ser definidas antecipadamente porque não concedem capacidades ao GUEST; elas codificam e protegem invariantes que já conhecemos.

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

## 20. Estrutura do projeto versus evolução do GUEST

O projeto possui duas necessidades diferentes que não devem ser confundidas. A ESTRUTURA FUNDAMENTAL DO PROJETO deve ser pensada de forma robusta o suficiente para materializar boundaries conhecidas e dificultar violações conceituais futuras. Por exemplo:

```
src/
├── guest/
└── host/
    ├── kernel/
    ├── trusted_base/
    │   ├── bit.py
    │   └── NAND.py
    └── main.py
tests/
├── unit/
└── conformance/
```

Essas divisões existem porque representam responsabilidades já conhecidas: computação derivada, infraestrutura interna do HOST, superfície axiomática concedida ao GUEST e provas executáveis das leis do GUEST.  Dentro do GUEST, porém, o filesystem deve refletir preferencialmente aquilo que já nasceu computacionalmente. Não é necessário criar antecipadamente diretórios vazios para arithmetic, sequential, memory, cpu, runtime, language etc. apenas porque sabemos que provavelmente existirão. A árvore do GUEST deve funcionar como registro arqueológico do nascimento da máquina. Portanto, é válido antecipar BOUNDARIES ESTRUTURAIS conhecidas do projeto, mas não capacidades computacionais hipotéticas do GUEST.

## 21. Critério para novas capacidades do GUEST

Antes de introduzir uma nova abstração ou conveniência COMPUTACIONAL no GUEST, responder:

1. Qual problema concreto apareceu?
2. Essa nova capacidade possui semântica computacional?
3. De quais componentes anteriores ela deriva?
4. Sua posição causal e suas dependências são legítimas?
5. Estamos usando Python apenas para descrição ou Python está resolvendo o problema?
6. A capacidade precisa existir agora?
7. Existe uma solução menor que preserve os mesmos princípios?
8. Estamos aprendendo por que essa abstração existe ou apenas reproduzindo algo conhecido?

Se essas perguntas não puderem ser respondidas claramente, a implementação no GUEST provavelmente é prematura. Esse critério não impede que a estrutura do HOST, dos testes ou do repositório seja projetada preventivamente para codificar boundaries e invariantes já conhecidos. O que não deve ser antecipado é a existência de capacidades computacionais que o GUEST ainda não precisou conquistar.

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
- Cobertura pelas leis globais de conformance

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

Testes não servem apenas para evitar regressões. No Zero, eles funcionam como PROVAS EXECUTÁVEIS DAS PROPRIEDADES DO UNIVERSO. Os testes unitários provam comportamento e invariantes locais. Um teste de `Bit` demonstra quais valores podem existir; um teste de `NAND` demonstra a truth table do axioma; os testes dos componentes derivados demonstram seu comportamento esperado. Separadamente, a suíte de `conformance` prova propriedades globais da construção: que o GUEST não utiliza semântica computacional indevida de Python, que suas dependências respeitam a ordem causal e que sua única passagem para o HOST é `src/host/trusted_base/`. Assim:

- unit tests (provam comportamento)
- conformance tests (provam legitimidade da construção)

À medida que o projeto evoluir, a suíte de testes deve se tornar uma descrição executável tanto do comportamento quanto das leis fundamentais do universo Zero. É fortemente recomendado que o projeto não evolua com a suíte de testes quebrada ou com cobertura incompleta.

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

### P6 - Abstrações computacionais do GUEST devem nascer de problemas

Não criar capacidades computacionais no GUEST antes de existir necessidade concreta.

### P7 - Repetição pode preceder generalização

É válido repetir manualmente para compreender qual abstração computacional deve surgir.

### P8 - Cada abstração computacional deve possuir ancestralidade

Deve ser possível rastrear sua construção até a Trusted Base e, para a lógica derivada, até NAND.

### P9 - Correção não basta

Um componente deve ser correto e construído somente com mecanismos permitidos.

### P10 - Conformance protege as leis do GUEST

As restrições impostas ao código do GUEST devem ser provadas por uma suíte de conformance externa à máquina e ao HOST, em vez de contaminar os tipos fundamentais com mecanismos defensivos.

### P11 - A Trusted Base deve permanecer mínima

Tudo que entra em `src/host/trusted_base/` passa a ser uma capacidade axiomática diretamente disponível ao GUEST e, por isso, deve exigir justificativa excepcionalmente forte.

### P12 - Descobrir é mais importante que reproduzir

Arquiteturas conhecidas são referências, não roteiros obrigatórios para a evolução computacional do GUEST.

### P13 - Conveniência computacional precisa ser conquistada

Toda abstração computacional poderosa deve surgir depois de compreendermos a complexidade que ela esconde.

### P14 - Python não pode computar pelo GUEST

A linguagem hospedeira pode descrever e compor a máquina, mas não pode fornecer a semântica computacional que a máquina deveria construir.

### P15 - Toda dependência do GUEST aponta para o passado causal

Uma unidade do GUEST só pode depender de unidades que a precedam causalmente.

### P16 - A Trusted Base é a única passagem privilegiada para o HOST

O GUEST pode acessar diretamente `src.host.trusted_base.*` e não pode acessar `src.host.kernel.*`, outros módulos do HOST, bibliotecas hospedeiras ou recursos externos.

### P17 - Kernel e Trusted Base possuem responsabilidades distintas

A Trusted Base contém capacidades axiomáticas concedidas ao GUEST. O `kernel` contém mecanismos internos fundamentais do HOST e não faz parte da superfície disponível ao GUEST.

### P18 - Estrutura pode ser preventiva; computação deve ser conquistada

A estrutura do projeto pode antecipar boundaries e invariantes já conhecidas para dificultar violações conceituais futuras. Essa antecipação estrutural não autoriza criar capacidades computacionais do GUEST antes da necessidade.

## 26. Considerações sobre o desenvolvimento

Durante a evolução COMPUTACIONAL DO GUEST, não avançar automaticamente para a próxima peça conhecida de uma arquitetura de computadores. Primeiro observar o estado atual; depois identificar o menor problema concreto que impede o próximo avanço; então trabalhar apenas nesse problema. Não criar APIs, abstrações ou capacidades no GUEST apenas "para o futuro" e não transformar silenciosamente o HOST em executor da computação que o GUEST deveria conquistar. Ao mesmo tempo, a arquitetura do PROJETO deve ser tratada como infraestrutura de proteção conceitual. Boundaries conhecidas podem ser representadas explicitamente e com antecedência quando isso reduz a possibilidade de erros futuros. `host/trusted_base`, `host/kernel`, `guest` e `tests/conformance` existem para tornar determinadas classes de violação estruturalmente difíceis, e não porque representem capacidades futuras da máquina. Portanto, o princípio não é "nunca antecipar estrutura". O princípio é: antecipar e solidificar as FRONTEIRAS que já conhecemos, mas não antecipar as CAPACIDADES COMPUTACIONAIS que o GUEST ainda não precisou construir. A pergunta permanente sobre o GUEST deve ser: "esta capacidade realmente existe no universo Zero, ou estamos deixando a máquina hospedeira fazê-la por nós?". Se a resposta for a segunda, a implementação deve ser reconsiderada.

## 27. Definição resumida

Zero pode ser resumido como: 

**Um computador construído progressivamente a partir de uma Trusted Base mínima de Bit e NAND, em que cada abstração computacional do GUEST precisa demonstrar como emerge das anteriores, enquanto o HOST fornece somente a infraestrutura necessária para construir, simular e observar essa evolução, e uma suíte de conformance prova que o GUEST usa apenas seu passado causal e a superfície axiomática explicitamente concedida.**

O sucesso do projeto não será apenas chegar a um programa complexo, será chegar até ele sem perder a capacidade de apontar para cada camada intermediária e explicar: **Foi assim que isso passou a existir.**
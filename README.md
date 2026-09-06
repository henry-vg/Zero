# ZERO - Construindo um computador pelos seus axiomas lógicos

## 1. Visão

**Zero** é um projeto para construir um computador a partir de seus axiomas lógicos mínimos, acompanhando explicitamente o surgimento de cada abstração computacional. O objetivo NÃO É partir do zero físico. Zero roda sobre uma máquina real, um sistema operacional e uma linguagem hospedeira. O objetivo é atingir o **zero lógico**:

> Nenhuma capacidade computacional pertencente ao universo do Zero deve ser considerada existente apenas porque a máquina hospedeira já a possui.

O ponto de partida computacional é uma Trusted Base mínima:

```
Bit ∈ {0, 1}

NAND : Bit × Bit -> Bit
```

A partir dela, toda capacidade do computador deve ser construída progressivamente. O requisito central do projeto é a **rastreabilidade causal**: para qualquer abstração computacional do GUEST, deve ser possível responder "de onde isso veio?" e seguir sua cadeia de derivação até a Trusted Base - e, para a lógica derivada, até `NAND`.

## 2. Motivação e objetivo

Assembly ainda pressupõe que muitas abstrações já existam: instruções, registradores, memória, operações aritméticas, jumps, program counter, arquitetura e uma CPU capaz de interpretar tudo isso. Zero percorre esse caminho na direção contrária: em vez de começar com uma máquina pronta e escrever software para ela, o projeto começa com quase nenhuma capacidade computacional e deixa que cada nova necessidade revele a próxima abstração. O valor do projeto está tanto no resultado quanto em **vivenciar o nascimento das abstrações**: compreender concretamente como lógica se torna aritmética, estado, memória, arquitetura, instruções, software e, eventualmente, programas de alto nível.

O primeiro grande marco é executar `Hello, World!` em uma máquina construída pelo próprio Zero, mas esse marco não encerra o projeto. Zero deve permanecer extensível o suficiente para continuar evoluindo em direção a runtime, linguagem, biblioteca padrão, sistemas mais complexos e, possivelmente, self-hosting parcial ou completo. Uma trajetória conceitual possível é:

0. NAND
1. gates
2. circuitos combinacionais
3. aritmética
4. estado
5. memória
6. arquitetura
7. CPU
8. machine code
9. assembly
10. runtime
11. linguagem
12. estruturas de dados
13. programas

Essa sequência é um mapa de compreensão, não uma arquitetura pronta a ser reproduzida.

## 3. HOST, GUEST e Trusted Base

Zero é organizado em dois universos conceitualmente distintos: HOST e GUEST. A Trusted Base pertence ao HOST e define a pequena superfície axiomática que o GUEST pode acessar diretamente.

### 3.1. HOST

O **HOST** é o universo hospedeiro no qual Zero é construído e simulado. Ele pode usar livremente os recursos da linguagem e da máquina hospedeira para:

- descrever e construir estruturas;
- instanciar experimentos;
- simular;
- fornecer estímulos;
- modelar mecanismos físicos de simulação, como propagação ou passagem de tempo;
- observar resultados;
- depurar, inspecionar e visualizar.

O HOST não precisa ser derivado de `NAND`, o seu papel é fornecer as condições para que o universo Zero exista, mas **sem realizar no lugar do GUEST a computação que o GUEST deveria construir**. Se a simulação exigir no futuro mecanismos como tempo, propagação ou agendamento de eventos, o HOST pode fornecê-los como infraestrutura de simulação. Isso não autoriza o HOST a fornecer memória, registradores, branching, aritmética, interpretação de instruções ou qualquer outra capacidade computacional que pertença à máquina. O HOST pode chamar componentes diretamente durante testes, inspeção ou desenvolvimento. Isso é um harness de desenvolvimento, não significa que uma máquina Zero completa já esteja executando autonomamente. Uma execução genuinamente pertencente ao GUEST emerge quando o HOST se limita a fornecer condições externas - construção, estímulos, tempo e observação - enquanto a causalidade computacional acontece dentro da estrutura construída pelo GUEST.

> O HOST fornece as condições da execução; o GUEST fornece a computação.

### 3.2. GUEST

O **GUEST** é o computador que está sendo construído - tudo que possui semântica computacional dentro da máquina deve emergir de:

1. capacidades explicitamente concedidas pela Trusted Base;
2. componentes do GUEST que já existam causalmente antes dele.

O GUEST não pode utilizar uma capacidade nativa da linguagem hospedeira apenas porque ela já existe. Um `and` nativo não substitui um AND construído. Um `if` nativo não cria branching. Uma lista Python não significa que Zero já possui listas. O mesmo vale para números arbitrários, loops, funções, classes, memória, controle de fluxo e qualquer outra abstração computacional.

### 3.3. Trusted Base

A **Trusted Base** é a superfície axiomática que o GUEST recebe sem precisar derivá-la.

Ela é deliberadamente mínima:

- `Bit`;
- `NAND`.

No código, sua superfície pública reside em:

```
src.host.trusted_base
```

O GUEST pode acessar somente essa superfície do HOST. Adicionar uma nova capacidade à Trusted Base é uma decisão fundamental: significa declarar que aquela capacidade passa a existir no universo Zero sem precisar ser conquistada. Por isso, a Trusted Base deve permanecer pequena, explícita e integralmente compreensível.

#### Bit

`Bit` define o domínio lógico fundamental:

```
Bit ∈ {0, 1}
```

Sua responsabilidade é representar exatamente esses dois estados. `Bit` deve implementar apenas suas invariantes intrínsecas. Restrições destinadas a impedir que o GUEST use Python para trapacear não devem ser incorporadas ao tipo apenas como mecanismos defensivos; elas pertencem à suíte de conformance.

#### NAND

`NAND` é o axioma lógico operacional:

```
NAND : Bit × Bit -> Bit
```

| A | B | NAND |
|---|---|------|
| 0 | 0 | 1    |
| 0 | 1 | 1    |
| 1 | 0 | 1    |
| 1 | 1 | 0    |

Por ser axiomático, `NAND` pode ter seu comportamento declarado diretamente. Uma truth table é uma representação apropriada porque torna explícito que sua semântica é concedida, e não derivada. Componentes posteriores do GUEST não recebem esse privilégio: seu comportamento deve emergir da composição de capacidades já existentes.

## 4. Python como linguagem de descrição

Python é uma linguagem hospedeira usada para **descrever e compor** o Zero. Sua sintaxe não implica automaticamente capacidades computacionais dentro do GUEST. Por exemplo:

```python
def AND(a: Bit, b: Bit) -> Bit:
    return NOT(NAND(a, b))
```

A existência de `def`, parâmetros, `return` e chamadas de função nesse código não significa que o computador Zero já possua funções como abstração de runtime. Nesse contexto, essas construções pertencem à linguagem usada para descrever a composição. A semântica computacional de AND continua vindo apenas de componentes já conquistados. A regra é:

> Python pode estruturar a descrição da máquina, mas não pode fornecer a semântica computacional que a máquina deveria construir.

Essa distinção também separa **meta-abstrações** de **abstrações computacionais**. Meta-abstrações existem para construir, simular ou observar o GUEST e pertencem ao HOST; Abstrações computacionais existem como capacidades da máquina e pertencem ao GUEST. Uma pergunta útil é:

> Se o HOST deixasse de existir depois que a máquina estivesse construída, essa abstração ainda precisaria existir para que a computação continuasse?

Se sim, ela provavelmente pertence ao GUEST.

## 5. Derivação e ordem causal

Toda abstração computacional do GUEST deve possuir ancestralidade explícita. Exemplo:

```
AND
└── NAND
```

Mais tarde, uma abstração maior pode depender de outras já derivadas:

```
HalfAdder
├── XOR
│   └── NAND
└── AND
    └── NAND
```

A organização conceitual em gates, aritmética, memória, CPU ou software não determina sozinha quais dependências são permitidas. O que governa as dependências é a **ordem causal**. Cada unidade arquitetural do GUEST possui uma posição causal explícita em seu caminho, usando prefixos no formato:

```
nDDD_
```

Exemplo:

```
n010_hardware/
└── n010_gates/
    ├── n010_NOT.py
    ├── n020_AND.py
    └── n030_OR.py
```

Para uma dependência:

```
A -> B
```

deve valer:

```
position(B) < position(A)
```

Portanto:

```
n020_AND -> n010_NOT  (permitido)
n020_AND -> n020_AND  (proibido)
n020_AND -> n030_OR   (proibido)
```

A posição causal considera o caminho completo, e os prefixos representam apenas ordem causal: não representam versão, importância, estabilidade ou prioridade. Para que essa ordem seja verificável:

- toda unidade arquitetural do GUEST deve possuir posição causal válida;
- posições causais entre siblings devem ser não ambíguas;
- toda dependência GUEST -> GUEST deve apontar estritamente para o passado.

Essa regra torna o grafo de dependências acíclico por construção.

## 6. Leis de conformance

Correção comportamental não é suficiente. Um componente pode produzir a resposta certa usando mecanismos que o Zero ainda não conquistou. Por isso, a suíte de **conformance** existe para provar que o código do GUEST respeita três leis fundamentais.

### L1 - Pureza da linguagem hospedeira

Python não pode computar pelo GUEST - construções nativas que forneçam semântica computacional ainda não conquistada são proibidas dentro do código do GUEST. Exemplos incluem:

- `True` e `False`;
- operadores booleanos nativos;
- condicionais e loops nativos;
- operadores aritméticos nativos;
- comparações nativas;
- builtins ou APIs que realizem computação pelo GUEST;
- acesso à representação interna de objetos para contornar componentes derivados.

A lei é estável. O conjunto de formas capazes de violá-la pode crescer conforme novos cheats sejam identificados.

### L2 - Dependência causal

Uma unidade do GUEST só pode depender de unidades do GUEST que pertençam estritamente ao seu passado causal:

```
A -> B somente se position(B) < position(A)
```

Posições ausentes, inválidas ou ambíguas também violam essa lei porque impedem que a relação causal seja determinada.

### L3 - Fronteira com o HOST

A única passagem privilegiada do GUEST para fora do próprio GUEST é a superfície pública da Trusted Base:

```
GUEST -> passado causal do GUEST  (permitido)
GUEST -> src.host.trusted_base    (permitido)

GUEST -> outros módulos do HOST  (proibido)
GUEST -> stdlib                  (proibido)
GUEST -> dependências externas   (proibido)
```

O acesso à Trusted Base deve ocorrer pela sua superfície pública, não por módulos internos. Essas três leis definem o contrato fundamental do código do GUEST.

## 7. Método de evolução do GUEST

Zero não deve reproduzir automaticamente uma arquitetura conhecida apenas porque sabemos antecipadamente como computadores tradicionais costumam ser construídos. O método se aplica às **capacidades computacionais do GUEST**. A estrutura do projeto, do HOST e dos testes pode ser desenhada preventivamente quando isso materializa boundaries e invariantes já conhecidas.

### 7.1. Problema antes da abstração

Uma nova abstração computacional só deve surgir depois que existir um problema concreto que a exija. Não devemos criar antecipadamente `Wire`, `Signal`, `Circuit`, `Clock`, `Register`, `Memory` ou qualquer outra capacidade apenas porque imaginamos que serão úteis. Primeiro aparece o problema; depois procuramos a menor abstração capaz de resolvê-lo. A arquitetura conhecida pode informar uma decisão, mas não substituir a descoberta do problema que justifica essa decisão.

### 7.2. Repetição antes da generalização

Nem toda repetição deve ser eliminada imediatamente. Antes de criar algo como:

```python
Adder(width=16)
```

pode ser pedagogicamente melhor repetir explicitamente a estrutura, observar o que se repete, identificar o que varia e somente então introduzir a abstração correta. Conveniência computacional deve ser conquistada depois que a complexidade que ela esconde estiver compreendida.

### 7.3. Menor próximo passo

Ao evoluir o GUEST:

1. observe o estado real do codebase;
2. identifique o menor problema que impede o próximo avanço;
3. determine se o problema pertence ao HOST ou ao GUEST;
4. se pertencer ao GUEST, identifique de quais capacidades anteriores ele pode derivar;
5. implemente apenas o necessário para resolver esse problema;
6. preserve a ordem causal e as leis de conformance.

O filesystem do GUEST deve funcionar como registro arqueológico do nascimento da máquina: ele deve refletir capacidades que já nasceram, não um scaffold antecipado de possibilidades futuras.

## 8. Testes como provas executáveis

Os testes do Zero possuem duas responsabilidades diferentes.

### Testes unitários

Provam comportamento e invariantes locais. Exemplos:

- `Bit` aceita apenas seu domínio válido;
- `NAND` satisfaz sua truth table;
- um gate derivado produz o comportamento esperado.

Os testes unitários devem acompanhar a estrutura do código que testam.

### Testes de conformance

Provam propriedades globais da construção:

- Python não computa pelo GUEST;
- dependências do GUEST respeitam a ordem causal;
- a única passagem privilegiada para o HOST é a Trusted Base.

Assim, os unit tests provam o que o componente faz; os conformance tests provam que ele foi construído legitimamente. Zero exige ambas as dimensões.

## 9. Convenções estruturais permanentes

O codebase materializa as fronteiras conceituais do projeto:

```
src/guest/
    capacidades computacionais derivadas

src/host/
    infraestrutura hospedeira

src/host/trusted_base/
    implementação da Trusted Base

tests/unit/
    provas de comportamento e invariantes locais

tests/conformance/
    provas globais das leis do GUEST
```

A superfície pública da Trusted Base é `src.host.trusted_base` - módulos internos da implementação da Trusted Base não fazem parte da superfície concedida ao GUEST. Imports do GUEST devem ser absolutos e explícitos. Um módulo do GUEST pode importar apenas:

- componentes pertencentes ao seu passado causal;
- símbolos expostos pela superfície pública da Trusted Base.

Essas convenções existem para tornar as fronteiras do Zero verificáveis pelo próprio codebase.

## 10. Critério permanente de decisão

Ao introduzir uma nova capacidade relacionada ao GUEST, responda:

1. Qual problema concreto exige essa capacidade?
2. Ela pertence ao HOST ou ao GUEST?
3. Ela possui semântica computacional?
4. Se pertence ao GUEST, de quais capacidades anteriores deriva?
5. Sua posição e suas dependências são causalmente válidas?
6. Python está apenas descrevendo a estrutura ou resolvendo a computação?
7. Existe uma solução menor que preserve os mesmos princípios?
8. Estamos compreendendo por que essa abstração existe ou apenas reproduzindo uma solução conhecida?

A pergunta permanente é:

> Esta capacidade realmente existe no universo Zero, ou estamos deixando a máquina hospedeira fazê-la por nós?

Se a resposta for a segunda, a implementação deve ser reconsiderada.

## 11. Definição resumida

**Zero é um computador construído progressivamente a partir de uma Trusted Base mínima de `Bit` e `NAND`, em que toda capacidade computacional do GUEST precisa demonstrar como emerge das anteriores, enquanto o HOST fornece somente a infraestrutura necessária para construir, simular e observar essa evolução, e uma suíte de conformance prova que o GUEST usa apenas seu passado causal e a superfície axiomática explicitamente concedida.**

O sucesso do projeto não é apenas chegar a um programa complexo. É chegar até ele sem perder a capacidade de apontar para cada abstração intermediária e explicar:

> **Foi assim que isso passou a existir.**

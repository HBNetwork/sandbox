# ASDF

Muitas vezes quando focamos no design do código começando pela BOSTA do banco de dados, a gente acaba criando metacolunas que espalham um dado em várias.

Exemplo:
1. Dinheiro costuma ser representado com DecimalField para o valor e um CharField para a moeda.
2. Um documento de identidade costuma ser representado por um CharField para o valor e um CharField para o tipo do documento.

```python
IdentificationTypes = (
    ("BrCpf", "Cpf"),
    ("BrRg", "Rg")
)

class Customer(models.Model):
    identification_value = models.CharField(...)
    identification_type = models.CharField(choices=IdentificationTypes)
```

## Qual o sintoma?

Para suportar múltiplos tipos, nosso código terá UMA PORRADA de IFS em várias partes:
- Na view
- No serializer
- Nas queries ao banco
- Nas validações
- Etc, etc, etc.

Precisamos ter em mente que Ifs são maléficos e devem ser expurgados para fora do sistema.

## Qual a doença?

A doença é o design focado no DADO e não na Semântica do que o dado representa.
Essa doença ataca os códigos multiplando Ifs.

## Qual o tratamento?

Temos 3 tratamentos possíveis:
1. Encurtar ao máximo o branch. Exemplos disso é o uso do early return.
2. Uso de polimorfismo para especializar os Ifs no comportamento de tipos análogos.
3. Expulsar o if para a camada mais externa do programa. Exemplos: Em vez de eu detectar as coisas com ifs, eu passo a exigir que o chamador defina explicitamente o que deseja.

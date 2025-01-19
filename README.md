# QuotexBot

QuotexBot é um bot automatizado em Python para interação com a plataforma de negociações Quotex. Ele foi projetado para facilitar o processo de negociação e realizar operações com base em análises técnicas, como RSI (Indicador de Força Relativa), MACD (Média Móvel de Convergência e Divergência) e níveis de suporte e resistência.

## Funcionalidades

- **Login e autenticação:** Realiza login na plataforma Quotex e gerencia o token de sessão.
- **Consulta de saldo:** Exibe o saldo atual da conta.
- **Consulta de detalhes da conta:** Exibe informações detalhadas sobre a conta do usuário.
- **Negociações automáticas:** Realiza negociações com base em condições predefinidas.
- **Consulta de ativos:** Recupera a lista de ativos disponíveis para negociação.
- **Indicadores técnicos:** Calcula indicadores RSI e MACD, e identifica níveis de suporte e resistência.

## Requisitos

- **Python:** Versão 3.7 ou superior
- **Dependências:**
  - `numpy`
  - `TA-Lib`
  - `quotexapi`

Para instalar as dependências, execute:

```bash
pip install numpy TA-Lib quotexapi
```

## Uso

### Configurações de Login

Edite as variáveis `EMAIL` e `PASSWORD` no código principal com suas credenciais do Quotex:

```python
EMAIL = "seu_email@example.com"
PASSWORD = "sua_senha"
```

### Executando o Bot

1. Certifique-se de que todas as dependências estejam instaladas.
2. Execute o arquivo principal:

```bash
python nome_do_arquivo.py
```

O bot irá realizar as seguintes operações:

- Conectar à plataforma Quotex.
- Obter os últimos candles para realizar análises.
- Calcular os indicadores RSI e MACD.
- Detectar níveis de suporte e resistência.
- Realizar negociações com base nas condições analisadas.
- Desconectar após concluir as operações.

### Exemplo de Execução

1. **Análise e negociação:**
   O bot avalia as condições de mercado utilizando RSI, MACD e os níveis de suporte e resistência para determinar se deve realizar uma operação de compra (CALL) ou venda (PUT).

2. **Saída esperada:**

   - Detalhes sobre o saldo atual.
   - Informativos sobre as negociações realizadas.
   - Resumo dos ativos analisados.

## Funções Principais

### Classe `QuotexBot`

#### Métodos:

- `conectar()`: Realiza o login na plataforma Quotex.
- `is_token_valid()`: Verifica a validade do token de autenticação.
- `desconectar()`: Encerra a sessão com a plataforma.
- `get_saldo()`: Retorna o saldo atual da conta.
- `get_detalhes_conta()`: Exibe informações detalhadas sobre a conta.
- `realizar_negociacao(ativo, direcao, valor, tempo_expiracao)`: Realiza uma negociação com os parâmetros especificados.
- `obter_lista_ativos()`: Retorna a lista de ativos disponíveis para negociação.
- `obter_detalhes_ativo(ativo)`: Retorna os detalhes de um ativo específico.

### Indicadores Técnicos

- `calcular_indicadores(candles)`: Calcula RSI e MACD com base nos candles fornecidos.
- `detectar_suporte_resistencia(candles)`: Identifica os níveis de suporte e resistência com base nos valores máximos e mínimos dos candles.

## Observação

Este bot foi desenvolvido para fins educacionais e de aprendizado. Certifique-se de compreender os riscos envolvidos em operações financeiras antes de utilizar esta ferramenta.

## Licença

Este projeto está licenciado sob a MIT License. Consulte o arquivo `LICENSE` para mais detalhes.

---

**Autor:** Paulo Maloza  
**Contato:** Paulomaloza@gmail.com


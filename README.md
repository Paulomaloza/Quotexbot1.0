# Quotex Bot Tool

Uma ferramenta automatizada para configuração e execução de bots de negociação na plataforma Quotex. Este script facilita a instalação de dependências, a configuração do ambiente e a execução do bot de maneira simples e direta.

## Recursos
- Verifica se o Python3 e pip estão instalados.
- Clona o repositório do bot a partir de um URL fornecido.
- Instala as dependências do projeto listadas no arquivo `requirements.txt`.
- Inicia o bot automaticamente.

## Pré-requisitos
Antes de executar o script, certifique-se de ter:
- **Python 3.6+** instalado.
- **pip** (gerenciador de pacotes do Python) instalado.
- Acesso ao repositório do bot Quotex.

## Como usar
1. Clone ou baixe este repositório para sua máquina.
2. Torne o script executável:
   ```bash
   chmod +x script.sh
   ```
3. Edite o arquivo `script.sh` substituindo os seguintes placeholders:
   - `<URL_DO_REPOSITORIO>`: Insira o URL do repositório do bot.
   - `<NOME_DO_DIRETORIO>`: Nome do diretório clonado.
   - `<NOME_DO_SCRIPT>`: Nome do arquivo principal do bot (por exemplo, `botquotex.py`).
4. Execute o script:
   ```bash
   ./script.sh
   ```

## Estrutura do Repositório
```
quotex-bot-tool/
├── script.sh         # Script para configurar e executar o bot
├── requirements.txt  # Dependências do projeto
└── README.md         # Documentação do projeto
```

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues com sugestões de melhorias.

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).


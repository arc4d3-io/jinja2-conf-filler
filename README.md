# Processador de templates Jinja2 com variáveis JSON - jinja2-conf-filler

## Descrição

Este script processa templates Jinja2 usando variáveis JSON, podendo executar múltiplos jobs configurados ou uma execução ad hoc de um único template. O resultado do processamento é salvo em arquivos de saída ou exibido no console.

## Requisitos

- Python 3.6+
- Jinja2

## Instalação

1. Clone o repositório:

   ```
   git clone https://github.com/arc4d3-io/jinja2-conf-filler
   ```

2. Crie um ambiente virtual e ative-o:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```
   pip install jinja2
   ```

### Estrutura de Diretórios Padrão

A estrutura de diretórios padrão do script consiste nos seguintes diretórios:

- `templates`: Este diretório armazena os arquivos de template Jinja2 que serão processados. Cada arquivo deve ter a extensão `.j2`.
- `vars`: Este diretório contém arquivos JSON com as variáveis que serão usadas no processamento dos templates. Os arquivos devem ter a extensão `.json`.
- `output`: Este diretório armazena os arquivos de saída gerados após o processamento dos templates. O script criará subdiretórios dentro do diretório `output` conforme especificado nos jobs ou no parâmetro `-o`.
- `jobs`: Este diretório armazena os arquivos os arquivos JSON com as configurações de jobs.

Assegure-se de que os arquivos de template e variáveis estejam nos diretórios corretos antes de executar o script. Caso deseje utilizar uma estrutura de diretórios diferente, você precisará modificar o código do script para refletir os novos caminhos.   

## Uso

1. Coloque os arquivos de template Jinja2 no diretório `templates`.
2. Coloque os arquivos JSON com as variáveis no diretório `vars`.
3. Configure os jobs no arquivo `sample-job.json`, seguindo o exemplo abaixo:

   ```json
   {
       "jobs": [
           {
               "job_name": "exemplo",
               "output_dir": "output_exemplo",
               "steps": [
                   {
                       "template": "template1.j2",
                       "output": "output1.txt"
                   },
                   {
                       "template": "template2.j2",
                       "output": "output2.txt"
                   }
               ]
           }
       ]
   }
   ```

6. Execute o script com os parâmetros desejados:

   ```
   python processador_templates.py -j jobs/sample-job.json
   ```

### Parâmetros

- `-j, --jobs`: Caminho para o arquivo JSON com as configurações dos jobs (exemplo: jobs.json).
- `-t, --template`: Nome do arquivo de template Jinja2 para uma execução ad hoc (exemplo: template.j2).
- `-c, --console`: Imprimir o resultado no console em vez de salvar em um arquivo.
- `-o, --output`: Nome do arquivo de saída para a execução ad hoc (exemplo: output.txt). Se não for especificado, o resultado será impresso no console.

## Exemplos

- Executar jobs configurados no arquivo `sample-job.json`:

  ```
  python processador_templates.py -j jobs/sample-jobs.json
  ```

- Processar um único template `template.j2` e salvar o resultado no arquivo `output.txt`:

  ```
  python processador_templates.py -t template.j2 -o output.txt
  ```

- Processar um único template `template.j2` e exibir o resultado no console:

  ```
  python processador_templates.py -t template.j2 -c
  ```

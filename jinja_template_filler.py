import argparse
import json
import os
import ipaddress
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

def is_list(value):
    return isinstance(value, list)

def exclude_elements(base_array, exclude_array):
    new_array = base_array[:]
    for elem in exclude_array:
        while elem in new_array:
            new_array.remove(elem)
    return new_array

def carregar_json_arquivo(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f'Erro na decodificação do JSON: {e}')
        exit(1)
    except FileNotFoundError:
        print(f'Arquivo {caminho} não encontrado.')

def carregar_json_diretorio(caminho):
    data = {}
    if os.path.isdir(caminho):
        for arquivo in os.listdir(caminho):
            if arquivo.endswith('.json'):
                arquivo_json = os.path.join(caminho, arquivo)
                data.update(carregar_json_arquivo(arquivo_json))
    return data

def carregar_json(caminho):
    if os.path.isdir(caminho):
        return carregar_json_diretorio(caminho)
    elif os.path.isfile(caminho):
        return carregar_json_arquivo(caminho)
    else:
        print(f'{caminho} não é um diretório nem um arquivo válido.')
        return {}

def processar_template(nome_template, variaveis, diretorio_template):
    env = Environment(loader=FileSystemLoader(diretorio_template))
    env.globals.update(ipaddress=ipaddress)
    env.filters['exclude'] = exclude_elements
    env.filters['is_list'] = is_list
   
    try:
        template = env.get_template(nome_template)
    except TemplateNotFound:
        print(f'O arquivo de template {nome_template} não foi encontrado no diretório {diretorio_template}.')
        exit(1)

    output = template.render(variaveis)
    return output

def executar_jobs(caminho_jobs, diretorio_vars, diretorio_template, diretorio_output):
    configuracao = carregar_json(caminho_jobs)
    variaveis = carregar_json(diretorio_vars)
    jobs = configuracao.get('jobs', [])

    for job in jobs:
        print(f'Executando job: {job["job_name"]}')
        output_dir = f"{diretorio_output}/{job['output_dir']}"        
        os.makedirs(output_dir, exist_ok=True)

        for step in job['steps']:
            nome_template = step["template"]
            print(f'  Processando template: {nome_template}')         
            resultado = processar_template(nome_template, variaveis, diretorio_template)
            output_file = os.path.join(output_dir, step['output'])
            
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(resultado)
            print(f'  Arquivo gerado: {output_file}')

def main():
    parser = argparse.ArgumentParser(description='Processar arquivos de template Jinja2 com variáveis JSON e executar jobs.')
    group = parser.add_mutually_exclusive_group(required=True)
    output_option = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-j', '--jobs', help='Caminho para o arquivo JSON com as configurações dos jobs (exemplo: jobs.json).')
    group.add_argument('-t', '--template', help='Nome do arquivo de template Jinja2 para uma execução ad hoc (exemplo: template.j2).')
    output_option.add_argument('-c', '--console', action='store_true', help='Imprimir o resultado no console em vez de salvar em um arquivo.')
    output_option.add_argument('-o', '--output', help='Nome do arquivo de saída para a execução ad hoc (exemplo: output.txt). Se não for especificado, o resultado será impresso no console.')
    args = parser.parse_args()

    diretorio_vars = 'vars'
    diretorio_template = 'templates'
    diretorio_output = 'output'

    if args.jobs:
        print('Processando o arquivo de jobs...')         
        executar_jobs(args.jobs, diretorio_vars, diretorio_template, diretorio_output)
    elif args.template:
        print('Processando o template...') 
        nome_template = args.template
        variaveis = carregar_json(diretorio_vars)
        resultado = processar_template(nome_template, variaveis, diretorio_template)

        if args.console:
            print('\nResultado:')
            print(resultado)
        else:    
            os.makedirs(diretorio_output, exist_ok=True)
            output_file = os.path.join(diretorio_output, args.output)
            try:
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    outfile.write(resultado)
                print(f'Template processado com sucesso. Verifique o arquivo {output_file}.')
            except IOError:
                print(f'Erro ao escrever no arquivo de saída {output_file}.')

if __name__ == '__main__':
    main()

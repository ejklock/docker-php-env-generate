import yaml
import os
import subprocess
import shutil

dockerComposeDir = 'docker-compose'
nginxConfDir = f'{dockerComposeDir}/nginx'
phpConfDir = f'{dockerComposeDir}/php-fpm'
mysqlDir = f'{dockerComposeDir}/mysql'

appName = input("Informe o nome da aplicação (app): ").replace(" ","-").lower() or 'app'
phpversion = input("Informe a imagem docker do php-fpm que deseja usar: ")
gitRepoUrl = input("Informe a url do repositorio git (opcional): ") or ''

dockerComposeFile = 'docker-compose.yml'
envFile = '.env'

data = {
    'version': '3.7',
    'services': {
        'app': {
            'container_name': f'{appName}-app-dev',
            'environment': [
                'COMPOSER_MEMORY_LIMIT=-1'
            ],
            'image': f'{phpversion}',
            'networks': [
                f'{appName}Network'
            ],
            'restart': 'unless-stopped',
            'volumes': [
                './:/var/www/app',
                './docker-compose/php-fpm/custom.ini:/usr/local/etc/php/conf.d/custom.ini',
            ],
            'working_dir': '/var/www/app'
        },
        'db': {
            'command': '--default-authentication-plugin=mysql_native_password',
            'container_name': f'{appName}-dev-db',
            'environment': {
                'MYSQL_DATABASE': f'{appName}',
                'MYSQL_PASSWORD':  f'{appName}',
                'MYSQL_ROOT_PASSWORD':  f'{appName}',
                'MYSQL_USER':  f'{appName}',
                'SERVICE_NAME': 'mysql',
                'SERVICE_TAGS': 'dev'
            },
            'image': 'mysql:5.7',
            'networks': [f'{appName}Network'],
            'ports': ['33306:3306'],
            'restart': 'unless-stopped',
            'tty': True,
            'volumes': [
                './docker-compose/mysql:/docker-entrypoint-initdb.d',
                f'{appName}MysqlData:/var/lib/mysql'
            ]
        },
        'nginx': {
            'container_name': f'{appName}-dev-nginx',
            'image': 'nginx:alpine',
            'networks': [f'{appName}Network'],
            'ports': ['8000:80'],
            'restart': 'unless-stopped',
            'volumes': [
                './:/var/www/app',
                './docker-compose/nginx:/etc/nginx/conf.d/'
            ],
            'working_dir': '/var/www/app'
        }
    },
    'networks': {
        f'{appName}Network': {
            'driver': 'bridge'
        },
    },
    'volumes': {
        f'{appName}MysqlData': {
            'driver': 'local',
            'name': f'{appName}MysqlData'
        }
    }
}

def generateFileWithPath(path, content, lines=False, isYaml=False):
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, 'w') as f:
        if not isYaml:
            if lines:
                f.writelines(content)
            else:
                f.write(content)
        else:
            yaml.dump(content, f, default_flow_style=False, sort_keys=False)

def clone_repository(url, path):
    print(f'Clonando repositório {url} para {path}\n')
    try:
        process = subprocess.Popen(['git', 'clone', url, path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        
        for line in process.stdout:
            print(line, end='')
        
        for line in process.stderr:
            print(line, end='')
        
        process.wait()
        
        if process.returncode != 0:
            print(f'\nErro ao clonar repositório. Código de saída: {process.returncode}')
            return False
        else:
            print(f'\nRepositório clonado com sucesso.')
            return True
    except Exception as e:
        print(f'\nErro ao clonar repositório: {e}')
        return False

# Criar a pasta do app
os.makedirs(appName, exist_ok=True)
os.chdir(appName)

print('Gerando arquivo docker-compose.yml\n')
generateFileWithPath(dockerComposeFile, data, False, True)

print('Criando app.conf do nginx\n')
generateFileWithPath(f'{nginxConfDir}/app.conf', """server {
    listen 80;
    client_max_body_size 0;
    index index.php index.html;
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;
    root /var/www/app/public;
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass app:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_buffers 16 16k; 
        fastcgi_buffer_size 32k;
    }
    location / {
        try_files $uri $uri/ /index.php?$query_string;
        gzip_static on;
    }
}""")

print('Criando config do php\n')
generateFileWithPath(f'{phpConfDir}/custom.ini', """memory_limit = 4096M
upload_max_filesize = 500m
max_execution_time = 5600
post_max_size = 500M
""")

generateFileWithPath(f'{mysqlDir}/.gitignore', """*.sql""")

# Clonar o repositório Git, se fornecido
if gitRepoUrl:
    print("Clonando repositório Git...")
    temp_dir = 'temp_git_clone'
    if clone_repository(gitRepoUrl, temp_dir):
        # Mover conteúdo do repositório para a raiz do projeto
        for item in os.listdir(temp_dir):
            s = os.path.join(temp_dir, item)
            d = os.path.join('.', item)
            if os.path.isdir(s):
                shutil.move(s, d)
            else:
                shutil.copy2(s, d)
        shutil.rmtree(temp_dir)
        print("Conteúdo do repositório Git movido para a pasta do projeto.")
    else:
        print("Falha ao clonar o repositório. A estrutura Docker foi criada sem o conteúdo do Git.")
else:
    print("Nenhum repositório Git fornecido. Estrutura Docker criada sem conteúdo do Git.")

print(f'\nSeu ambiente PHP foi criado com sucesso na pasta {appName}. A estrutura Docker LAMP está pronta para uso.\n')
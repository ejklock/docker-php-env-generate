
import yaml
import os

dockerComposeDir = f'docker-compose'
nginxConfDir = f'{dockerComposeDir}/nginx'
phpConfDir = f'{dockerComposeDir}/php-fpm'
mysqlDir = f'{dockerComposeDir}/mysql'

appName= input("Informe o nome da aplicação (app): ").replace(" ","-").lower() or 'app'
phpversion = input("Informe a imagem docker do php-fpm que deseja usar: ")
gitRepoUrl = input("Informe a url do repositorio git : ")

dockerComposeFile=f'{appName}/docker-compose.yml'
envFile = f'{appName}/.env'

data = {
    'version': '3.7',
    'services': {
        'app': 
            {
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
                    './app:/var/www/app',
                    './.docker-compose/php-fpm/custom.ini:/usr/local/etc/php/conf.d/custom.ini',
                    './.docker-compose/php-fpm/xdebug.ini:/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini'
                ],
                'working_dir': '/var/www/app'
            },
            'db': 
                {
                    'command': '--default-authentication-plugin=mysql_native_password',
                    'container_name': f'{appName}-dev-db',
                    'environment': {
                        'MYSQL_DATABASE': '${DB_DATABASE}',
                        'MYSQL_PASSWORD': '${DB_PASSWORD}',
                        'MYSQL_ROOT_PASSWORD': '${DB_PASSWORD}',
                        'MYSQL_USER': '${DB_USERNAME}',
                        'SERVICE_NAME': 'mysql',
                        'SERVICE_TAGS': 'dev'
                        },
                     'image': 'mysql:5.7',
                     'networks': [f'{appName}Network'],
                     'ports': ['${DB_EXTERNAL_PORT}:${DB_PORT}'],
                     'restart': 'unless-stopped',
                     'tty': True,
                     'volumes': [
                         './.docker-compose/mysql:/docker-entrypoint-initdb.d',
                         f'{appName}MysqlData:/var/lib/mysql'
                         ]
                },
              'nginx': 
                {
                    'container_name': f'{appName}-dev-nginx',
                    'image': 'nginx:alpine',
                    'networks': [f'{appName}Network'],
                    'ports': ['8000:80'],
                    'restart': 'unless-stopped',
                    'volumes': [
                        './app:/var/www/app',
                        './.docker-compose/nginx:/etc/nginx/conf.d/'
                    ],
                    'working_dir': '/var/www/app'
                }
            },
    'networks':{
        f'{appName}Network':{
            'driver':'bridge'
        },
       
    },
    'volumes': {
        f'{appName}MysqlData': {
            'driver': 'local',
            'name': f'{appName}MysqlData'
        }
    }}
    
def generateFileWithPath(path,content,lines=False,isYaml=False):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path, 'w') as f:
        if not(isYaml):
            if lines:
                f.writelines(content)
            else:
                f.write(content)
        else:
            yaml.dump(content, f, default_flow_style=False, sort_keys=False)


print('Gerando arquivo docker.compose.yml\n')

generateFileWithPath(dockerComposeFile,data,False,True)

print('Gerando arquivo .env\n')

generateFileWithPath(envFile,[
        "DB_HOST=db\n", 
        "DB_PORT=3306\n",
        "DB_EXTERNAL_PORT=33306\n",
        f"DB_DATABASE={appName}\n",
        f"DB_USERNAME={appName}\n",
        f'DB_PASSWORD={appName}\n',
        'DB_TIMEZONE=+00:00',
        ],True)

print('Criando app.conf do nginx\n')

generateFileWithPath(f'{appName}/{nginxConfDir}/app.conf',"""server{
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
    }
    location / {
        try_files $uri $uri/ /index.php?$query_string;
        gzip_static on;
    }
}""")


print('Criando config do php\n')

generateFileWithPath(f'{appName}/{phpConfDir}/custom.ini',"""memory_limit = 4096M
upload_max_filesize = 500m
max_execution_time = 5600
post_max_size = 500M
""")

print(f'Clonando repositório {gitRepoUrl}\n')

os.system(f"git clone {gitRepoUrl} {appName}/app")

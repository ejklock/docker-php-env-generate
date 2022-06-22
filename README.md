# Gerador de Ambiente Docker com Docker Compose para Aplicações PHP

### 1. Baixar o Executavel da solução acordo com sua plataforma

* Windows <https://github.com/ejklock/docker-lamp-template-generate/suites/5962362674/artifacts/204842095>
* Linux <https://github.com/ejklock/docker-lamp-template-generate/suites/5962362674/artifacts/204842094>

### 2. Extrair e copiar o exectavel para sua pasta de projetos e executar via terminal (cmd, powershell e variantes)

* ### Linux
  ```
   sudo chmod 777 docker-dev-lamp-env
  ```
  ```
   ./docker-dev-lamp-env
  ```

* ### Windows
  
  ```
   docker-dev-lamp-env
  ```
  ### 3. Infomar as entradas exigidas pelo prompt e a url do repositorio (.git no fim da url)
  
  1. Nome e  Imagem do dockerhub do php-fpm


     O autor do projeto disponibiliza  [algumas imagens com as mais diferentes versões do php](https://registry.hub.docker.com/r/ejklock/php-fpm/tags), incluido composer e varias extensões do php por padrão (5.6, 7.3 e 7.4) bastando apenas especificar a versão desejada (ex: ejklock/php-fpm:7.3 ou ejklock/php-fpm:7.4)
  
   ![image](https://user-images.githubusercontent.com/8179907/175052410-a5dd25cd-794f-4f0e-8ee9-f4a05f3cca4c.png)
 
 2. Url do repositório git do projeto (necessária chave .ssh configurada)

   ![image](https://user-images.githubusercontent.com/8179907/175055257-98c9d78d-f71c-4451-8053-e1bf43b887ce.png)


### 4. Estrutura da gerada

O script gerará um boilerplate para a aplicação pronta para rodar.

![image](https://user-images.githubusercontent.com/8179907/175055670-9a8d7832-49c9-48a8-902a-545a949b5544.png)

 1. Pasta app
    
    Nessa pasta fica o codigo clonado da aplicação. É aqui vocẽ irá trabalar
 
 2. Pasta docker-compose
    
    Nessa pasta ficam alguns arquivos configuraveis da estrutura em geral
    
    1. Pasta mysql
       
       Nessa pasta você (antes de levantar o container da aplicação pela primeira vez) pode colocar o script do banco para que o container restaure um banco ja existente no seu banco de desenvolvimento. Basta apagar esse arquivo exemplo ou adicionar conteúdo nele
       
    2 . Pasta nginx
      
      Nessa pasta ficam as configurações sobre o web server nginx. Para mais detalhes sobre o arquivo de configuração acesse <https://www.nginx.com/>
      
    3 . Pasta php-fpm
      
      Nessa pasta fica um arquivo custom.ini que é onde podemos colocar as configurações do php que serão sobrescritas (php.ini)
      
 4. Pasta raiz do boilerplate gerado
  
    Na pasta raiz você encontrará 2 arquivos:
   
    1. ".env"
      
      O arquivo ".env" do boilerplate você controla algumas variaveis de ambiente como usuario do banco, senha, porta  etc
      
    2. docker-compose.yml

      Esse é o arquivo de configuração do docker-compose onde são descritos os serviços e configurações a serem levantados pelo docker. Mais informações consultar a documentação do docker-compose <https://docs.docker.com/compose/>   

### 4. Rodando o projeto

Para rodar o projeto basta, na raiz do boilerplate gerado (fora da pasta app) rodar:

```
docker-compose up
```
### 5. Rodando comandos dentro dos containeres

O docker permite você executar comandos dentro dos containeres para fazer algumas ações. 

```
docker-compose exec <nome_do_servico_no_arquivo_docker-compose.yml> <seu_comando>
```

1. Rodar o composer install no serviço app:

```
docker-compose exec app composer install
```

2. Rodar um comando do php/laravel no serviço app:
```
docker-compose exec app php artisan
```

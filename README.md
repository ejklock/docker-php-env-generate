 Docker Environment Generator with Docker Compose for PHP Applications

## Description:

This repository provides a Docker environment generator powered by Docker Compose specifically tailored for PHP applications. Whether you're working on a small project or a large-scale application, setting up your development environment can be time-consuming. With this tool, you can quickly generate a boilerplate environment configured with Docker Compose, allowing you to focus on coding rather than environment setup.

### Features:
- **Platform Support:** Works seamlessly on Windows and Linux platforms.
- **Easy Setup:** Download the executable, provide necessary inputs, and let the tool do the rest.
- **Flexible Configuration:** Choose the PHP-FPM version and customize your environment based on your project's requirements.
- **Pre-configured Services:** Includes MySQL and Nginx configurations to kickstart your development process.
- **Command Line Interface:** Interact with the tool via command line, making it convenient for developers.

### How to Use:
1. Download the executable for your platform from the provided links.
2. Extract and execute the executable in your project folder.
3. Follow the prompts to input necessary information, such as PHP-FPM version and Git repository URL.
4. Once generated, you'll have a ready-to-use Docker environment for your PHP application.
5. Use `docker-compose up` command to run the project, and execute additional commands inside containers using `docker-compose exec`.

## Steps

### 1. Download the Executable for the solution according to your platform

* Windows [Download here](https://github.com/ejklock/docker-lamp-template-generate/suites/5962362674/artifacts/204842095)
* Linux [Download here](https://github.com/ejklock/docker-lamp-template-generate/suites/5962362674/artifacts/204842094)

### 2. Extract and copy the executable to your project folder and execute it via terminal (cmd, powershell, and variants)

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
  ### 3. Provide the required inputs through the prompt and the repository URL (.git at the end of the URL)
  
  1. Name and DockerHub image of php-fpm


     The project author provides [several images with different PHP versions](https://registry.hub.docker.com/r/ejklock/php-fpm/tags), including Composer and various PHP extensions by default (5.6, 7.3, and 7.4), you just need to specify the desired version (e.g., ejklock/php-fpm:7.3 or ejklock/php-fpm:7.4).
  
   ![image](https://user-images.githubusercontent.com/8179907/175052410-a5dd25cd-794f-4f0e-8ee9-f4a05f3cca4c.png)
 
 2. Git repository URL of the project (SSH key configuration required)

   ![image](https://user-images.githubusercontent.com/8179907/175055257-98c9d78d-f71c-4451-8053-e1bf43b887ce.png)


### 4. Generated structure

The script will generate a boilerplate for the application ready to run.

![image](https://user-images.githubusercontent.com/8179907/175055670-9a8d7832-49c9-48a8-902a-545a949b5544.png)

 1. App folder
    
    This folder contains the cloned code of the application. This is where you will work.
 
 2. Docker-compose folder
    
    This folder contains some configurable files of the structure in general
    
    1. MySQL folder
       
       In this folder, you (before bringing up the application container for the first time) can place the database script so that the container restores an existing database in your development environment. Just delete this example file or add content to it.
       
    2 . Nginx folder
      
      This folder contains configurations for the Nginx web server. For more details on the configuration file, visit <https://www.nginx.com/>.
      
    3 . PHP-FPM folder
      
      This folder contains a custom.ini file where we can put PHP configurations that will be overridden (php.ini).
      
 4. Root folder of the generated boilerplate
  
    In the root folder, you will find 2 files:
   
    1. ".env"
      
      The ".env" file of the boilerplate controls some environment variables such as database user, password, port, etc.
      
    2. docker-compose.yml

      This is the docker-compose configuration file where the services and configurations to be brought up by Docker are described. For more information, consult the Docker Compose documentation <https://docs.docker.com/compose/>.   

### 4. Running the project

To run the project, simply, in the root of the generated boilerplate (outside the app folder), run:

```
docker-compose up
```
### 5. Running commands inside containers

Docker allows you to execute commands inside containers to perform some actions.

```
docker-compose exec <service_name_in_docker-compose.yml_file> <your_command>
```

1. Run composer install on the app service:

```
docker-compose exec app composer install
```

2. Run a PHP/Laravel command on the app service:
```
docker-compose exec app php artisan
```

### Contribution:
Contributions are welcome! If you have any ideas to improve this tool or encounter any issues, feel free to open an issue or submit a pull request.

### Credits:
This project is maintained by ejklock and is inspired by the need for an efficient Docker environment setup for PHP development.

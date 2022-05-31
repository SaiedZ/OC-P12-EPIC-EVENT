# EpicEvents CRM API

<br>
<span><img src="https://img.shields.io/badge/DJANGO-3.2-brightgreen?style=for-the-badge&logo=django&logoColor=white">   <img src="https://img.shields.io/badge/Python-3.10.0-brightgreen?style=for-the-badge&logo=python&logoColor=white">   <img src="https://img.shields.io/badge/Django Rest Framework-3.13.1-brightgreen?style=for-the-badge&logo=django&logoColor=white">   </span>
<br>
<br>
Training django and DRF project.
Part of Open Classrooms "Python developper", 12th Project.

## :page_with_curl: What's it ?

The EpicEvents CRM API allows users to manage data related to users, clients, contracts and events.

Our API allows users to make CRUD operations if permissions are respected. Permissions are based on the team of the user for some models and on support user or sale user for some other models. They are detailled in the API documentation.

Our API is organized around [REST](http://en.wikipedia.org/wiki/Representational_State_Transfer). It uses standard HTTP response codes, authentication, and verbs.

we have built this API respecting the recommendations of the OWASP top [10 recommandations](https://owasp.org/www-project-top-ten/)

##  📖  API Documentation

[API documentation](https://documenter.getpostman.com/view/19779552/Uz59Me61)


## :mag: Technologies

*   Django Rest Framework as backend
*   Postgresql as database
*   JWT (JSON Web Token) for the backend authentication

## 💿 How to setup the API ?

1. First, you will need to download [the source code](https://github.com/SaiedZ/LITReviewWebApp.git) from GitHub.
2. Unzip the folder
3. Go to the unzipped folder using your terminal
4. You can also clone the repo without dowloading the folder. In this case, don't follow the steps above and just: use these commands (git must be installed):
```bash
git clone https://github.com/SaiedZ/issuestrackingapi.git
cd LITReviewWebApp
```
5. Create your virtual environment with the following command (here I call it .env, but you can call it another way)
```bash
python -m venv .env
```
6. Activate the virtual environment with the following command
 
  * on Unix or Mac :
```shell
 source .env/bin/Activate
```
   * on Windows :
```bash
.env\Scripts\activate.bat
```

7. Move to src folder
```bash
cd src
```

8. Install the packages required to run the tool from the `requirements.txt` file
```bash
pip install -r requirements.txt
```

9. Now y can start the development server


For more information, refer to the python.org documentation :

[Virtual envirement tutorial](https://docs.python.org/3/tutorial/venv.html)


## ⚙️ Launch the development server

First of all, you need to be located in the **src forlder**

To launch the development server locally, just use the `runserver` command from the `manage.py` file:

```
python manage.py runserver
``` 
Of course, you must first ensure that you have activated your virtual environment and that you are in the folder that contains the `manage.py` file.

Once the development server is launched, you can start using the API by following the documentation [API documentation](https://documenter.getpostman.com/view/19779552/UVkqqZyf)

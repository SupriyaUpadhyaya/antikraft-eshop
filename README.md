# **AntiKraft eShop Codebase**
AntiKraft is an eCommerce platform to buy or sell antique art and artifacts across a wide range of categories.

### **Team Members :**

| Student ID | Name |  Email ID |
|----------|:-------------:|------:|
| 244815 | Supriya Upadhyaya | supriya.upadhyaya@st.ovgu.de |
| xxxxxx | Aarathi |   aarathi@st.ovgu.de |
| xxxxxx | Aneesh Sathyan | aneesh.pindalavalappil@st.ovgu.de |

### <br/><br/>**Logo :** 
<img src="static/logo/png/logo-no-background.png" width="150" height="150">    <img src="static/team-logo/codepanda.gif" width="150" height="150">

### <br/><br/>**Technology stack :**
    Python with Flask
    HTML + CSS + Bootstrap
    SQLite 
    Web Server : Gunicorn
    Local directory / Cloud storage manage images

### <br/><br/>**Steps to run the application :**
1. Clone the "antikraft-eshop" repository to local
2. Install the pre-requisites mentioned in requirement.txt using ```pip install```
3. Execute below command from the "antikraft-eshop" directory: ```gunicorn -w 4 'antikraft-app:app'```

### <br/><br/>**Project directory Structure :**
    antiKraft-eshop/
    ├── backend
    │   ├── controller.py
    │   └── model.py
    ├── images
    │   └── dummy.png
    ├── static
    │   └── logo
    ├── templates
    │   ├── homepage
    │   ├── product-page
    │   └── base.html
    ├── tests
    ├── Architecture.png
    ├── LICENSE
    ├── README.md
    ├── antikraft-app.py
    ├── config.py
    ├── requirements.txt
    └── schema.sql

### <br/><br/>**Architecture :**
![](architecture.png)






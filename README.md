# **Visit AntiQKraft eShop : https://antiqkraft.onrender.com/**
AntiKraft is an eCommerce platform to buy or sell antique art and artifacts across a wide range of categories.

Visit AntiQKraft eShop link - https://antiqkraft.onrender.com/

### **Team Members :**

| Student ID | Name |  Email ID |
|----------|:-------------:|------:|
| 244815 | Supriya Upadhyaya | supriya.upadhyaya@st.ovgu.de |
| 244267 | Aarathi Vijayachandran Chettiar Bhagavathi | aarathi.vijayachandran@st.ovgu.de |
| 241215 | Aneesh Sathyan | aneesh.pindalavalappil@st.ovgu.de |

### <br/><br/>**Logo :** 
<figure><img src="static/logo/logo-black.png" width="250" height="250" href="https://antiqkraft.onrender.com/"> <figcaption>eShop Logo</figcaption> </figure>  <figure><img src="static/team-logo/codepanda.gif" width="150" height="150" > <figcaption>Team Logo</figcaption> </figure>

### <br/><br/>**Technology stack :**
    Python with Flask
    HTML + CSS + Bootstrap
    SQLite 
    Web Server : Gunicorn
    Cloud storage for product iamges - Google drive
    Drive link for images :
    https://drive.google.com/drive/folders/1hupeF6m06aloS4jyl9i0QIB4_IJ3hZCM?usp=sharing
    https://drive.google.com/drive/folders/14CMpny02eYL2o-dzBuDDrBk2bxGMCw3I?usp=sharing

### <br/><br/>**Steps to run the application :**
1. Clone the "antikraft-eshop" repository to local
2. Install the pre-requisites libraries and train chat bot by executing build script "antikraft-eshop" directory```./build.sh```
3. Execute below command from the "antikraft-eshop" directory: ```gunicorn -w 4 'antikraft-app:app'```

### **Requirement checklist :**

| Essential | Necessary |  Nice to have |
|----------|-------------|------|
| ✔️ Create account | ✔️ Search for product | ✔️ Award for selling |
| ✔️ Create offers | ✔️ Different category | ✔️ Customer satifcation ratio |
| ✔️ Buy products | ✔️ Different sorting | ✔️ Do not show full seller infomation before buy |
| ✔️ Out of stock message | ✔️ Do not remove old offers from the database | ✔️ Seller should be able to see previous offers |
| ✔️ Allow pictures to be posted in an offers | ✔️ Chat service between sell and user | ✔️ Relevant product recommendations |
| ✔️ Sponsored search | | ✔️ Chat bot|

### <br/><br/>**Architecture :**
<img src="static/readme/Architecture.png">

### <br/><br/>**Figma Layout :**
Figma link - https://www.figma.com/file/lkPSi2MGeSiqm8wvnLN0k6/Complete_UI-(1)?type=design&mode=design&t=noSNdLHnyy0zkFbD-1
<img src="static/readme/homepage.jpeg">

### <br/><br/>**Project directory Structure :**
    antiKraft-eshop/
    ├── backend                  // Business logic and DB CRUD operation
    │   ├── controller.py
    │   └── model.py
    ├── images                   // Product images uploaded by seller, can be moved to cloud storage
    │   └── dummy.png
    ├── static                   // CSS, images and other static content
    │   ├── logo
    │   ├── team-logo
    │   ├── Architecture.drawio
    │   ├── Architecture.png
    │   └── homepage.png
    ├── templates                // UI - htmls
    │   ├── homepage
    │   ├── product-page
    │   └── base.html
    ├── tests                    // Test cases
    │   └── test.py
    ├── LICENSE
    ├── README.md
    ├── antikraft-app.py
    ├── requirements.txt         // Pre-requisites to be installed
    └── schema.sql               // Sqlite database schema





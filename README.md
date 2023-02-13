# SkinMatch Website
## **Live Web application (use Google Chrome for best results):**
http://skinmatch.pythonanywhere.com/ 

## **Description:**
The application was created with a combination of python, javascript, sql, html, and css. 

SQLite was used to construct a relational database with interlinked tables to store user information, product details, user-uploaded pictures, and other critical data for the website’s efficient operation. Throughout the code of the website, queries are used to retrive information from the database using SQL commands.

This website was designed to create a community of makeup lovers to share the actual shade of different products on their skin.

Based on color theory, different product shades will show up differently based on your actual skin tone. The same shade of a blush, bronzer, lipstick, concealer and so on will look completely different on someone who has fair skin as opposed to someone who has a darker complexion. SkinMatch allows users to browse and also upload pictures of different products on their skin.

In addition, if you are someone who has bought makeup online or in a drugstore you know how frustrating it is to try to figure out the true color of a product, based on the over-edited, perfect lightning pictures that official brands post on their website or by just eyeballing the packaging of a product. This website was created for people like you and me to post raw pictures over normal everyday lightning to portrait the true color of products. Helping us save money and time.

In the following, we will go file per file explaining their contents and uses.

### **- skinmatch.db:**
Let's start by mentioning this file, information from the application is stored into this SQL databases.
There are four tables in the database: users, products, shades, saved.

Users: Stores an unique id, username, hash (also known as password), email.

Products: Stores product brand, product name, url of product image, redirect for product page, search name.

Shades: Stores an unique id, product name, images that are uploaded, description written by who uploaded the image, and user_id for whom did the upload.

Saved: Stores img_id coming from the unique id in table shades, user_id for whom saved the image, product name, and description of the saved image.

### **- layout.html:**
This file contains the layout that all pages within this application will follow. It is composed with html, css, and jinja. There are mainly three components to it.

1) The title SkinMatch at the very top of the page was made into a button so that once it is clicked, no matter in what page the user is on, they can go back to the main *index.html* page.

2) There are two different version of the navbar, the non-logged in and the logged in. Users have the option to save pictures into the session only when they are logged in. Therefore the non-logged in version do not have this option to click on.

3) There is a footer that will appear fixed at the very bottom of each page that can also take you back to the homepage if clicked.

### **- helpers.py:**
In this file we defined the error function which will be imported into *app.py* file which contains the main python codes that will empower the whole application.

This error function defines within itself the replace function, which will replace a message with whatever new message we want. And then it will render the new message in the *error.html* page.

The error function is used throughout the application to tell users of errors and give hints to the users so they know what to fix to proceed using the application.

### **- error.html:**
This file contains the same layout as all the other html files and, as previously mentioned, it returns hints (new message) preventing users from moving forward until they fix the issue.

### **- app.py:**
Here we store the main python code ran in the application. The file start of by importing different libraries, configuring flask application and configuring SQL database.

- @app.route("/") Simply renders the **_index.html_** page in which it contains an introduction to the application telling users what this website is for.

- @app.route("/products", methods=["GET","POST"]) This route is used to display products users can look at.
 With the GET method, products will be retrieved from skinmatch.db and these will be loaded into the **_products.html_** page as buttons so that if they are clicked users will be redirected into the respective product's page.
The Post method will gather the product's name/brand the user inputted into the Search bar and based on that it will retrieve products from the database that matches the input and render it into the **_products.html_** page.

- @app.route("/login", methods=["GET","POST"])
The GET method simply renders **_login.html_** which contains a form where the user will input the username and password to login.
The POST method get the information inputted by the user and checks for error, it will first make sure the user inputted a username and a password, if any of those fields are blank it will direct the user to an error page. If fields are not blank, we will check for the username in the users database and check if password matches the inputted, if one of these criterials do not macth then an error will appear. Otherwise, user will be logged in and redirected to **_index.html_** with the logged in navbar.

- @app.route("/register", methods=["GET", "POST"])
The GET method, just like in login, will return a form for the user to register.
The POST method will check for errors such as an empty field, password and confirmation password matching, checking that username has not been taken and it's unique, and that Email has not been enrolled before. If any of these fails an error with its corresponding message will return. Otherwise, a hash will be generated for the password for security reasons and the information inputted will be inserted into the users table in the database and the user will be redirected into **_index.html_** with the logged in navbar.

- @app.route("/logout") This just clears the session and returns the user to **_index.html_** with the non logged in navbar.

- @app.route("/about") This takes the user into **_about.html_** which displays the mission of the website.

- @app.route("/infallibleconcealer", methods=["GET","POST"]) (and the following ones with / followed by the name of the product contain the same code.)
The GET method will go into the shades database and load into the respective product page images that has been submitted by different users.
In the page there is an icon that will show a pop-up form which will allow users to upload any pictures if they desire as long as they are logged in. JavaScript was used here to transform the picture file uploaded by the user into an URL that will be stored into Local Storage, allowing our database to access the URL and the picture every time page is loaded. I added a checkbox for the user to confirm submission and once it is checked the newly created url will populate a hidden input field that will be inserted along with other information into the shades table in the database using the POST method. Now every image uploaded with the respective product will upload into the page.

- @app.route("/saved", methods=["GET","POST"])
The save feature is only available for users that are logged in. Therefore firstly, the code will check if user is logged in, if not, user will be prompted with an error message asking to register or login.
If user is logged in, the GET method will obtain the user id and load from table saved in the database all saved images corresponding to session user id into **_saved.html_** page.
With the POST method, there is a button to save an image under each image in each product page. Once clicked it will populate a hidden form with information about the selected image and user's id. Then python code will insert it into the saved table in the database. This way every time the user visits "Saved" only saved images corresponding to his/her id will appear.

- @app.route("/delete_saved", methods=['POST'])
In **_saved.html_** there is a button to remove from saved image. Once clicked, it will populate a hidden form with the id of the image and user_id and it will delete from the database the rows corresponding to that information. Removing the saved image in the saved list.

### **- Static Folder:**
This folder contains the web application's css in **_styles.css_**. This website was made with a combination of my own css and Bootstrap features as well.
To avoid any copyright problems all pictures in this website were taken and edited by myself all of these located in the image folder within static folder.

### **- Design Choices:**
One of the design choices that I debated the most was the expansion effect of the shade images updoaded by users. I wanted to make the image expand in a pop-up area rather than expanding on hover, I believe that it would look nicer and have a more friendly user experience.
I attempted doing this by adding an onclick JavaScript function to each shade image being iterated. But because Jinja was using a for loop to add the shade images into the page, the button was working only for the last image iterated. I made many attempts to solved this without success, hence, I opted to expand the image on hover.

Given that I am still new at coding and computer science, and this is my first website, I believe there are still a lot of improvements that can be done to this application, I hope that as I gain more knowledge I can keep perfecting this application.

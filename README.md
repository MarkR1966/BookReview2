# Flask Book List

##### Resources

* Trello: https://trello.com/b/nqWxQLs7/book-review-website
* Website: http://35.214.107.12

#### Contents
* Brief
* Functionality
* Data
* Technologies
* CI Pipeline
* Testing
* Design
* Risk Assessment
* Current Issues
* Future Improvements

#### Brief

To create a CRUD application with utilisation of supporting tools,
methodologies and technologies that encapsulate all core modules
covered during training.

Basically create an application that will take input from a user
and allow them to Create, Read, Update or Delete data stored in a
database based on the input.

##### Minimum requirements
* Project tracking via Trello or other similar application
* A Relational database with at least 2 tables that are joined in a relationship
* Documentation
* A functional CRUD application in Python following best practice
and meeting project management requirements
* Test Suites
* Functioning front end website using Flask
* Code fully integrated into a Version Control System using the
Feature-Branch model which will subsequently be built through a CI
server and deployed to a cloud-based virtual machine.

#### Functionality

I created a Book List application to meet the requirements set.  This
allows to users to view a list of books, add a new book to the list,
update details of an existing book and delete a book from the list.

The user stories that satisfied the brief were
* As a user I want to ba able to add a book - Create
* As a user I want to be able to see a list of books - Read
* As a user I wanto to be able to amend a book entry - Update
* As a user I want to be able to delete a book from the list - Delete

#### Data

#### Technologies
* Trello for project management
* GCP SQL Server using mySQL
* Python for application programming
* Flask for website
* Github for VCS
* Jenkins for CI
* NGINX to run the application
* Systemd to run the application as a service

#### CI Pipeline

CI Pipeline flow goes as as follows
* Source code is created - this is where the application is developed locally
* When working changes have been made to the code this is pushed 
to the repository on Github
* After each code push to Github we check on Trello for the next requirement
* This continues until we have the basic requirements completed
* Jenkins is running an automatic task to check for changes on Github
* when a new build is detected this is uploaded and processed onto the
GCP VM for deployment to end users

#### Testing

#### Design
The front end design is very simple and purely operational

#### Risk Assessment

#### Difficulties
* Using the project management software for the first time
(time to learn how to use)
* Stripping back the initial idea to avoid being more complex than required
* Not enough coding knowledge to produce 'blue sky' application
#### Current Issues
* No searching functionality
* limited functionality
#### Future Improvements
* Adding review scores and read status for each use
* displaying average review score against tile based on all users scores






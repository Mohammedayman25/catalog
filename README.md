# Item catalog

**By Mohammed Ayman**

This is a simple website that displays a catalog of many categories with other items in.

## Required to run

- Virutal box and vagrant (to use the virtual machine)
- Internet (to use google authentication)

## Run

- Navigate to the vagrant folder and boot up the vagrant machine by typing the following commands:
```
vagrant up
vagrant ssh
```
- Inside the virtual machine, navigate to the app folder called "**catalog**" by typing the following command:
```
cd /vagrant/catalog/
```
- Run the "**database_setup.py**" file by typing `python database_setup.py`
- Run the "**fill_database.py**" file by typing `python fill_database.py`
- Run the app by typing `python project.py`
- Finally visit the app at [localhost:8000/](localhost:8000/)

## Main routes

- ## "/" or "/home"
    This page displays all the categories in the database and the latest five items in the database.

- ## "/category_items/<cat_id>"
    This page takes in a category id and displays all the items in the category with this id.

- ## "/category_items/<cat_id>/item/<item_id>"
    This page takes in a category id and item id and displays the data of the item.

- ## "/add_item"
    This page displays a form to add items on GET requests and creates a new item in the database with the given data on POST requests.

- ## "/editItem/<item_id>"
    This page displays a form to edit the item with the provided id in the url on GET requests and updates its data in the database with the given data on POST requests.

- ## "/delete/<cat_id>/<item_id>"
    This page displays a confirmation message that asks the user to confirm the deletion of the item with the id provided in the url on GET requests, and deletes the item using its id from the database on POST requests.

- ## "/login"
    This page displays a button to let the user login using google account on GET requests, and logs the user in with the help of the route "**/gconnect**" and then redirects to the "**/home**" route on POST requests.
- ## "/gdisconnect"
    This page disconnects and logs the user out of the google account and redirects back to the "**/home**" route.

## JSON endpoints (API routes)

- ## "/category_items/<cat_id>/JSON"
    This page returns (in **JSON** format) the id, name and the items of the category with the given id in the url.

- ## "/category_items/<cat_id>/item/<item_id>/JSON"
    This page returns (in **JSON** format) the id, name, description and the category id of the item with the given id in the url.

- ## "/catalog.json"
    This page returns (in **JSON** format) the id, name, and the items of all the categories in the database.
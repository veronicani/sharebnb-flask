# Flask Backend for Sharebnb
Backend server for Sharebnb API. In use by [Sharebnb React Frontend](https://github.com/veronicani/sharebnb-react).

## About The Project
Integrates AWS S3 into relational database for file storage.
![Database schema](/schema.png?raw=true)

See [requirements.txt](https://github.com/veronicani/sharebnb-flask/blob/main/requirements.txt) for a full list of dependencies.

### Getting Started
1. Clone this repo.
    ```sh
    git clone https://github.com/veronicani/sharebnb-flask.git
    ```
2. To install dependencies into a virtual environment (venv), create / activate venv in the project directory. 
    To create new venv
    ```sh
    $ python3 -m venv venv
    ```
    To activate venv: 
    ```sh
    $ source venv/bin/activate
    ```
3. Install requirements.txt.
    ```sh
    (venv) $ pip3 install -r requirements.txt
    ```
    Note: this will override any previous installs in the venv.
4. Run server.
    ```sh
    (venv) $ flask run -p 5000
    ```
    (For some macs, running on port 5000 will lead to an address conflict, so run on port 5001 instead)

### Seeding Data
1. Create new database (requires PostgresQL to be installed):
   ```sh
   createdb sharebnb
   ```
2. To reseed data:
   ```sh
   cd sharebnb-flask
   ```
1. Enter iPython in terminal (while in venv):
   ```sh
   (venv) $ ipython
   ```
2. Run seed file:
    ```py
    In [1]: run seed.py
    ```
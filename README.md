# Flask Backend for Sharebnb
Backend server for Sharebnb API. In use by [Sharebnb React Frontend](https://github.com/veronicani/sharebnb-react).

### Database Schema
Integrates AWS S3 into relational database for file storage.
![Database schema](/schema.png?raw=true)

### To run server
1. Create / activate venv in the project directory. 
  - To create new venv: `$ python3 -m venv venv`
  - To activate venv: `$ source venv/bin/activate`
2. Install requirements.txt.
  - `(venv) $ pip3 install -r requirements.txt`
  - Note: this will override any previous installs in the venv
3. Run server.
  - `$ flask run -p 5000` (5001 for Macs)

### Seeding data
To reseed data:
1. Enter iPython in terminal (while in venv):
- `(venv) $ ipython`
2. Run seed file:
- `In [1]: run seed.py`

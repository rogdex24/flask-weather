# flask-weather

### Steps to setup and run the API on EC2 Instance

1. Download Docker Image  
`docker pull rogdex24/flask-weather:latest`

2. Run Docker Container  
`docker run -d --env-file db.env -p 5000:5000 rogdex24/flask-weather`

The `db.env` file should have the databse configuration details

API Would be accessible on `localhost:5000`

### Setup Project for Development 

1. `git clone`

2. `cd flask-weather`

3. `pip install -r requirements.txt`  
    Add a `.env` file and fill in the database configurations
4. `flask run`

API Would be accessible on `localhost:5000`

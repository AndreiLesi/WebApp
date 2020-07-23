# WebApp

A description of the task is given in the accompanying  PDF (here you can see what the WebApp looks like aswell)

## How to Use:

**1) Install Docker on your machine**

**2) Open a terminal and build the project (run this comand in this folder):**

    docker-composes build 

**3) Start the Application:**

    docker-compose up -d

**4) Initialize the Database on its first startup (else skip this step):**

  - Create an empty database:

        docker-compose exec flask python manage.py createDB

  - Create a dataset with some sample inputs

        docker-compose exec flask python manage.py createSampleDB

**5) Open your browser and open localhost page to see the application:**

    localhost/

**6) Play around with it**

The following tests are available:
  
    Tests/
      |- FalseTest.py (instant Failed Test)
      |- TrueTest.py (instant Successful test)
      |- ShortTest.py (random result, <10 sec. test)
      |- LongTest.py (random result, 10 - 20 sec. test)
  
    ServerTests/
      |- TrueTest.py (instant Successful test)
      |- SuperLongTest.py (random result, 30 - 40 sec. test)


- Run different Tests either from .py files or an entire folder:  
  - Run all Tests in the ServerTests Folder
  
        Requester: Andrei, Environment ID: 1, Test Path: ServerTests 

  - Run one single Test:
  
        Requester: Max, Environment ID: 2, Test Path: Tests/TrueTest 
  
    

- Try invalid inputs:
  - Invalid environment id (not between 1 - 100):
  
        Requester: Danny, Environment ID: 102, Test Path: Tests/TrueTest

  - invalid test path: 

        Requester: Mark, Environment ID: 102, Test Path: abcde

  - Blocked environment id:
    
      1) Start a longer test on an Environment ID:
      
             Requester: Julie, Environment ID: 7, Test Path: Tests/LongTest

      2) Start another test in the same (now busy) environment:
      
             Requester: Jonas, Environment ID: 7, Test Path: Tests/TrueTest
      

**7) Shut down the application by running the following command in the same terminal:**

    docker-compose down

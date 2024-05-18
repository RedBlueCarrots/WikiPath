# WikiPath

WikiPath is a website for users to play the Wikipedia game

## Setup instructions:

Requires python3 and pip

**Make sure you are in the uppermost WikiPath directory.**

Create a virtual environment:

```
python3 -m venv venv
```

Activate the environment:

- WINDOWS :

  ```
  venv\Scripts\activate
  ```

- UNIX:
  ```
  source venv/bin/activate
  ```

Traverse into the Wikipath directory.

Install the requirements via pip:

```
pip install -r requirements.txt
```


To run, simply :

```
flask run
```

And if everything was setup and configured right you should run on port 5000.

Now you can just open the virtual environment and run flask if you want to use the server again.

Testing

Make sure you're in the WikiPath directory and run:
```
python3 -m unittest tests/unit.py
```

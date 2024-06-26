# WikiPath

WikiPath is a website for users to play the [Wikipedia game](https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game). <br>Players start from a particular article and attempt to navigate to a chosen destination article via the hyperlinks in the articles.

Players can create an account and login. Once logged in, they can propose challenges on WikiPath, where other users can view and submit attempts. Challenges are a given start article and destination article, where players compete with each other to find the path of these articles with the fewest article links. Challenges has a set time limit, and once that time limit is over, a winner is decided. Winners gains points called WikiAura.

To prevent users from seeing other users submissions before the challenge is over, each user can only see their own submission until the the remaining time finishes, which then allows users to see all submissions to a challenge.

Viewers of the site (logged in or not), can view all challenges, completed or ongoing. They can also search for a specific challenge via the search bar.

## Group members

| UWA ID   | Name          | Github username |
| -------- | ------------- | --------------- |
| 23450844 | Ethan Yong    | RadiationOcelot |
| 23475912 | Delta Oliver  | DeltaO3         |
| 23334811 | Joseph Newman | RedBlueCarrots  |
| 23443804 | Jaidan Balea  | jaidan18        |

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
Create a secret key:

- WINDOWS :

  ```
  setx FLASK_SECRET_KEY 'insert_secret_key_here'
  ```

- UNIX :
  ```
  export FLASK_SECRET_KEY='insert_secret_key_here'
  ```

Refer to the Database section if you don't have a database.

Run the flask app :

```
flask run
```

By default it should run on port 5000.

You can change the port number if you wish:

```
flask run -p port_number
```

Now you can just open the virtual environment and run flask if you want to use the server again.

## Database

Included in the release/main branch is an empty app.db, i.e. an empty database. You can make a new one if you currently don't have a database.

To do so, in the WikiPath directory, enter the flask shell by:

```
flask shell
```

Then run:

```
db.create_all()
```

Then exit:

```
exit()
```

See [here](https://github.com/RedBlueCarrots/WikiPath/pull/64#issuecomment-2101833081) for creating and doing a database migration if you wish to upgrade the database with new models.

## Testing

Make sure you're in the WikiPath directory and run:

```
python3 -m unittest tests/unit.py
```

To run selenium tests, make sure webdrivers are installed/downloaded before hand. <br>
More information on how we got it to run with Firefox on WSL [here](https://github.com/RedBlueCarrots/WikiPath/pull/84).

Once installed/downloaded, run:

```
python -m unittest tests/selenium.py
```

Note that we could not get the selenium tests to work on Windows.

# WikiPath

WikiPath is a website for users to play the [Wikipedia game](https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game). <br>Players start from a particular article and attempt to navigate to a chosen destination article via the hyperlinks in the articles.

Players can propose challenges on WikiPath, where other users can view and attempt the challenges. Challenges are a given start article and destination article, where players compete with each other to find the path of these articles with the fewest article links. Challenges has a set time limit, and once that time limit is over, a winner is decided. Winners gains points called WikiAura.

## Group members

| UWA ID      | Name     | Github username|
| ------------- | ------------- |--- |
| 23450844|Ethan Yong | RadiationOcelot |
| 23475912 |Delta Oliver| DeltaO3 |
|23334811 | Joseph Newman | RedBlueCarrots|
|23443804 | Jaidan Balea | jaidan18|

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

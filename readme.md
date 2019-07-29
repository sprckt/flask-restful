# Exercise 1

The nest.py script will take a flat JSON array and nest contents as specified through command line arguments.
The order of the command line arguments will stipulate the level that each attribute shall take up

The input of the following format is:

```
[
  {
    "country": "UK",
    "city": "Manchester",
    "currency": "GBP",
    "amount": 200
  },
  {
    "country": "DE",
    "city": "Hamburg",
    "currency": "EUR",
    "amount": 300
  },
  {
    "country": "DE",
    "city": "Berlin",
    "currency": "EUR",
    "amount": 10
  }
 ]
 ```
 
The script shall be executed like this:
 
```
cat input.json | python nest.py currency country city
```

The output of this invocation should be:
```
{
  "GBP": {
    "UK": {
      "Manchester": [
        {
          "amount": 200
        }
      ]
    }
  },
  "EUR": {
    "DE": {
      "Hamburg": [
        {
          "amount": 300
        }
      ],
      "Berlin": [
        {
          "amount": 20
        }
      ]
    }
   }
}
```

# Exercise 2

The nested app in Exercise 1 is now provided as a WebAbpp. The Flask web framework along with Flask-Restful, Flask-HTTPAuth, SqlAlchemy and pytest-flask were used to create the app. 
To launch the app:
- Create virtualenv using `python3 -m venv venv`
- Install all libraries using `pip install -r requirements.txt`
- Run the app using `flask run`
- User credentials to use are `email: e@gmail.com, password: password`. 

You pass the key order to the app using the following syntax and send to the POST /nest endpoint

```.bash
/nest?order=currency&order=country&order=city&order=amount
```

The response from the app will be in the following format:
```json
{"nested": [{}, {}]}
```
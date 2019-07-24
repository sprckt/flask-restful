# Revolut Exercise 1

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

The output of this invocation is:
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
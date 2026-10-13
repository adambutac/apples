# apples
This project has nothing to do with apples.  Instead, it is designed to generate a markov chain based on some input.

## Usage
```
python apples.py words3.txt [order]
```
`order` is how many previous characters each step remembers (default 3). Higher orders sound more like real words but copy the input more often. It prints generated words until you stop it.

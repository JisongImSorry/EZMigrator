import random
import string

def rand_string():
  characters = string.ascii_letters
  random_string = ''.join(random.choice(characters) for _ in range(6))
  return random_string
import os
import sys
from scanner.scann import lexer
import json


sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def likeJson(data):
    return json.dumps(data, indent=2, ensure_ascii=False)

def main():
  data = '''
    a = 1
    b = 2
    c = a + b
    print(c)
  '''

  lexer.input(data)
  for token in lexer:
    print(token)


if __name__ == "__main__":
    main()
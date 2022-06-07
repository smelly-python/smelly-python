import sys
import json

def main():
    print(f"Argument count: {len(sys.argv)}")
    if len(sys.argv) < 2: 
        print('Insufficient parameters provided')
        sys.exit(1)
    with open(sys.argv[1]) as file: 
        dictData = json.load(file)
        print(dictData)
    
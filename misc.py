import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--pr", help="PR number")
  args = parser.parse_args()
  print(f'PR={args.pr} ')

if __name__ == '__main__':
  main()
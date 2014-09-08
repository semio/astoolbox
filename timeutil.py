from datetime import datetime, timedelta

def middate(a, b):
  """find the middle date between 2 dates"""
  if b > a:
    return a + (b - a) / 2
  else:
    raise ValueError

# testy.py
# from signal import signal, alarm, SIGALRM

import sys

TIMER = False
RERAISE = False
ALLOWED_TIME = 1
if TIMER:
  from signal import signal, alarm, SIGALRM

from copy import deepcopy
import time



def print_err(*a):
     print(*a, file = sys.stderr)




# format testów
# TESTS = [ {"arg":arg0, "hint": hint0}, {"arg":arg1, "hint": hint1}, ... ]



def list2str( L ):
  s = ""
  for x in L:
    s += str(x) +", "
  s = s.strip()
  if len(s) > 0:
    s = s[:-1]
  return s

def limit( L, lim=120 ):
  x = str( L )
  if len(x) < lim:
    return x
  else:
    return x[:lim]+"[za dlugie]..."



class TimeOut(Exception):
  def __init__(self):
    pass


def timeout_handler( signum, frame ):
   raise TimeOut()



def internal_runtests( printarg, printhint, printsol, check, TESTS, f ):
  passed = 0
  total  = len(TESTS)
  total_time = 0
  for i,d in enumerate(TESTS):
    print("-----------------")
    print("Test", i )
    arg  = deepcopy(d["arg"])
    hint = deepcopy(d["hint"])
    printarg( *arg )
    printhint( hint )
    try:
      if TIMER:
        signal( SIGALRM, timeout_handler )
        alarm(ALLOWED_TIME + 1)
      time_s = time.time()
      end    = time.time()
      sol    = f( *arg )
      time_e = time.time()

      if TIMER:
        alarm(0)
      printsol( sol )
      res = check( *arg, hint, sol )
      if res: passed += 1
      print("Orientacyjny czas: %.2f sek." % float(time_e-time_s))
      total_time += float(time_e-time_s)
    except TimeOut:
      print("!!!!!!!! PRZEKROCZONY DOPUSZCZALNY CZAS")
    except KeyboardInterrupt:
      print("Obliczenia przerwane przez operatora")
    # except Exception as e:
    #   print("WYJATEK:", e)
    #   if RERAISE: raise e


  print("-----------------")
  print("Liczba zaliczonych testów: %d/%d" % (passed,total) )
  print("Orientacyjny łączny czas : %.2f sek." % total_time )

  print_err(sys.argv[0].replace("_"," ").replace(".py",""), passed, total, "%.2f" % total_time)

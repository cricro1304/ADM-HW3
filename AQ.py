def controllo():
  limitations=[]
  lowerbound=0
  upperbound=0
  d, sumHours= map(int, input().split())
  for _ in range(d):
    limitations.append(tuple(map(int,input().split())))
  for x in range(d):
    lowerbound+=limitations[x][0]
    upperbound+=limitations[x][1]

  if sumHours>upperbound or sumHours<lowerbound:
    print('NO')
  else:
    print('YES')
  funzionericorstiva(d, sumHours, limitations)
  
  

def funzionericorstiva(d, sumHours, limitations, current_report=[]):
  

  if d == 0:
    if sumHours == 0:
      print(*current_report)
    return
  min_limit, max_limit = limitations[-d]
  

  for hours in range(min_limit, min(max_limit, sumHours) + 1):
      funzionericorstiva(d - 1, sumHours - hours, limitations, current_report + [hours])

controllo()

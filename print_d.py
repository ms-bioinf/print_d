from tabulate import tabulate
import matplotlib.pyplot as plt

#############################################################
#
# Code for pretty printing of d and db
#
# print_d is the main function.
#
#############################################################

def print_d(d,db,a,b,**kwargs):
  """
  prints the matrix d in dynamic programming.
  Assumes variables d, a, b, m, n, and optionally db.
  Optional parameters:
  - path (one, all) to print backtracking path(s).
  - style (str, png) to print as text or image with color.
  - edu (all, init, main, result, ij) to highlight some cells.
  """
  path = kwargs.get("path", None)
  style = kwargs.get("style", None)
  edu = kwargs.get("edu", None)

  m=len(a)
  n=len(a)

  if not d:
    print("Matrix d must be defined to use print_d.")
    return

  if path:
    paths = getPaths(db,m,n)
    if path=="one": paths=paths[:1]
    for p in paths:
      print("\n\nMatrix d for alignment\n%s\n\n"%(path2str(a,b,p)))
      if style == "str":
        print("%s\n\n"%(d2str(d,db,a,b,m,n,path=p))) 
      else:
        d2png(d,db,a,b,m,n,path=p)
  else:
    print("\n\nMatrix d\n")
    if style == "str":
      print("%s\n\n"%(d2str(d,db,a,b,m,n))) 
    else:
      d2png(d,db,a,b,m,n)

  if edu:
    if edu=="all":
      d2png(d,db,a,b,m,n,edu="init") # d and db as pretty picture with color
      d2png(d,db,a,b,m,n,edu="main") # d and db as pretty picture with color
      d2png(d,db,a,b,m,n,edu="result") # d and db as pretty picture with color
      d2png(d,db,a,b,m,n,edu="ij") # d and db as pretty picture with color
    else:
      d2png(d,db,a,b,m,n,edu=edu)




#############################################################
#
# Code for pretty printing of d and db
#
#############################################################

def str_ij(d,db,i,j, **kwargs): 
  """returns the contents of cell i,j in d and d_b 
  as a string"""
  style = kwargs.get("style", None)
  if style == "plain":
    d2s = {"N":"^", "W":"<", "NW":"\\"}
  else:
    d2s = {"N":"\u2191", "W":"\u2190", "NW":"\u2196"}
  direction = ""
  if (i,j) in db:
    direction = "".join([d2s[x] for x in db[i,j]])+" "
  return direction+str(d[i,j])



#############################################################
#
# Convert matrix d into a string
#
#############################################################

def d2str(d,db,a,b,m,n,**kwargs):
  """
  returns the matrix d and d_b as string.
  String b is printed as first row and string a as first column.
  i, j iterate through all cells in d and d_b and store
  the cell contents in the list rows.
  Rows is then given as parameter to tabulate, which
  does the layout as a table. Tabulate has many options
  to refine the layout of the table further.
  **kwargs is optionally used to pass a path through the matrix.
  """
  path = kwargs.get("path", None)
  rows = [list("  "+b)]
  for i in range(0,m+1):
    row = [(" "+a)[i]]
    for j in range(0,n+1):
      s = str_ij(d,db,i,j, style="plain")
      if path and (i,j) in path: s = "* "+s
      row.append(s)
    rows.append(row)
  return tabulate(rows, tablefmt="plain", stralign="right")



#############################################################
#
# Print d as an image with matplotlib
#
#############################################################

def d2png(d,db,a,b,m,n,**kwargs):
  path = kwargs.get("path", None)
  edu = kwargs.get("edu", None)
  fig, ax = plt.subplots()
  columns = list("  "+b)
  colors = [list("w"*(n+2)) for i in range(m+1)]
  cell_text = [list(" "*(n+2)) for i in range(m+1)]
  for i in range(m+1):
    for j in range(n+1):
        if (i,j) in d and (i,j) in db:
          cell_text[i][j+1] = str_ij(d,db,i,j)
  the_table = ax.table(cellText=cell_text,
                       cellColours=colors,
                       colLabels=columns,
                       cellLoc='right',
                       loc='center')
  for i in range(m+2): 
    for j in range(n+2):    
      the_table[i,j].set_edgecolor("#A9A9A9")
      the_table[i,j].get_text().set_color("#696969")
      the_table[i,j].set_height(0.2)
      the_table[i,j].set_width(0.2)
  # first row
  for j in range(n+2):    
    the_table[0,j].set_facecolor("#DCDCDC")
    the_table[0,j].get_text().set_color("#000000")
    the_table[0,j].loc="center"
  # first column with centered characters in black on grey background
  for i in range(m+2):    
    the_table[i,0].get_text().set_text(list("  "+a)[i])
    the_table[i,0].loc="center"
    the_table[i,0].set_facecolor("#DCDCDC")
    the_table[i,0].get_text().set_color("#000000")
  # backtracking path
  if path:
    for (i,j) in path:
      the_table[i+1,j+1].get_text().set_color("#000000")
      the_table[i+1,j+1].set_facecolor("#56b5fd")

  if edu and edu=="init":
    for i in range(1,m+2):    
      the_table[i,1].set_facecolor("r")
    for j in range(2,n+2):    
      the_table[1,j].set_facecolor("r")

  if edu and edu=="main":
    for i in range(2,m+2):    
      for j in range(2,n+2):    
        the_table[i,j].set_facecolor("r")

  if edu and edu=="result":
    the_table[m+1,n+1].set_facecolor("r")

  if edu and edu=="ij":
    i,j = 3,2
    the_table[i+1,j+1].set_facecolor("r")
    the_table[0,j+1].set_facecolor("r")
    the_table[i+1,0].set_facecolor("r")
    the_table[i,j].set_facecolor("mistyrose")
    the_table[i,j+1].set_facecolor("mistyrose")
    the_table[i+1,j].set_facecolor("mistyrose")

  ax.axis('tight')
  the_table.set_fontsize(12)
  ax.axis('off')
  plt.show()


#############################################################
#
# Get all paths and alignments from the backtracking matrix
#
#############################################################

def getPaths(db,i,j):
  """
  returns alls paths from bottom right to top left in db.
  """
  if i+j==0:
    return [[(0,0)]]
  paths = []
  if "N" in db[i,j]:
    paths += getPaths(db,i-1,j)
  if "W" in db[i,j]:
    paths += getPaths(db,i,j-1)
  if "NW" in db[i,j]:
    paths += getPaths(db,i-1,j-1)
  for path in paths:
    path.append((i,j))
  return paths

def path2str(a,b,path):
  """prints the alignment corresponding to a given path through the matrix d."""
  (s1,s2) = zip(*path)
  line1 = "  "+"".join([get_char(s1,a,x) for x in range(1,len(s1))])
  line2 = "  "+"".join([get_char(s2,b,x) for x in range(1,len(s2))])
  return "%s\n%s"%(line1,line2)

def get_char(s1,a,x):
  if s1[x]==s1[x-1]: 
    return "-"
  return a[s1[x-1]]

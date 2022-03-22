class Category:
  def __init__(self, name):
    self.name = name
    self.ledger = []

  def __str__(self):
    heading = f"{self.name:*^30}\n"
    deals = ""
    total = 0
    for deal in self.ledger:
      deals += f"{deal['description'][0:23]:23}" + f"{deal['amount']:>7.2f}" + '\n'

      total += deal['amount']

    output = heading + deals + "Total: " + str(total)
    return output

  def deposit(self, amount, description = ""):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description = ""):
    if(self.check_funds(amount)):
      self.ledger.append({"amount": -amount, "description": description})
      return True
    return False

  def get_balance(self):
    total_amount_left = 0
    for item in self.ledger:
      total_amount_left += item["amount"]

    return total_amount_left

  def transfer(self, amount, category):
    if(self.check_funds(amount)):
      self.withdraw(amount,"Transfer to " + category.name)
      category.deposit(amount, "Transfer from " + self.name)
      return True
    return False

  def check_funds(self, amount):
    if(self.get_balance() >= amount):
      return True
    return False

  def get_amount_withdrawn(self):
    total_withdrawn = 0
    for item in self.ledger:
      if item["amount"] < 0:
        total_withdrawn += item["amount"]
    return total_withdrawn

    
  

def truncate(n):
  multiplier = 10
  return int(n * multiplier) / multiplier

def get_totals(categories):
  total = 0
  items = []
  for category in categories:
    total += category.get_amount_withdrawn()
    items.append(category.get_amount_withdrawn())
  final = list(map(lambda x: truncate(x/total), items))
  return final



def create_spend_chart(categories):
  s = "Percentage spent by category\n"
  index = 100
  totals = get_totals(categories)
  while index >= 0:
    cat_space = " "
    for total in totals:
      if total * 100 >= index:
        cat_space += "o  "
      else:
        cat_space += "   "
    s += str(index).rjust(3) + "|" + cat_space + ("\n")
    index -= 10
  
  dash = "-" + "---"*len(categories)
  names = []
  cat_name = ""
  for category in categories:
    names.append(category.name)
  
  index_max = max(names, key=len)

  for x in range(len(index_max)):
    name_str = '     '
    for name in names:
      if x >= len(name):
        name_str +=   "   "
      else:
        name_str += name[x] + "  "

    if(x != len(index_max) -1 ):
      name_str += '\n'

    cat_name += name_str

  s += dash.rjust(len(dash)+4) + "\n" + cat_name
  return s

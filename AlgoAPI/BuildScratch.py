from AlgoAPI import *

class BuildScratch:
  def __init__(self,projectContent):
    self.projectContentJSON = json.loads(projectContent)
  #Берет со сцены все переменные и листы

  def getLists(self):
    a = self.projectContentJSON
    lists = a["targets"][0]["lists"]
    #print(lists)
    return lists

  def getVariables(self): 
    a = self.projectContentJSON
    variables = a["targets"][0]["variables"]
    #print(variables)
    return variables

  def Variable(self, idd,name,value):
    a = self.projectContentJSON
    a["targets"][0]["variables"][idd] = [name,value]

  def List(self, idd,name,value):
    a = self.projectContentJSON
    a["targets"][0]["lists"][idd] = [name,value]

  def DebugPrint(self):
    a = self.projectContentJSON
    print(json.dumps(a, indent=4, ensure_ascii=False))

  def delVariable(self,idd):
    try:
      del self.projectContentJSON["targets"][0]["variables"][idd]
    except (KeyError, TypeError) as e:
      print(f"Error deleting variable: {e}")
  def delList(self,idd):
    try:
      del self.projectContentJSON["targets"][0]["lists"][idd]
    except (KeyError, TypeError) as e:
      print(f"Error deleting variable: {e}")
  def result(self):
    return self.projectContentJSON
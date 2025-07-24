from AlgoAPI import *

class AlgoServe:
  def __init__(self, Cookie, ID):
    global r
    self.Cookie = Cookie
    self.ID = ID
    urll = f"https://learn.algoritmika.org/api/v1/projects/info/{ID}"
    responsecheck = "https://learn.algoritmika.org/api/v1/profile"
    self.header={'cookie': Cookie,'user-agent': "Mozilla"}  
    r = requests.get(responsecheck, headers=self.header)
    #print(r.text)
    if r.status_code == 200:
      r = r.json()
      self.OwnerID = r["data"]["studentId"]
      #print(self.OwnerID)
    else:
      print("Неправильные входные данные аккаунта")
      exit()  
    try:
      r = requests.get(urll, headers=self.header)
      r = r.json()
    except:
      print(r.text)
    try:
      try:
        LId = int(r["data"]["meta"]["scratchId"])
      except:
        LId = int(r["data"]["meta"]["projectId"])
    except:
      LId = None
    self.LocalID = LId
    self.urlScratch = f"https://learn.algoritmika.org/api/v1/scratch/save-project/{self.LocalID}"
    self.urlLoadScratch = f"https://learn.algoritmika.org/api/v1/scratch/load/{self.LocalID}"
    self.urlLoadInfo = f"https://learn.algoritmika.org/api/v1/projects/info/{self.ID}?expand=uploads%2Cvideo%2Cremix%2Ccontest"
    self.urlParseComment = f"https://learn.algoritmika.org/api/v1/projects/comment/{self.ID}"
    response = requests.get(self.urlLoadInfo,headers=self.header).json() 
    #print(response, self.urlLoadInfo)
    if response["data"]["author"]["id"] == self.OwnerID:
      pass
    else:
      print("Ошибка: Это не ваш проект")
      exit()


    self.result = self.ParseScratch()
    self.projectContentJSON = json.loads(self.result)

  def ParseScratch(self):
    try:
            response = requests.get(self.urlLoadScratch, headers=self.header)
            response.raise_for_status()
            try:  
              result = json.dumps(response.json(), indent=4, ensure_ascii=False)  # Красивый вывод JSON
            except json.JSONDecodeError:
                print("Ответ не является JSON, вывод текста:")
                print(response.text)
                result = None  
    except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе ParseScratch: {e}")
            result = None
    
    return result

    if result:
      self.projectContentJSON = json.loads(result)
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

  def startList(self,name,value,idd=None):
    if idd == None: idd = name
    try: return self.getLists()[idd]
    except: self.List(name,value,idd); return self.getLists()[idd]

  def startVariable(self,name,value,idd=None):
    if idd == None: idd = name
    try: return self.getVariables()[idd][1]
    except: self.Variable(name,value,idd); return idd

  def ParseComment(self): 
    try:
      response = requests.get(self.urlParseComment+"?page=1&perPage=1&sort=-created_at",headers=self.header)
      response.raise_for_status()
      a = response.json()
      try:
        self.Name = a["data"]["items"][0]["author"]["name"]
        self.Message = a["data"]["items"][0]["message"]
        self.IDU = a["data"]["items"][0]["author"]["id"]
        return {"Name":a["data"]["items"][0]["author"]["name"],
        "Message":a["data"]["items"][0]["message"],
        "UserId":a["data"]["items"][0]["author"]["id"],
        "isCelebrity":a["data"]["items"][0]["author"]["isCelebrity"],
        "svgUrl":a["data"]["items"][0]["author"]["avatar"]["svgUrl"],
        "createdAt":a["data"]["items"][0]["createdAt"]}

      except (KeyError, IndexError, TypeError) as e:
        print(f"Ошибка при парсинге JSON(нету комментария): {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

  def Variable(self,name,value, idd=None):
    if idd == None: idd = name
    a = self.projectContentJSON
    a["targets"][0]["variables"][idd] = [name,value]

  def List(self,name,value, idd=None):
    if idd == None: idd = name
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
  def Build(self):
    try:
      """
      for i in range(2):
        #print(str(json.loads(self.result)))
        #print("\n")
        #print(str(self.projectContentJSON))
        #print("\n")
        print(str(json.loads(self.result)) == str(self.projectContentJSON))
        r = requests.post(self.urlScratch, headers=self.header, json={"projectContent": json.dumps(self.projectContentJSON)})
        self.result = self.ParseScratch()
      
      exit()
      """
      if str(json.loads(self.result)) == str(self.projectContentJSON):
        pass
      else:
        #self.projectContentJSON = json.loads(self.result)
        r = requests.post(self.urlScratch, headers=self.header, json={"projectContent": json.dumps(self.projectContentJSON)})
        r.raise_for_status()  # Проверяем на HTTP ошибки
        print("Проект обновлен")
        print(r, r.text)
        self.result = self.ParseScratch()
    except requests.exceptions.RequestException as e:
      print(f"Ошибка при запросе ChangeScratchProject: {e} \n {r.text}")
    return self.projectContentJSON

  time.sleep(.5)

  def ChnageVar(self, id):
    pass
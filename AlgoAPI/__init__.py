import requests,time,json,random
from AlgoAPI.Functions import *
from AlgoAPI.BuildScratch import *
#https://learn.algoritmika.org/api/v2/settings/geo/reverse
#POST
#{"accuracy": 124, "lat": 55.663433350177286, "lon": 37.905414853515545}
"""
Завтра:
-Делаем парсинг трендов, поиска, проектов-
-Делаем прикол с геолокацией-
-Парсинг друзей и подписок и одноклассников(по возможности)-
-Setup-
-Документалка-
-SimpleRPost+-
"""
class AlgoAPI:


  def __init__(self, Cookie, ID=0):

    global r
    self.Cookie = Cookie
    self.ID = ID
    urll = f"https://learn.algoritmika.org/api/v1/projects/info/{ID}"
    responsecheck = "https://learn.algoritmika.org/api/v1/profile"
    self.header={'cookie': Cookie,'user-agent': ""}  
    r = requests.get(responsecheck, headers=self.header)
    #print(r.text)
    if r.status_code == 200:
      r = r.json()
      self.OwnerID = r["data"]["studentId"]
      #print(self.OwnerID)
    else:
      print("Неправильные входные данные аккаунта")
      exit()
    

    #Константы
    self.base_url = "https://learn.algoritmika.org/api/v1"
    self.base_urlV2 = "https://learn.algoritmika.org/api/v2"
    self.urlSeeMyProjects = f"https://learn.algoritmika.org/api/v1/projects/index?expand=uploads&isDeleted=0&page=1&perPage=999&projectLang=all&scope=student&sort=-id&type=design%2Cgamedesign%2Cimages%2Cpresentation%2Cpython%2Cscratch%2Cunity%2Cvideo%2Cvscode%2Cwebsite"
    self.UpdateURLS()

    self.Name = ""
    self.Message = ""
    self.source = ''
    self.titlee = ''
    self.projectContent = ''
  def ParseInfoProject(self,ID=None): 
    if not ID is None: self.ID = ID  

    self.UpdateURLS()
    response = requests.get(self.urlLoadInfo,headers=self.header).json()
    return response

  def ParseComment(self,ID=None): 
    if not ID is None: self.ID = ID  

    self.UpdateURLS()
    try:
      response = requests.get(self.urlParseComment+"?page=1&perPage=1&sort=-created_at",headers=self.header)
      response.raise_for_status()
      a = response.json()
    
      try:
        self.Name = a["data"]["items"][0]["author"]["name"]
        self.Message = a["data"]["items"][0]["message"]
        self.IDU = a["data"]["items"][0]["author"]["id"]
        print(self.Name, self.IDU)
        print(self.Message)
      except (KeyError, IndexError, TypeError) as e:
        print(f"Ошибка при парсинге JSON(нету комментария): {e}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")

  def ParseComments(self, lengthComment=2,ID=None):
    if not ID is None: self.ID = ID 

    self.UpdateURLS()
    try:
      try:
        response = requests.get(self.urlParseComment+f"?page=1&perPage={lengthComment}&sort=-created_at",headers=self.header)
        response.raise_for_status()
        a = response.json()
        result = {}
        #print(a)
        try:
          for i in range(lengthComment):
          #print(i+1)
            self.Name = a["data"]["items"][i]["author"]["name"]
            self.Message = a["data"]["items"][i]["message"]
            self.IDMM = a["data"]["items"][i]["author"]["id"]
            self.IDM = a["data"]["items"][i]["id"]
            result[self.IDM] = [self.IDMM,self.Name,self.Message]
          #print(self.Name, self.ID)
          #print(self.Message)
          #print(result)
        except (KeyError, IndexError, TypeError) as e:
          print(f"Ошибка при парсинге JSON(нету комментария): {e}")
      except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
    except:
      print("Ошибка инициализации")
    return result
  
  def ParseScratch(self,ID=None):
      if not ID is None: self.ID = ID  

      self.UpdateURLS()
      self.CPOR()
      try:
            response = requests.get(self.urlLoadScratch, headers=self.header)
            response.raise_for_status()
            try:  
              result = json.dumps(response.json(), indent=4, ensure_ascii=False)  # Красивый вывод JSON
            except json.JSONDecodeError:
                print("Ответ не является JSON, вывод текста:")
                print(response.text)
                return None  
      except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе ParseScratch: {e}")
            return None
      
      return result


  def ParsePython(self,ID=None):
    if not ID is None: self.ID = ID

    self.UpdateURLS()
    self.CPOR()
    a = requests.get(self.urlLoadPython, headers=self.header).json()
    return a["data"]["content"]

  def SimpleRGet(self,url,json=None): 
    self.UpdateURLS()
    try:
      r = requests.get(url,headers=self.header,json=json)
      r.raise_for_status()
      print(r.text)
    except requests.exceptions.RequestException as e:
      print(f"Ошибка при запросе SimpleRGet: {e}")
    return r
  def SimpleRPost(self,url,json=None,files=None):
    self.UpdateURLS()
    try:
      r = requests.post(url,headers=self.header,json=json,files=files)
      r.raise_for_status()
      print(r.text)
    except requests.exceptions.RequestException as e:
      print(f"Ошибка при запросе SimpleRGet: {e}")
    return r
  def ChangePyProject(self,titlee,source,ID=None):
    if not ID is None: self.ID = ID

    self.UpdateURLS()
    try:
      r = requests.post(self.urlPython, headers=self.header, json={"content": source, "name": titlee})
      r.raise_for_status()  # Проверяем на HTTP ошибки
      print(r, r.text)
    except requests.exceptions.RequestException as e:
      print(f"Ошибка при запросе ChangePyProject: {e}")

  def ChangeScratchProject(self,projectContent,ID=None):
    if not ID is None: self.ID = ID

    self.UpdateURLS()
    try:
      r = requests.post(self.urlScratch, headers=self.header, json={"projectContent": json.dumps(projectContent)})
      r.raise_for_status()  # Проверяем на HTTP ошибки
      print(r, r.text)
    except requests.exceptions.RequestException as e:
      print(f"Ошибка при запросе ChangeScratchProject: {e} \n {r.text}")
#titlee,desc,preview,Remix
  def ChangeSettingsProject(self,title=None,desc=None,preview=None,remix=None,ID=None):
    if not ID is None: self.ID = ID 

    self.UpdateURLS()

    try:
      jsonn = {}
      if title != None:
        jsonn["title"] = title
      if desc != None:
        jsonn["description"] = desc
      if preview != None:
        jsonn["previewName"] = preview
      if remix != None:
        jsonn["isRemixEnabled"] = remix
      print(jsonn)
      r = requests.post(self.urlDescChanger, headers=self.header, json=jsonn)
      r.raise_for_status()  # Проверяем на HTTP ошибки
      print(r, r.text)
    except requests.exceptions.RequestException as e:
      print(f"Ошибка при запросе ChangeDescProject: {e}")


  def CreateProject(self,type="scratch", title=None, ID=None):
    if not ID is None: self.ID = ID 

    self.UpdateURLS()

    jsonn = None

    if type == "python": 
      get = self.base_url+"/python/create"; 
      if title == None: jsonn = {"name": f"Created_by_AlgoAPI_{random.randint(1,9999999999999999999)}"}
      else: jsonn = {"name": title}

    elif type == "video": 
      get = self.base_urlV2+"/video/create" 
      if title == None: jsonn = {"title": f"Created by AlgoAPI"} 
      else: jsonn = {"title": title}

    else: get = self.base_url+"/scratch/create"; type = "scratch"
    print(get)
    r = requests.post(get,headers=self.header, json=jsonn).json()
    if type == "scratch": 
      self.ID = r["data"]["project"]["projectRelationId"]; 
      self.LocalID = r["data"]["project"]["id"]
      if type == "scratch" and title != None: 
        self.ChangeSettingsProject(title=title)
    elif type == "python": self.ID = r["data"]["projectRelationId"]; self.LocalID = r["data"]["id"]; return r["data"]["projectRelationId"];
    elif type == "video":  self.ID = r["data"]["projectRelationId"]; return r["data"]["projectRelationId"];
  #-----------------
  def ChangeDescAvatar(self,title=None):
    if title == None:
      print("Вы не ввели title: ChangeDescAvatar(title='')")
    else:
      url = "https://learn.algoritmika.org/api/v2/community/profile/update"
      r = requests.post(url, headers=self.header, json={"about":title})
      print(r.text)
  def ChangeAvatar(self,items=None,character=None,gender=None,skinTone=None):
    url = "https://learn.algoritmika.org/api/v2/avatar/save"
    jsonn = {}
    if items!=None: jsonn["items"] = items
    if character!=None: jsonn["avatarId"] = character
    if gender!=None: jsonn["gender"] = gender
    if skinTone!=None: jsonn["skinTone"] = skinTone
    print(jsonn)
    r = requests.post(url, headers=self.header, json=jsonn)
    print(r.text)
  def LoadAvatar(self):
    url = "https://learn.algoritmika.org/api/v2/avatar/items/equipped"
    get = requests.get(url,headers=self.header).json()
    #print(get)
    gender = get["data"]["avatar"]["meta"]["gender"]
    skinTone = get["data"]["avatar"]["meta"]["skinTone"]
    avatarId = get["data"]["avatar"]["id"]
    itemss=[]
    for i in range(len(get["data"]["items"])):
      itemss.append(get["data"]["items"][i]["id"])
    print(f"items={itemss},character={avatarId},gender='{gender}',skinTone='{skinTone}'")
  #-----------------
  def CPOR(self):
    self.urlLoadInfo = f"https://learn.algoritmika.org/api/v1/projects/info/{self.ID}?expand=uploads%2Cvideo%2Cremix%2Ccontest"
    response = requests.get(self.urlLoadInfo,headers=self.header).json() 
    #print(response, self.urlLoadInfo)
    if response["data"]["remix"]["isRemixEnabled"] == 1 or response["data"]["author"]["id"] == self.OwnerID:
      return True
    else:
      print("Ошибка: Доступ к проекту, заблокировал чужой автор")
      exit()


  def UpdateURLS(self):
    urll = f"https://learn.algoritmika.org/api/v1/projects/info/{self.ID}"
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
    self.urlParseComment = f"https://learn.algoritmika.org/api/v1/projects/comment/{self.ID}"
    self.urlPython = f"https://learn.algoritmika.org/api/v1/python/save?id={self.LocalID}"
    self.urlDescChanger = f"https://learn.algoritmika.org/api/v1/projects/update/{self.ID}"
    self.urlScratch = f"https://learn.algoritmika.org/api/v1/scratch/save-project/{self.LocalID}"
    self.urlLoadScratch = f"https://learn.algoritmika.org/api/v1/scratch/load/{self.LocalID}"
    self.urlLoadPython = f"https://learn.algoritmika.org/api/v1/python/preview?id={self.LocalID}"
    self.urlLoadImagePreview = f"https://learn.algoritmika.org/api/v1/projects/save-image-preview?projectId={self.ID}"
    self.urlLoadInfo = f"https://learn.algoritmika.org/api/v1/projects/info/{self.ID}?expand=uploads%2Cvideo%2Cremix%2Ccontest"



  time.sleep(0.5) #Включена задержка, рекомендовано для стабильности сервера алгоритмики



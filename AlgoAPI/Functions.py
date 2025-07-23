from AlgoAPI import *

global StudentID
#ОТДЕЛЬНЫЕ ФУНКЦИИ, КОТОРЫЕ НЕ ЗАВИСИТ ОТ КЛАССА AlgoAPI
def Login(login,password):
  urlLogin = 'https://learn.algoritmika.org/s/auth/api/e/student/auth' #Mozilla
  response = requests.post(urlLogin, headers={"user-agent": "Mozilla"},  # Рекомендуется актуальный User-Agent
                                     json={"login": str(login), "password": str(password)})
  if response.status_code == 200:
    a = response.json()
    return f"studentId={a["item"]["studentId"]};studentAccessToken={a["item"]["studentAccessToken"]}; studentCreatedTimestamp={a["item"]["studentCreatedTimestamp"]}"  # Сохраняем куки как атрибут класса
  else:
    print("Неправильный логин и пароль")
    print(response.text)
    return None
def TokenLogin(sID=0,sToken=0,sTime=0):
  #Эти данные обновляется, когда авторизуриешься еще раз
  return f"studentId={sID};studentAccessToken={sToken}; studentCreatedTimestamp={sTime}"

def BeautifulJSON(res):
  result = json.dumps(res, indent=4, ensure_ascii=False)
  return result
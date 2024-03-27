import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate('obj_database.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


# Autenticação
def authentication(user='', password=''):
    users_db = db.collection("users").stream()
    for user_db in users_db:
        if user == user_db.id and password == user_db.get('senha'): return True
    return False


#Puxar cards
def get_tasks(candidate):
    todo = db.collection(f"todo/{candidate}/tasks").stream()
    for task in todo:
        print(task.get('instrutor'))

#Criar task
def add_tasks(instructor, message, status, type, candidate):
    #Adquirindo o ultimo elemento
    last_id = 0
    tasks = db.collection(f"todo/{candidate}/tasks").stream()
    for task in tasks: last_id = int(task.id) + 1
    #Adicionando task
    tasks = db.collection(f"todo/{candidate}/tasks").document(str(last_id))
    tasks.set({'instrutor':instructor, 'mensagem':message, 'status':status, 'tipo':type})

#Puxar informações de cards
def get_cards(candidate):
    cards = {
        'aFazer': [],
        'concluido':[],
        'confirmado':[]
    }
    tasks = db.collection(f"todo/{candidate}/tasks").stream()
    for task in tasks:
        if task.get('status') == 'aFazer':
            cards['aFazer'].append(
                {
                    'id':task.id,
                    'instrutor':task.get('instrutor'),
                    'mensagem':task.get('mensagem'),
                    'tipo':task.get('tipo')
                }
            )
        elif task.get('status') == 'concluido':
            cards['concluido'].append(
                {
                    'id':task.id,
                    'instrutor':task.get('instrutor'),
                    'mensagem':task.get('mensagem'),
                    'tipo':task.get('tipo')
                }
            )
        elif task.get('status') == 'confirmado':

            cards['confirmado'].append(
                {
                    'id':task.id,
                    'instrutor':task.get('instrutor'),
                    'mensagem':task.get('mensagem'),
                    'tipo':task.get('tipo')
                }
            )

    return cards

def task_concluded(id, candidate):
    tasks = db.collection(f"todo/{candidate}/tasks").document(str(id))
    tasks.update({'status':'concluido'})
    return True

def task_inconcluded(id, candidate):
    tasks = db.collection(f"todo/{candidate}/tasks").document(str(id))
    tasks.update({'status':'aFazer'})

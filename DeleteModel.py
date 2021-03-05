import sys
sys.path.append('/usr/src/app')

from app import create_app
from app.utils import get_model

from pymongo import MongoClient
from bson.objectid import ObjectId


if __name__ == '__main__':

    app = create_app()
    if len(sys.argv) >= 2:
        with app.app_context():
            if sys.argv[1] == "help":
                print("можно использовать {package,batch, order} комманды")

            elif sys.argv[1] == "package" and len(sys.argv)==2:
                get_model('Package')._get_collection().delete_many({})#Удаляет все метки
                print("Удаление всех меток")

            elif sys.argv[1] == "batch":
                get_model('Batch')._get_collection().delete_many({})

            elif sys.argv[1] == "order" :
                get_model('Order')._get_collection().delete_many({})

            elif sys.argv[1] == 'package' and len(sys.argv)>=3: # Точечно удалет одну метку или более , которую(ые)нужно вводить после пробела
                if sys.argv[1] == 'package' and sys.argv[2]=='parse':
                    try:
                        file = open(sys.argv[3])
                        fread = file.read()
                        needItemStack = [line.strip() for line in fread.split()]
                        print("Считывание меток из файла")
                        file.close()

                    except FileNotFoundError:
                        print("файл не найден")
                        sys.exit(0)


                else:
                    print("Обработка запроса...")
                    needItemStack = sys.argv[2:]

                flag = False
                needId = []

                #Инициализируем подключение к базе
                client = MongoClient('192.168.1.178',27017)
                db = client.test
                collection = db['packages']
                cursor = collection.find({})

                _id = None
                rfid = None
                for doc in cursor:
                    rfid = doc['rfid']
                    _id = doc['_id']

                    if rfid in needItemStack:
                        needId.append(_id)
                        flag = True

                if flag == True:
                    print("Удаление...")
                if flag == False:
                    print("Такой метки не существует")
                for itemId in needId:
                     collection.remove({ "_id" : ObjectId(itemId) })

                if _id == None:
                    print("В списке нету меток")

# Делает проверку на правильность написания

    if len(sys.argv) == 1 or sys.argv[1]=='':
        print("Требуется значение после имени файла")

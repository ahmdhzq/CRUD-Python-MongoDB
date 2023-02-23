import pymongo

# membuat koneksi url mongo
koneksi_url ="mongodb://localhost:27017"

def cekKoneksi() :
    client = pymongo.MongoClient(koneksi_url)
    try:
        cek = client.list_database_names()
        print(cek)
    except:
        print('database error')

cekKoneksi()

# membuat database baru
def createDatabase():
    myclient = pymongo.MongoClient(koneksi_url)
    mydatabase = myclient['db_wisatawan']
    mycollection = mydatabase['wisatawan']
    value_data = mycollection.insert_one({'nama' : "Jono", 'asal' : "Yogyakarta"})
    print("berhasil menambahkan data")
    print(value_data)


# melakukan inisialisasi pada class MongoCrud
class MongoCRUD:
    def __init__(self, data, koneksi):
        self.client = pymongo.MongoClient(koneksi)
        database = data['database']
        collection = data['collection']
        cursor =self.client[database]
        self.collection=cursor[collection]
        self.data = data

    # function read data
    def read(self):
        documents = self.collection.find()
        value = [{
            item:data[item] for item in data if item != '_id'} for data in documents]
        return value
    
    # function create data
    def createData(self, data):
        new_document = data['document']
        response = self.collection.insert_one(new_document)
        value = {
            'status' : 'berhasil',
            'document_id' : str(response.inserted_id)
        }
        return value

    def updateData(self):
        data_awal = self.data['dataAwal']
        update_data = {
            "$set" : self.data['dataUpdate']
        }

        response = self.collection.update_one(data_awal, update_data)
        value = {
            "status" : "berhasil diupdate" if response.modified_count > 0 else "data tidak ditemukan"
        }

        print(value)
    
if __name__ =='__main__':
    data = {
        #nama database yang akan disambungkan
        "database" : "db_wisatawan",
        #nama collection yang akan disambungkan
        "collection" : "wisatawan",

        # data yang akan diupdate
        "dataAwal" : {
            "nama" : "Jono",
            "asal" : "Yogyakarta"
        },

        "dataUpdate" : {
            "nama" : "Roki",
            "asal" : "Madiun"
        }
    }

    mongo_objek = MongoCRUD(data, koneksi_url)
    update = mongo_objek.updateData()
    print(update)
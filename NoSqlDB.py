from rethinkdb import r


class RethinkDatabase:

    def __init__(self):
        super(RethinkDatabase, self).__init__()



    def InsertData(self,measurementvalue,datatime,tagname,value,devicename,count):
        r.connect('127.0.0.1', 28015).repl()
        self.connection = r.connect(db='synfodriver')
        try:
            r.table_create('modbusdata').run(self.connection)
        except:
            print("ookkk")
        self.modbusdata = r.table('modbusdata')

        jsonvalue={
            'id': count,
            'tagname': tagname,
            'time': r.now().to_iso8601().run(self.connection),
            'devicename': devicename
        }
        print(jsonvalue)
        self.modbusdata.insert(jsonvalue).run(self.connection)

        for modbus in self.modbusdata.run(self.connection):
            print('modbus',modbus)

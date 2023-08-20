import json
import os

class project:
    def __init__(self,_dir: str):
        self.base = {
                "model": {},
                "circuits": {"0": {}},
                "quantic": {},
                "chemical": {},
                "files": []
            }
        
        
        
        self.name = os.path.basename(_dir)

        self.dir = _dir

        self.project = self.load()

    def save(self):
        with open(self.dir,"w") as ProjFile:
            data = json.dumps(self.project,indent=4)
            ProjFile.write(data)
            print(data)
            ProjFile.close()

        

    def load(self):
        
        if os.path.isfile(self.dir):
            with open(self.dir) as ProjFile:
                data = ProjFile.read()
                if data == "":
                    return self.base
                
                return json.loads(data)
            
        else:
            return self.base



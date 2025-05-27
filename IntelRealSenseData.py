import json 

#This script contains additional informations 
# about intel real sense devices
#and packs them to json format

class IntelRealSenseData:
    intel_json_data = """
    [
        {
            "name": "Lidar L500",
            "serial number": "f1320623"


        },

        {
            "name": "Depth Camera D435i Dev 1", 
            "serial number": "241122074115"
        },

        {
            "name":  "Depth Camera D435i Dev 2",
            "serial number": "No data"
        }
        
    ]
    """

    def __init__(self):
        self.data = self.loadJson()

    
    def loadJson(self):
        """
        Function loads json data to python dict format.
        """

        data_dict = json.loads(self.intel_json_data)
        return data_dict

        

    def matchSerialNumber(self, device_name: str):
        """
        Function finds and returns serial number of the device if the device_name exists in json data
        """
        for data_item in self.data:
            if data_item.get("name") == device_name:
                serial_number = data_item.get("serial number")
                return(serial_number)




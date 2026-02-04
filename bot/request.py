import requests



class Get_Requests:
    
    @staticmethod
    def make_request(url1: str):
        
        url = "http://localhost:8000/sql/" + url1
            
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() 
            return data
        else:
            print(f"Ошибка: {response.status_code}")



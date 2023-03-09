# -*- coding:utf-8 -*-
from flask import Flask,request, jsonify
import json
import ast
import time
 
app = Flask(__name__)
 
@app.route('/notification', methods = ['POST'])
def event_receiver():
    if request.method == 'POST':
        
        
        res = request.data
        data_list = res.split(b"--myboundary\r\n")
        
        if data_list:
            for a_info in data_list:
                if b"Content-Type" in a_info:
                    lines = a_info.split(b"\r\n")
                    a_type = lines[0].split(b": ")[1]
 
                    if a_type == b"image/jpeg":
                        image_data = b"\r\n".join(lines[3:-3])
                    else:
                        text_data = b"\r\n".join(lines[3:-1])
        
 
        evento_str = text_data.decode("utf-8")
        evento_dict = ast.literal_eval(evento_str.replace("--myboundary--", " "))
        json_object = json.dumps(evento_dict, indent = 4) 
        resp_dict = json.loads(json_object)
 
        print(resp_dict)
 
        event_code = resp_dict.get("Events")[0].get('Code')
        print("################## ", event_code, " ##################")
 
        if event_code == "AccessControl":
            event_data = resp_dict.get("Events")[0].get('Data')
            
            card_name = event_data.get('CardName')
            card_no = event_data.get('CardNo')
            card_type = event_data.get('CardType')
            door = event_data.get('Door')
            error_code = event_data.get('ErrorCode')
            method = event_data.get('Method')
            reader_id = event_data.get('ReaderID')
            event_status = event_data.get('Status')
            event_type = event_data.get('Type')
            event_entry = event_data.get('Entry')
            event_utc = event_data.get('UTC')
            user_id = event_data.get('UserID')
            user_type = event_data.get('UserType')
            pwd = event_data.get('DynPWD')
            
            
            print("UserID: ",  user_id)
            print("UserType", user_type)
            print("CardName: ", card_name)
            print("CardNo: ", card_no)
            print("CardType: ", card_type)
            print("Password: ", pwd)
            print("Door: ", door)
            print("ErrorCode: ", error_code)
            print("Method: ", method)
            print("ReaderID: ", reader_id)
            print("Status: ", event_status)
            print("Type: ", event_type)
            print("Entry: ", event_entry)
            print("UTC: ",  event_utc)
            print(49 * "#")
 
            # Exemplo de regras que podem ser implementadas
            time.sleep(1)
            if user_id == 6:
                return jsonify({"message": "Pagamento não realizado!", "code": "200", "auth": "false"})
            elif card_no in ["EC56D271", "09201802"]: # Caso o código do cartão esteja listado libera o acesso
                return jsonify({"message": "Bem vindo !", "code": "200", "auth": "true"})
            elif pwd != None:
                if int(pwd) == 222333:
                    return jsonify({"message": "Acesso Liberado", "code": "200", "auth": "true"})
 
        elif event_code == "DoorStatus":
            event_data = resp_dict.get("Events")[0].get('Data')
            
            door_status = event_data.get('Status')
            door_utc = event_data.get('UTC')
            
            print("Door Status: ",  door_status)
            print("UTC", door_utc)
            print(49 * "#")
            return jsonify({"message": "", "code": "200", "auth": "false"})
        
        elif event_code == "BreakIn":
            event_data = resp_dict.get("Events")[0].get('Data')
            
            door_name = event_data.get('Name')
            door_utc = event_data.get('UTC')
            
            print("Door Name: ",  door_name)
            print("UTC", door_utc)
            print(49 * "#")
            return jsonify({"message": "", "code": "200", "auth": "false"})
        
        
    return jsonify({"message": "", "code": "200", "auth": "false"})
 
    '''
    O retorno deverá ser um JSON, contendo as informações:
    
    "message": "", // Mensagem que será exibida no display
    "code": "200", // Codigo sempre é 200.
    "auth": "", Boolean, corresponde se a porta irá ser acionada ou não. 
    
    '''
 
@app.route('/keepalive', methods = ['GET'])
def keep_alive():
    return "OK"
 
    '''
    Deverá ser retornado uma request que contenha código 200.
 
    '''
 
# Server Start
if __name__ == '__main__':
    app.run(host='192.168.3.14', debug=False, port=3000)
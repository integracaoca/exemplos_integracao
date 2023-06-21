from os.path import abspath, dirname, join
import requests
from datetime import datetime

'''
    Este projeto tem como objetivo fornecer exemplos de utilização da API de integração com dispositivos de controle de acesso na linguagem Python. 
    É importante ressaltar que os exemplos fornecidos são apenas ilustrativos e podem não estar atualizados. Portanto, é recomendado consultar a documentação oficial para obter as chamadas finais e atualizadas.
'''

save_dir = join(dirname(abspath(__file__)), "s_files") # diretorio para salvar imagens

class IntelbrasAccessControlAPI:
    def __init__(self, ip: str, username: str, passwd: str):
        self.ip = ip   
        self.username = username                            
        self.passwd = passwd
        self.digest_auth = requests.auth.HTTPDigestAuth(self.username, self.passwd)

    ##### Device Manager #####
    def get_current_time(self) -> datetime:
        try:
            url = "http://{}/cgi-bin/global.cgi?action=getCurrentTime".format(
                                        str(self.ip), 
                                    )
                
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()
            
            data = self._raw_to_dict(raw)
                 
            date_time_obj = datetime.strptime(data.get('result').replace("-", "/"), '%Y/%m/%d %H:%M:%S')

            if result.status_code != 200:
                raise Exception()
            return date_time_obj
        except Exception:
            raise Exception("ERROR - During Get Current Time")
    
    def set_current_time(self) -> str:
        try:
            current_datetime = datetime.today().strftime('%Y-%m-%d') + '%20' + datetime.today().strftime('%H:%M:%S')

            url = "http://{}/cgi-bin/global.cgi?action=setCurrentTime&time={}".format(
                                        str(self.ip),
                                        str(current_datetime), 
                                    )
                
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Current Time")
        
    def get_ntp_config(self) -> dict:
        try:
            url = "http://{}/cgi-bin/configManager.cgi?action=getConfig&name=NTP".format(
                                        str(self.ip)
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            ntp_config = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return ntp_config
        except Exception:
            raise Exception("ERROR - During Get NTP Config")
        
    def set_ntp_config(self, address: str, port: str, enable: bool) -> str:
        try:
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&NTP.Address={}&NTP.Port={}&NTP.Enable={}".format(
                                        str(self.ip),
                                        str(address),
                                        str(port),
                                        str(enable).lower(),
                                    )    
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            
            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set NTP Config")
        
    def get_software_version(self) -> str:
        try:
            url = "http://{}/cgi-bin/magicBox.cgi?action=getSoftwareVersion".format(
                                        str(self.ip), 
                                    )
        
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            
            firmware_version = data.get('version')

            if result.status_code != 200:
                raise Exception()
            return firmware_version
        except Exception:
            raise Exception("ERROR - During Get Software Version")
    
    def get_network_config(self) -> dict:
        try:
            url = "http://{}/cgi-bin/configManager.cgi?action=getConfig&name=Network".format(
                                        str(self.ip), 
                                    )
                
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            
            network_config_dict = data

            if result.status_code != 200:
                raise Exception()
            return network_config_dict
        except Exception:
            raise Exception("ERROR - During Get Network Config")
    
    def get_device_serial(self) -> str:
        try:
            url = "http://{}/cgi-bin/magicBox.cgi?action=getSerialNo".format(
                                        str(self.ip), 
                                    )
                
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            device_serial = data.get('sn')

            if result.status_code != 200:
                raise Exception()
            return device_serial
        except Exception:
            raise Exception("ERROR - During Get Device Serial")
    
    def get_cgi_version(self) -> str:
        try:
            url = "http://{}/cgi-bin/IntervideoManager.cgi?action=getVersion&Name=CGI".format(
                                        str(self.ip), 
                                    )
                
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            cgi_version = data.get('version')

            if result.status_code != 200:
                raise Exception()
            return cgi_version
        except Exception:
            raise Exception("ERROR - During Get CGI Version")
    
    def get_device_type(self) -> str:
        try:
            url = "http://{}/cgi-bin/magicBox.cgi?action=getSystemInfo".format(
                                        str(self.ip), 
                                    )
                
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            device_type = data.get('deviceType')

            if result.status_code != 200:
                raise Exception()
            return device_type
        except Exception:
            raise Exception("ERROR - During Get Device Type")
    
    def set_network_config(self, new_ip: str, new_gateway: str, new_mask: str, dhcp: bool) -> str:
        try:
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&Network.eth0.IPAddress={}&Network.eth0.DefaultGateway={}&Network.eth0.SubnetMask={}&Network.eth0.DhcpEnable={}".format(
                                        str(self.ip),
                                        str(new_ip),
                                        str(new_gateway),
                                        str(new_mask),
                                        str(dhcp).lower(),
                                    )
                
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Network Config")
        
    def reboot_device(self) -> str:
        try:
           url = "http://{}/cgi-bin/magicBox.cgi?action=reboot".format(
                                        str(self.ip),
                                     )
           result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
           
           if result.status_code != 200:
               raise Exception()
           return str(result.text)
        except Exception:
            raise Exception("ERROR - During Reboot Device") 

    ##### Event Server Manager #####
    def set_event_sender_configuration(self, state: bool, server_address: str, port: int, path: str) -> str:
            '''
            state: True / False
            server_address: Endereço de IP ou DDNS do servidor
            port: Porta do Servidor
            path: Path do servidor, exemplo /notification
            '''
            try:

                url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&PictureHttpUpload.Enable={}&PictureHttpUpload.UploadServerList[0].Address={}&PictureHttpUpload.UploadServerList[0].Port={}&PictureHttpUpload.UploadServerList[0].Uploadpath={}".format(
                                            str(self.ip),
                                            str(state).lower(),
                                            str(server_address),
                                            str(port),
                                            str(path)
                                        )
                    
                result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

                if result.status_code != 200:
                    raise Exception()
                return str(result.text)
            except Exception:
                raise Exception("ERROR - During Set Current Time")

    ##### Door Config #####
    def open_door(self, door : int) -> str:
        '''
        Send a remote command to open door, default value for door is 1
        '''
        try:
            url = "http://{}/cgi-bin/accessControl.cgi?action=openDoor&channel={}".format(
                                        str(self.ip),
                                        str(door) 
                                    )
                
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Open Door - ", e)

    def close_door(self, door : int) -> str:
        '''
        Send a remote command to open close, default value for door is 1
        '''
        try:
            url = "http://{}/cgi-bin/accessControl.cgi?action=closeDoor&channel={}".format(
                                        str(self.ip),
                                        str(door)
                                    )
                
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Close Door - ",e)
        
    def set_door_state(self, state: int) -> str:
        '''
        0 = Normal/Estado normal de porta
        1 = CloseAlways/Porta sempre fechada   
        2 = OpenAlways/Porta sempre aberta
        '''
        try:
            estado = ['Normal','CloseAlways','OpenAlways']
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].State={}".format(
                                        str(self.ip),
                                        str(estado[state]),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Door State")
    
    def set_door_sensor_delay(self, CloseTimeout: int) -> str:
        try: 
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].CloseTimeout={}".format(
                                        str(self.ip),
                                        str(CloseTimeout),
                                )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Door Sensor Delay")

    def set_door_sensor_state(self, SensorType: int) -> str: 
        '''
        0 = Sempre Aberto
        1 = Sempre Fechado
        '''
        try:
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AccessControlGeneral.SensorType={}".format(
                                        str(self.ip),
                                        str(SensorType),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Door Sensor State")

    def set_door_name(self, Name: str) -> str:
        try:
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].Name={}".format(
                                        str(self.ip),
                                        str(Name),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Door Name")
        
    def enable_door_sensor(self, SensorEnable: bool) -> str:
        try: 
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].SensorEnable={}".format(
                                        str(self.ip),
                                        str(SensorEnable).lower(),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Enable Door Sensor ")
        
    def set_door_unlock_interval(self, UnlockHoldInterval: int) -> str:
        try: 
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].UnlockHoldInterval={}".format(
                                        str(self.ip),
                                        str(UnlockHoldInterval),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Unlock Interval")
        
    def enable_exit_button(self, ButtonExitEnable: bool) -> str:
        try: 
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AccessControlGeneral.ButtonExitEnable={}".format(
                                        str(self.ip),
                                        str(ButtonExitEnable).lower(),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Enable/Disable Exit Button")
        
    def set_door_verification_method(self, Method: int) -> str: 
        try: 
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].Method={}".format(
                                        str(self.ip),
                                        str(Method),
                                    ) 
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During set Door Verification Method")

    def set_open_timezone(self,OpenAlwaysTime: int) -> str:
        try:
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].OpenAlwaysTime={}".format(
                                        str(self.ip),
                                        str(OpenAlwaysTime),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception :
            raise Exception("ERROR - During Open Timezone")
        
    def set_close_timezone(self,CloseAlwaysTime: int) -> str:
        try:
            url = "http://1{}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].CloseAlwaysTime={}".format(
                                        str(self.ip),
                                        str(CloseAlwaysTime),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception :
            raise Exception("ERROR - During Close Timezone")
        
    def get_door_config(self) -> dict:
        try: 
            url = "http://{}/cgi-bin/configManager.cgi?action=getConfig&name=AccessControlGeneral".format(
                                        str(self.ip),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception :
            raise Exception("ERROR - During Get Door Config")

    def get_door_state(self, door: int) -> str:
        '''
        Return Close or Open to Door State
        '''
        try:
            url = "http://{}/cgi-bin/accessControl.cgi?action=getDoorStatus&channel=1".format(
                                        str(self.ip),
                                        str(door)
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            
            door_state = data.get('Info.status')

            if result.status_code != 200:
                raise Exception()
            return str(door_state)
        except Exception as e:
            raise Exception("ERROR - During Get Door State - ", e)

    def set_access_control_door_enable(self, state: bool) -> str:
        try:
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].Enable={}".format(
                                        str(self.ip),
                                        str(state).lower()
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Enable Door - ",e)
    
    def stop_alarm_v2(self) -> str:
        try:
            url = "http://{}/cgi-bin/configManager.cgi?action=setConfig&AlarmStop.stopAlarm=true".format(
                                        str(self.ip),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Stop Alarm V2 ",e)

# User Manager

    def delete_all_users_v1(self) -> str:
        '''
        This command delete all user and credential incluse in device
        '''
        try:
            url = "http://{}/cgi-bin/recordUpdater.cgi?action=clear&name=AccessControlCard".format(
                                        str(self.ip)
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Remove All Users using V1 command - ", e)

    def delete_all_users_v2(self) -> str:
        '''
        This command delete all user and credential incluse in device
        '''
        try:
            url = "http://{}/cgi-bin/AccessUser.cgi?action=removeAll".format(
                                        str(self.ip)
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Remove All Users using V2 command - ", e)

    def add_user_v1(self, CardName: str, UserID: int, CardNo: str, CardStatus: int, CardType: int, Password: int, Doors: int) -> dict:
        '''
        CardName: Nome do Usuário / Nome do Cartão
        UserId: Numero de ID do Usuário
        CardNo: Código Hexadecimal do Cartão
        CardStatus:  0 = Normal, 1 = Cancelado, 2 = Congelado
        CardType: 0 = Ordinary card, 1 = VIP card, 2 = Guest card, 3 = Patrol card, 4 = Blocklist card, 5 = Duress card
        Password: Senha de Acesso, Min 4 - Max 6
        Doors: Portas de Acesso, Default 0
        '''
        try:
            url = "http://{}/cgi-bin/recordUpdater.cgi?action=insert&name=AccessControlCard&CardNo={}&CardStatus={}&CardName={}&UserID={}&Password={}&CardType={}&Doors[0]={}".format(
                                        str(self.ip),
                                        str(CardNo).upper(),
                                        str(CardStatus),
                                        str(CardName),
                                        str(UserID),
                                        str(Password),
                                        str(CardType),
                                        str(Doors),
                                    )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception as e:
            raise Exception("ERROR - During Add New User using V1 command - ", e)
  

    def config_online_mode(self, enable, server_address, port, path_event, device_mode, enable_keepalive, interval_keepalive, path_keepalive, timeout_keepalive, timeout_response) -> bool:
        try:

            url_server_config = "http://{}/cgi-bin/configManager.cgi?action=setConfig&PictureHttpUpload.Enable={}&PictureHttpUpload.UploadServerList[0].Address={}&PictureHttpUpload.UploadServerList[0].Port={}&PictureHttpUpload.UploadServerList[0].Uploadpath={}".format(
                                        str(self.ip),
                                        str(enable),
                                        str(server_address),
                                        str(port),
                                        str(path_event),
                                    )

            url_keepalive_config = "http://{}/cgi-bin/configManager.cgi?action=setConfig&Intelbras_ModeCfg.DeviceMode={}&Intelbras_ModeCfg.KeepAlive.Enable={}&Intelbras_ModeCfg.KeepAlive.Interval={}&Intelbras_ModeCfg.KeepAlive.Path={}&Intelbras_ModeCfg.KeepAlive.TimeOut={}&Intelbras_ModeCfg.RemoteCheckTimeout={}".format(
                                        str(self.ip),
                                        str(device_mode),
                                        str(enable_keepalive),
                                        str(interval_keepalive),
                                        str(path_keepalive),
                                        str(timeout_keepalive),
                                        str(timeout_response),
                                    )
                
            result_events = requests.get(url_server_config, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            result_keepalive = requests.get(url_keepalive_config, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result_events.status_code != 200 or result_keepalive.status_code != 200:
                raise Exception()
            return str(result_events.text)
        except Exception:
            raise Exception("ERROR - During Set Online Mode")

    
    def _raw_to_dict(self, raw):
        data = {}
        for i in raw:
            if len(i) > 1:
                name = i[:i.find("=")]
                val = i[i.find("=") + 1:]
                try:
                    len(data[name])
                except:
                    data[name] = val
            else:
                data["NaN"] = "NaN"
        return data

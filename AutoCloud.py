#Code written by Dr.Ankur, for automating onworks session/s (free cloud computer)

import requests
import websocket
import base64
import io
import threading
import time
import ssl
import random
import string
import traceback

run_os = "ubuntu-20.04.1-desktop"
command_file = "commands.txt"

sessions = 1 #how many sessions to be started
start_from = 1 #start from session no.

gui = 0 #whether to capture gui or not

msg = ["" for _ in range(sessions*start_from)]
blob = ["" for _ in range(sessions*start_from)]
dimension_x, dimension_y = [0 for _ in range(sessions*start_from)], [0 for _ in range(sessions*start_from)]

canvas_width = 1024
canvas_height = 768

sync_first = [1 for _ in range(sessions*start_from)]
cursor_first = [1 for _ in range(sessions*start_from)]

intention_ws_close = [0 for _ in range(sessions*start_from)]

after_socket_28s = [time.time() for _ in range(sessions*start_from)]
after_socket_switch = [1 for _ in range(sessions*start_from)]

def start_session_outer(session):
    start_time = time.time()
    duration = 20 * 60 #Each session will last only 20mins.
    
    def start_session(session):
        try:
            global msg
            global blob
            global dimension_x, dimension_y
            global canvas
            global sync_first
            global curosr_first
            global after_socket_28s
            global after_socket_switch
            global intention_ws_close
            
            msg[session-1] = ""
            blob[session-1] = ""
            dimension_x[session-1], dimension_y[session-1] = 0, 0

            #canvas[session-1] = Image.new('RGB', (canvas_width, canvas_height), 'white')
            sync_first[session-1] = 1
            cursor_first[session-1] = 1
            
            intention_ws_close[session-1] = 0
            
            after_socket_28s[session-1] = time.time()
            after_socket_switch[session-1] = 1

            
            username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

            url = f"https://www.onworks.net/community/user.php?username={username}"
            response = requests.get(url) #'onworks76'

            url2 = f"https://www.onworks.net/runos/create-os.php?v=1&service={response.text}&username={username}&app=null&os={run_os}"
            response2 = requests.get(url2) #'guest22\n\n\n'

            url3 = f"https://www.onworks.net/osessionx{response.text[7:]}/api/tokens"
            response3 = requests.post(url3,data=f'username={response2.text.strip()}&password=server01{response2.text.strip()[5:]}') #'{"authToken":"E32BF9452DA4D627435DB8BBE076AAE33FF21D765288E904E01DEF7156923DA8","username":"guest22","dataSource":"default","availableDataSources":["default"]}'
            
            url4 = f"https://www.onworks.net/osessionx{response.text[7:]}/api/session/data/default/connectionGroups/ROOT/tree?token={response3.json()['authToken']}"
            response4 = requests.get(url4)

            url5 = f"https://www.onworks.net/osessionx{response.text[7:]}/api/tokens"
            response5 = requests.post(url5,data=f'token={response3.json()["authToken"]}&username={response2.text.strip()}&password=server01{response2.text.strip()[5:]}')
            
            #websocket url
            url9 = f"wss://www.onworks.net/osessionx{response.text[7:]}/websocket-tunnel?token={response5.json()['authToken']}&GUAC_DATA_SOURCE=default&GUAC_ID=DEFAULT&GUAC_TYPE=c&GUAC_WIDTH=1800&GUAC_HEIGHT=726&GUAC_DPI=144&GUAC_AUDIO=audio/L8&GUAC_AUDIO=audio/L16&GUAC_IMAGE=image/jpeg&GUAC_IMAGE=image/png&GUAC_IMAGE=image/webp"

            #print(url9)

            def update_gui(blob,x,y):
                global canvas
    
                image_data = base64.b64decode(blob)
                image = Image.open(io.BytesIO(image_data))
                canvas[session-1].save(f'image{session}.png')
                
                canvas[session-1] = Image.open(f"image{session}.png")
                canvas[session-1].paste(image, (int(x), int(y)), image.convert('RGBA'))
                canvas[session-1].save(f"image{session}.png")

            def on_message(ws, message):
                global intention_ws_close
                global after_socket_28s
                global after_socket_switch
                global msg
                global blob
                global dimension_x, dimension_y
                global sync_first
                global cursor_first
                
                if (time.time() - start_time) > duration:
                    ws.send('10.disconnect;')
                    intention_ws_close[session-1] = 1
                    ws.close()
                    return
                
                if after_socket_switch[session-1]:
                    url2 = f"https://www.onworks.net/community/user.php?username={username}&service={response.text}"
                    requests.get(url2)
                    url3 = f"https://www.onworks.net/runos/security.php?username={username}&service={response.text}"
                    requests.get(url3)
                    after_socket_switch[session-1] = 0
                    after_socket_28s[session-1] = time.time()
                else:
                    if (time.time() - after_socket_28s[session-1]) >= 28:
                        url4 = f"https://www.onworks.net/community/user.php?username={username}&service=service{response.text[7:]}"
                        requests.get(url4)
                        url5 = f"https://www.onworks.net/runos/security.php?username={username}&service=service{response.text[7:]}"
                        requests.get(url5)
                        after_socket_switch[session-1] = 1
                        
                        ws.send('5.mouse,3.500,3.312,1.1;5.mouse,3.500,3.312,1.0;')
                
                #if 'blob' not in message:
                    #formatted_time = time.strftime("%d-%m-%y %H:%M:%S", time.localtime())
                    #with open(f'log{session}.txt','a') as f:
                        #f.write('[' + formatted_time + ']: Received: ' + message + '\n\n')
                #print(f'Received: {message}')
                        
                msg[session-1] += message
                if msg[session-1].endswith(';'):
                    data = msg[session-1].split(';')
                    index = 0
                    for item in data:
                        if sync_first[session-1]:
                            if 'sync' in data[-2]:
                                #print('Sending 3 monkeys')
                                ws.send('9.clipboard,1.0,10.text/plain;')
                                ws.send('3.end,1.0;')
                                ws.send('5.audio,1.0,31.audio/L16;rate=44100,channels=2;')
                                sync_first[session-1] = 0
                        if 'Audio input unsupported' in item:
                            #print("Sending Audio end")
                            ws.send('3.end,1.0;')
                        if 'cursor' in data[-2]:
                            if cursor_first[session-1]:
                                #print("Sending Cursor OK")
                                ws.send('3.ack,1.1,2.OK,1.0;')
                                cursor_first[session-1] = 0
                        if 'sync' in item:
                            ws.send(item+';')
                            #print('Sending Item: ',item)
                        if gui:
                            with open('show_image.txt','r') as f:
                                show_image = f.read()
                            show_image = show_image.split('\n')
                            if 'image' in item:
                                dimension = item.split(',')
                                dimension_x[session-1], dimension_y[session-1] = dimension[-2].split('.')[-1], dimension[-1].split('.')[-1]
                            if 'blob' in item:
                                blob[session-1] += item.split('.')[-1]
                            if '.end' in item:
                                if str(session) in show_image:
                                    update_gui(blob[session-1],dimension_x[session-1],dimension_y[session-1])
                                dimension_x[session-1], dimension_y[session-1] = 0, 0
                                blob[session-1] = ""
                        index += 1
                    msg[session-1] = ""
                
            def on_error(ws, error):
                print(f'{session}: Websocket Error: ', error)
                #traceback.print_exc()
                #input()

            def on_close(ws, close_status_code, close_msg):
                global retry
                
                if not intention_ws_close[session-1]:
                    print(f"{session}: Closed connection: {close_status_code} - {close_msg}")
                    if retry[session-1] == 5:
                        print(f'{session}: Retried 5 time, but no response, exiting this session...')
                        return
                    print(f'{session}: Retrying...')
                    time.sleep(30)
                    retry[session-1] += 1
                    start_session(session)
                else:
                    print(f'{session}: Closed successfully!! ')
                    return

            def on_open(ws):
                formatted_time = time.strftime("%d-%m-%y %H:%M:%S", time.localtime(start_time))
                print(f'{formatted_time}: Session{session} started, {response.text}, {response2.text.strip()}')
                def send_msg(ws):
                    try:
                        while True:
                            url1 = f"https://www.onworks.net/osessionx{response.text[7:]}/api/session/tunnels/92718fb1-a41c-4a01-88e5-6b130c322b0a/activeConnection/connection/sharingProfiles?token={response5.json()['authToken']}"
                            requests.get(url1)
                            time.sleep(10)
                            #print('Sending nop')
                            #ws.send('3.nop;')
                            with open(command_file,'r') as f:
                                commands = f.read()
                            if commands:
                                session_in_command = ''
                                session_digits = [int(digit) for digit in str(session)]
                                for session_digit in session_digits:
                                    session_in_command += f'3.key,2.{ord(str(session_digit))},1.1;3.key,2.{ord(str(session_digit))},1.0; '
                                commands = commands.replace('3.key,3.115,1.1;3.key,3.115,1.0; 3.key,2.46,1.1;3.key,2.46,1.0; 3.key,3.115,1.1;3.key,3.115,1.0; 3.key,3.104,1.1;3.key,3.104,1.0;',f'3.key,3.115,1.1;3.key,3.115,1.0; {session_in_command}3.key,2.46,1.1;3.key,2.46,1.0; 3.key,3.115,1.1;3.key,3.115,1.0; 3.key,3.104,1.1;3.key,3.104,1.0;')
                                commands = commands.split("\n")
                                for command in commands:
                                    commands_key = command.split(" ")
                                    for command_key in commands_key:
                                        ws.send(command_key)
                                        time.sleep(0.1)
                                    #formatted_time = time.strftime("%d-%m-%y %H:%M:%S", time.localtime())
                                    #with open(f'log{session}.txt','a') as f:
                                        #f.write('[' + formatted_time + ']: Sent: ' + command + '\n\n')
                                    time.sleep(5)
                                #print(f'{session}: Command {commands} sent successfully!')
                                #with open('commands1.txt','w') as f:
                                    #f.write('')
                                break
                    except:
                        pass

                thread1 = threading.Thread(target=send_msg,args=(ws,))
                thread1.start()
                
            #websocket.enableTrace(True)

            ws = websocket.WebSocketApp(
                url9,
                on_message=on_message,
                on_error=on_error,
                on_open=on_open,
                on_close=on_close
            )

            ws.run_forever()
            #ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, proxy_type='http',http_proxy_host='127.0.0.1', http_proxy_port=f'8080')
            
        except Exception as e:
            global retry

            if retry[session-1] == 5:
                print(f'{session}: Retried 5 time, but no response, exiting this session...')
                return
            
            print(f'{session}: Got Error, restarting!!', e, f'response2: {response2.status_code} {response2.text}, response1: {response.status_code} {response.text}')
            time.sleep(15)
            retry[session-1] += 1
            start_session(session)
            
    start_session(session)

while True:
    retry = [0 for _ in range(sessions*start_from)]
    
    threads = []
    for session in range(start_from-1, sessions+(start_from-1)):
        thread = threading.Thread(target=start_session_outer,args=(session+1,))
        thread.start()
        threads.append(thread)
        #time.sleep(60)

    for thread in threads:
        thread.join()

    time.sleep(100)
    print('Restarting Another loop')

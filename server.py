import asyncio
import datetime
import json
from pymongo import MongoClient

from sanic import Sanic

client = MongoClient(port=27017, connect=False)
db = client.chatapp.chatapp


app = Sanic()

app.static('/', 'client.html', )

wss = []

@app.websocket('/ws')
async def chat_server(request, ws):
    while True:
        # msg = 'Hi!'
        # username = 'System'
        #
        # print('Sending data: {}'.format(msg))
        #
        # await ws.send(content_to_be_transferred(username, msg))

        if ws not in wss:
            wss.append(ws)

        data = await ws.recv()
        # update db

        username, text = data.split(',')

        datetimestamp = datetime.datetime.now().strftime('%Y-%M-%d %H:%m:%S')

        msg_info = [username, text, datetimestamp]

        """
        {
            'username': <username>, 
            'text_and_timestamp': [
                                    {"timestamp": <timestamp>, "msg": <msg>}
                                    ...
                                  ]
        }
        """

        db.find_one_and_update({'username': msg_info[0]},
                               {'$push': {'text_and_timestamp': {'timestamp': msg_info[2],
                                                                 'msg': msg_info[1]}
                                          }
                                }, upsert=True)

        for each_ws in wss:
            print(id(each_ws))
            await each_ws.send(content_to_be_transferred(msg_info))

        print('Username: {} Received Data:{}'.format(username, text))


def content_to_be_transferred(msg_info):
    return json.dumps(msg_info)



if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
#
# asyncio.ensure_future()

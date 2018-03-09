from sanic import Sanic
from sanic import response

app = Sanic()

@app.route('/')
async def hello(request):
    return response.json({'hello': "world"})

@app.route('/number/<integer_arg:int>')
async def integer_handler(request, integer_arg):
    return response.text('Integer - {}'.format(integer_arg))

@app.route('/person/<name:[A-z]+>')
async def person_handler(request, name):
    return response.text('Person - {}'.format(name))

@app.route('/folder/<folder_id:[A-z0-9]{0,4}>')
async def folder_handler(request, folder_id):
    return response.text('Folder - {}'.format(folder_id))

# Define the handler functions
async def handler1(request):
    return response.text('OK')

async def handler2(request, name):
    return response.text('Folder - {}'.format(name))

async def person_handler2(request, name):
    return response.text('Person - {}'.format(name))

# Add each handler function as a route
app.add_route(handler1, '/test')
app.add_route(handler2, '/folder/<name>')
app.add_route(person_handler2, '/person/<name:[A-z]>', methods=['GET'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, workers=2)


@app.websocket('/feed')
async def feed(request, ws):
    while True:
        data = 'hello'
        print('Sending data: ' + data)
        await ws.send(data)
        data = await ws.recv()
        print('Received Data: ' + data)


#
# import time
# import asyncio
#
#
# def is_prime(x):
#     return not any(x // i == x / i for i in range(x - 1, 1, -1))
#
#
# async def highest_prime_below(x):
#     print('Highest prime below %d' % x)
#     for y in range(x - 1, 0, -1):
#         if is_prime(y):
#             print('→ Highest prime below %d is %d' % (x, y))
#             return y
#         await asyncio.sleep(0.01)
#     return None
#
#
# async def main():
#     t0 = time.time()
#     await asyncio.wait([
#         highest_prime_below(100000),
#         highest_prime_below(10000),
#         highest_prime_below(1000)
#     ])
#     t1 = time.time()
#     print('Took %.2f ms' % (1000 * (t1 - t0)))
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()
#

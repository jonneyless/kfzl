import json
import re
from wsgiref.simple_server import make_server

from libs.api import editMessage
from libs.helper import userGQUnban


def callback(environ, response):
    response('200 OK', [('Content-Type', 'application/json')])

    method = environ.get('REQUEST_METHOD')
    if method == 'POST':
        requestBody = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))

        bodyData = requestBody.decode('utf-8')
        bodyData = re.sub('\'', '\"', bodyData)
        bodyData = json.loads(bodyData)

        if 'callback_data' not in bodyData or 'flag' not in bodyData:
            data = json.dumps([{'message': 'params error', 'data': []}])
            return [data.encode('utf-8')]

        params = json.loads(bodyData['callback_data'])
        if bodyData['flag'] != 1:
            params['text'] += '\n' + params['type'] + '：失败'
        else:
            params['text'] += '\n' + params['type'] + '：成功'

        if 'next' in params:
            if (params['next'] & 64) == 64:
                callbackData = {'message_id': params['message_id'], 'chat_id': params['chat_id'], 'text': params['text'], 'type': '公群解除屏蔽'}
                params['text'] += '\n公群解除屏蔽：处理中...'

                userGQUnban(params['user_id'], json.dumps(callbackData))

        editMessage({'message_id': params['message_id'], 'chat_id': params['chat_id'], 'text': params['text']})

    data = json.dumps([{'message': 'success', 'data': []}])
    return [data.encode('utf-8')]


if __name__ == "__main__":
    port = 8347
    httpd = make_server("0.0.0.0", port, callback)
    print("serving http on port {0}...".format(str(port)))
    httpd.serve_forever()

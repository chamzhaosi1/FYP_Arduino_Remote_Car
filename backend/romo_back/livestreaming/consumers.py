import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class CallConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        # response to client, that we are connected.
        self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

    def disconnect(self, close_code):
        # Leave room group
        print("Leave room group %s" %self.my_name)

        async_to_sync(self.channel_layer.group_discard)(
            self.my_name,
            self.channel_name
        )

        ## If get a notice like "21 of 50 channels over capacity in group"
        ## then we need adjust the maximum value of the channels layer in Django setting.py

    # Receive message from client WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        eventType = text_data_json['type']

        if eventType == 'login':
            name = text_data_json['data']['name']
            print("login %s" % name)

            # we will use this as room name as well
            self.my_name = name

            # Join room
            async_to_sync(self.channel_layer.group_add)(
                self.my_name,
                self.channel_name
            )

        if eventType == 'call':
            name = text_data_json['data']['name']
            print(self.my_name, "is calling", name)
            # print(text_data_json)

            # to notify the callee we sent an event to the group name
            # and their's groun name is the name
            async_to_sync(self.channel_layer.group_send)(
                name,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': self.my_name,
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'answer_call':
            # has received call from someone now notify the calling user
            # we can notify to the group with the caller name
            
            caller = text_data_json['data']['caller']
            # print(self.my_name, "is answering", caller, "calls.")

            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    'type': 'call_answered',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'ICEcandidate':
            user = text_data_json['data']['user']

            async_to_sync(self.channel_layer.group_send)(
                user,
                {
                    'type': 'ICEcandidate',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )
        if eventType == 'refreshSession':
            callee = text_data_json['data']['client']
        
            # Notify other users in the group that this user has left
            async_to_sync(self.channel_layer.group_send)(
                callee,
                {
                    'type': 'refreshSession',
                    'data': {
                        'username': self.my_name
                    }
                }
            )

        if eventType == 'stopSession':
            callee = text_data_json['data']['client']
            print("close %s" ,self.my_name)
            
            # Notify other users in the group that this user has left
            async_to_sync(self.channel_layer.group_send)(
                callee,
                {
                    'type': 'endSession',
                    'data': {
                        'username': self.my_name
                    }
                }
            )  

            self.close()


    def call_received(self, event):
        # print(event)
        print('Call received by ', self.my_name )
        self.send(text_data=json.dumps({
            'type': 'call_received',
            'data': event['data']
        }))


    def call_answered(self, event):
        # print(event)
        print(self.my_name, "'s call answered")
        self.send(text_data=json.dumps({
            'type': 'call_answered',
            'data': event['data']
        }))


    def ICEcandidate(self, event):
        self.send(text_data=json.dumps({
            'type': 'ICEcandidate',
            'data': event['data']
        }))


    def endSession(self, event):
        print("send ending")
        self.send(text_data=json.dumps({
            'type': 'end_session',
            'data': event['data']
        }))

    def refreshSession(self, event):
        print("refresh page")
        self.send(text_data=json.dumps({
            'type': 'refresh_session',
            'data': event['data']
        }))
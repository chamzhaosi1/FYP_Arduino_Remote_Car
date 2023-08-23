import json
import random
import time
from datetime import datetime
import serial
import io

from flask import Flask, Response, render_template, stream_with_context

application = Flask(__name__)
# random.seed()  # Initialize the random number generator
ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)
print(ser.name)         # check which port was really used


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/chart-data')
def chart_data():
    def serial_data():
        prevV = 0
        count_same = 0

        while True:
            line = ser.readline()

            try :
                string = line.decode('utf-8').strip()
                # print(string)
                if len(string.split(",")) == 2:
                    target = string.split(",")[0]
                    current = string.split(",")[1]
                    
                    if isinstance(target, float):
                        if prevV != target:
                            # print(target)
                            print(target)
                            print(current)
                            # value1 = target
                            json_data = json.dumps(
                                # {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
                                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'value1': target,
                                'value2': current})
                            yield f"data:{json_data}\n\n"
                            count_same = 0
                            prevV = target
                            time.sleep(0.05)
                        # else:
                        #     count_same += 1
                        #     if count_same == 30:
                        #         time.sleep(5)
    
            except UnicodeDecodeError:
                pass

    response = Response(stream_with_context(serial_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == '__main__':
    application.run(debug=True, threaded=True)
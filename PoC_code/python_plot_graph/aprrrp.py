import plotly.graph_objects as go
import serial
import io
import numpy as np
from array import array
from flask import Flask, render_template

app = Flask(__name__)

ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)
print(ser.name)         # check which port was really used


# while True:
#     line = ser.readline()
#     string = line.decode('utf-8').strip()
#     print(string)

# ser.close() 

@app.route("/")
def plot():
    # Generate some data
    # x = [1, 2, 3, 4, 5]
    # y = [10, 20, 30, 40, 10]

    n = 255  # set the length of the array
    step = 15  # set the step size

    x = []
    y = np.arange(15, n+1, step)
    print(y)

    count = 0 
    while True:
        line = ser.readline()
        string = line.decode('utf-8').strip()
        print(string)
        x.append(string.split(" ")[0])
        count += 1

        if count == 500:
            break


    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y))

    # Return the plotly plot as an html div
    plot_div = fig.to_html(full_html=False)

    # Render the template with the plot data
    print(x)
    print(y)
    return render_template('plot.html', plot_div=plot_div)


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000) 
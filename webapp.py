from flask import Flask, render_template, request, redirect, flash, current_app as app
import sys, os, subprocess, time, json
import pyBluezConnector
app = Flask(__name__)

@app.route('/')
@app.route('/main/', methods = ['POST', 'GET'])
def main():
    init()
    connect()
    return render_template('main.html')

@app.route('/connected/', methods = ['POST', 'GET'])
def connectedDevices():
#    filename = os.path.join(app.static_folder, 'message.json')
#    with open(filename) as file:
#        data = json.load(file)
    with open("/home/pi/.config/meshctl/prov_db.json", 'r') as file:
        data = json.load(file)
    return render_template('connected.html', posts=data)

@app.route('/on/<unicastAddress>', methods = ['GET'])
def switchOnApp(unicastAddress):
    print("on : " + unicastAddress)
    switchOn(unicastAddress)
    return redirect('/connected', code=302)

@app.route('/off/<unicastAddress>', methods = ['GET'])
def switchOffApp(unicastAddress):
    print("off : " + unicastAddress)
    switchOff(unicastAddress)
    return redirect('/connected', code=302)

@app.route('/status/<unicastAddress>', methods = ['GET'])
def statusRequest(unicastAddress):
    #responseCode = "off"
    responseCode = lightStat(unicastAddress)
    return render_template('status.html', status = responseCode, uniAddress = unicastAddress)

@app.route('/devices/add/<uidd>', methods = ['POST', 'GET'])
def provision(uidd):
    addDev(uidd)
    #filename = os.path.join(app.static_folder, 'message.json')
    #with open(filename) as file:
    #    data = json.load(file)
    with open("/home/pi/.config/meshctl/prov_db.json", 'r') as file:
        data = json.load(file)
    return render_template('provision.html', uidd=uidd, posts=data)

@app.route('/grouped/<uidd>', methods = ['POST', 'GET'])
def addToGroup(uidd):
    if request.method == 'POST':
        result = request.form
        deviceType = request.form['options']
        group(result['uni'], result['group'], deviceType)
        return render_template("result.html", result = result, device = uidd)

@app.route('/devices/', methods = ['POST', 'GET'])
def remove():
    filename = os.path.join(app.static_folder, 'message.json')
    with open(filename) as file:
        data = json.load(file)
    return render_template('remove.html', posts=data)

@app.route('/remove/<uidd>', methods = ['POST', 'GET'])
def removeUidd(uidd):
    removeDev(uidd)
    return redirect('/devices', code=302)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


from flask import render_template, url_for, flash, redirect, abort, request, jsonify, make_response
#from flaskblog.models import User,Post
#from flaskblog.forms import RegistrationForm, LoginForm,PostForm
from flaskblog import app
from flask_login import login_user, current_user, logout_user, login_required
import requests
import datetime
from flaskblog import pool


def getCountryCases(country):
    url = "https://covid-193.p.rapidapi.com/statistics"
    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "4d9e908890mshba2fda3a9dfb5dfp11e63bjsndf1d7a33c10c"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    for obj in data["response"]:
        if obj["country"] == country:
            cases = obj["cases"]
            break
    return cases


def getWorldCases(date):
    url = "https://covid-19-statistics.p.rapidapi.com/reports/total"
    querystring = {"date": f"{date}"}
    headers = {
        'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
        'x-rapidapi-key': "4d9e908890mshba2fda3a9dfb5dfp11e63bjsndf1d7a33c10c"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    return response.json()["data"]


def main():
    todayDate = datetime.datetime.date(datetime.datetime.utcnow())
    yestDate = todayDate - datetime.timedelta(days=1)
    print(f"Covid-19 Cases updated as of {yestDate} :")

    worldCases = getWorldCases(yestDate)
    print(
        f"World: \nTotal Confirmed: {worldCases['confirmed']}, New Confirmed: {worldCases['confirmed_diff']}, Death Toll: {worldCases['deaths']}, New Deaths: {worldCases['deaths_diff']}")

    country = "India"
    cases = getCountryCases(country)
    print(
        f"Cases in {country}: \nTotal: {cases['total']}, New: {cases['new']}, Active: {cases['active']}, Critical: {cases['critical']}, Recovered: {cases['recovered']}")
    return(worldCases['confirmed'], worldCases['confirmed_diff'], worldCases['deaths'], worldCases['deaths_diff'], cases['total'], cases['new'], cases['active'], cases['recovered'])


var1, var2, var3, var4, var5, var6, var7, var8 = main()


pool.main()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', var1=int(var1), var2=int(var2), var3=int(var3), var4=int(var4), var5=int(var5), var6=int(var6), var7=int(var7), var8=int(var8))


@app.route('/ngoconnect')
@app.route('/ngo')
def ngo():
    return render_template('ngo.html')


@app.route('/cry')
def cry():
    return render_template('cry.html')


@app.route('/giveindia')
def giveindia():
    return render_template('giveindia.html')


@app.route('/goonj')
def goonj():
    return render_template('goonj.html')


@app.route('/helpageindia')
def helpageindia():
    return render_template('helpageindia.html')


@app.route('/nanhikali')
def nanhikali():
    return render_template('nanhikali.html')


@app.route('/smile')
def smile():
    return render_template('smile.html')   


@app.route('/screeningtool')
def screeningtool():
    resp = make_response(render_template('screeningtool.html'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/pooling')
def pooling():
    Pools = pool.main()
    user_details = pool.fetch_pool_batch(Pools, 34631)
    # print(user_details)
    return render_template('pooling.html', user_details=user_details)


@app.route('/stageonedata', methods=['POST'])
def stageonedata():
    input_json = request.get_json(force=True)
    print("RecievedData", input_json)
    return jsonify({"registeredData": True})

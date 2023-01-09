from flask import Flask, render_template, redirect, url_for
from app import app

@app.route('/direction/fasad/')
def fasad():
    return redirect(url_for('catid', url='vyveski'))


@app.route('/direction/pos/')
@app.route('/direction/opera/')
def pos():
    return redirect(url_for('catid', url='poligrafija'))


@app.route('/direction/iss/')
def iss():
    return redirect(url_for('catid', url='stendy-i-tablichki'))


@app.route('/direction/format/')
def format():
    return redirect(url_for('catid', url='shirokoformatnaja-pechat'))


@app.route('/direction/baget/')
def baget():
    return redirect(url_for('catid', url='dopolnitelnye-uslugi'))


@app.route('/direction/laser-graver/')
def lazer():
    return redirect(url_for('catid', url='lazernaja-rezka'))


@app.route('/direction/design/')
def design():
    return redirect(url_for('catid', url='dizajn'))


@app.route('/direction/fest/')
def fest():
    return redirect(url_for('catid', url='brendirovanie'))


@app.route('/direction/stamp/')
def stamp():
    return redirect(url_for('product', url_cat='dopolnitelnye-uslugi', url='shtampy-i-pechati'))


@app.route('/direction/suvenir/')
def suvenir():
    return redirect(url_for('product', url_cat='lazernaja-rezka', url='lazernaja-rezka-suvenirov'))


@app.route('/portfolio/')
def portfolio():
    return redirect(url_for('cases'))


@app.route('/about_us/')
@app.route('/partnyory/')
@app.route('/regalii/')
@app.route('/customers/')
def about_us():
    return redirect(url_for('aboutus'))


@app.route('/kontakty/')
def kontakty():
    return redirect(url_for('contacts'))





















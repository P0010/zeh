from flask import Flask, render_template, request, url_for, redirect, flash
import datetime
import asyncio
from flask_login import login_user, login_required, logout_user
import os
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


from app import app, db, allowed_file
from app.models_main import Category, Product, Images, Price, Suggestion, Social, Index_product, User
from app.models_cases import Cases, CasesTitle, Contacts, ContactsTitle, Aboutus, Clients
from app.telegr import somefunc
from app.mail import send_email

now = datetime.datetime.now()  # Дата



@app.route('/', methods = ['POST', 'GET'])
def index():
    categories = Category.query.filter(Category.name=='root').first()
    ind = Social.query.first()
    ind_pr = Index_product.query.all()
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        topic = request.form['topic']
        if phone != '':
            asyncio.run(somefunc(name, phone, topic))
            send_email(name, phone, topic)
            client = Clients(name=name, phone=phone, site=topic)
            try:
                db.session.add(client)
                db.session.commit()
                return render_template('index.html', happy='Данные успешно отправленны', categories=categories, ind=ind, ind_pr=ind_pr, now=now)
            except:
                return 'Произошла ошибка'
        else:
            return render_template('index.html', error='Пожалуйста заполните все формы', categories=categories, ind=ind, ind_pr=ind_pr, now=now)
    else:
        return render_template('index.html', categories=categories, ind=ind, ind_pr=ind_pr, now=now)


@app.route('/catalog', methods = ['POST', 'GET'])
def catalog():
    ind = Social.query.first()
    categories = Category.query.filter(Category.name=='root').first()
    contacts = Contacts.query.all()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        topic = request.form['topic']
        if phone != '':
            asyncio.run(somefunc(name, phone, topic))
            send_email(name, phone, topic)
            client = Clients(name=name, phone=phone, site=topic)
            try:
                db.session.add(client)
                db.session.commit()
                return render_template('catalog.html', happy='Данные успешно отправленны', categories=categories, ind=ind, now=now, contacts=contacts )
            except:
                return 'Произошла ошибка'
        else:
            return render_template('catalog.html', happy='Пожалуйста заполните все формы', categories=categories, ind=ind, now=now, contacts=contacts)
    else:
        return render_template('catalog.html', categories=categories, ind=ind, now=now, contacts=contacts)



@app.route('/category/<string:url>', methods=['POST', 'GET'])
def catid(url):
    ind = Social.query.first()
    categories = Category.query.filter(Category.name=='root').first()
    catid = Category.query.filter_by(url=url).first()
    contacts = Contacts.query.all()
    print('help')
    print(catid)
    red = catid.path_to_root()  
    
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        topic = request.form['topic']
        if phone != '':
            asyncio.run(somefunc(name, phone, topic))
            send_email(name, phone, topic)
            client = Clients(name=name, phone=phone, site=topic)
            try:
                db.session.add(client)
                db.session.commit()
                return render_template('catid.html', happy='Данные успешно отправленны', catid=catid, red=red, categories=categories, ind=ind, now=now, contacts=contacts)
            except:
                return 'Произошла ошибка'
        else:
            return render_template('catid.html', error='Пожалуйста заполните все формы', catid=catid, red=red, categories=categories, ind=ind, now=now, contacts=contacts)
    return render_template('catid.html', catid=catid, red=red, categories=categories, ind=ind, now=now, contacts=contacts)


@app.route('/<string:url_cat>/<string:url>', methods = ['POST', 'GET'])
def product(url_cat, url):
    ind = Social.query.first()
    categories = Category.query.filter(Category.name=='root').first()
    catid = Category.query.filter_by(url=url_cat).first()
    red = catid.path_to_root()
    contacts = Contacts.query.all()

    bread = Product.query.filter_by(url=url).first()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        topic = request.form['topic']
        if phone != '':
            asyncio.run(somefunc(name, phone, topic))
            send_email(name, phone, topic)
            client = Clients(name=name, phone=phone, site=topic)
            try:
                db.session.add(client)
                db.session.commit()
                return render_template('product.html', happy='Данные успешно отправленны', red=red, catid=catid, bread=bread, categories=categories, ind=ind, now=now, contacts=contacts)
            except:
                return 'Произошла ошибка'
        else:
            return render_template('product.html', error='Пожалуйста заполните все формы', red=red, catid=catid, bread=bread, categories=categories, ind=ind, now=now, contacts=contacts)
    return render_template('product.html', red=red, catid=catid, bread=bread, categories=categories, ind=ind, now=now, contacts=contacts)


@app.route('/cases', methods = ['POST', 'GET'])
def cases():
    cases = Cases.query.all()

    ind = Social.query.first()
    categories = Category.query.filter(Category.name=='root').first()
    contacts = Contacts.query.all()

    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        topic = request.form['topic']
        asyncio.run(somefunc(name, phone, topic))
        send_email(name, phone, topic)
        client = Clients(name=name, phone=phone, site=topic)
        try:
            db.session.add(client)
            db.session.commit()
            return render_template('cases.html', happy='Данные успешно отправленны', cases=cases, ind=ind, categories=categories, now=now, contacts=contacts)
        except:
            return 'Произошла ошибка'
    else:
        case_t = CasesTitle.query.filter_by(id=1).first()
        return render_template('cases.html', cases=cases, ind=ind, categories=categories, now=now, contacts=contacts, case_t=case_t)


@app.route('/case/<string:url_case>', methods = ['POST', 'GET'])
def case(url_case):
    case = Cases.query.filter_by(url=url_case).first()

    ind = Social.query.first()
    categories = Category.query.filter(Category.name=='root').first()
    contacts = Contacts.query.all()

    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        topic = request.form['topic']
        asyncio.run(somefunc(name, phone, topic))
        send_email(name, phone, topic)
        client = Clients(name=name, phone=phone, site=topic)
        try:
            db.session.add(client)
            db.session.commit()
            return render_template('case.html', happy='Данные успешно отправленны', case=case, ind=ind, categories=categories, now=now, contacts=contacts)
        except:
            return 'Произошла ошибка'
    else:
        return render_template('case.html', case=case, ind=ind, categories=categories, now=now, contacts=contacts)


@app.route('/contacts', methods = ['POST', 'GET'])
def contacts():

    ind = Social.query.first()
    categories = Category.query.filter(Category.name=='root').first()
    contacts = Contacts.query.all()

    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        topic = request.form['topic']
        asyncio.run(somefunc(name, phone, topic))
        send_email(name, phone, topic)
        client = Clients(name=name, phone=phone, site=topic)
        try:
            db.session.add(client)
            db.session.commit()
            return render_template('contacts.html', happy='Данные успешно отправленны', ind=ind, categories=categories, now=now, contacts=contacts)
        except:
            return 'Произошла ошибка'
    else:
        contact_t = ContactsTitle.query.filter_by(id=1).first()
        return render_template('contacts.html', ind=ind, categories=categories, now=now, contacts=contacts, contact_t=contact_t)


@app.route('/aboutus', methods = ['POST', 'GET'])
def aboutus():
    ind = Social.query.first()
    categories = Category.query.filter(Category.name=='root').first()
    contacts = Contacts.query.all()
    ab = Aboutus.query.filter_by(id=1).first()
    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        topic = request.form['topic']
        asyncio.run(somefunc(name, phone, topic))
        send_email(name, phone, topic)
        client = Clients(name=name, phone=phone, site=topic)
        try:
            db.session.add(client)
            db.session.commit()
            return render_template('aboutus.html', categories=categories, ind=ind, contacts=contacts, now=now, ab=ab, happy='Данные успешно отправленны')
        except:
            return 'Произошла ошибка'
    else:
        return render_template('aboutus.html', categories=categories, ind=ind, contacts=contacts, now=now, ab=ab)

@app.route('/search', methods = ['POST', 'GET'])
def w_search():

    ind = Social.query.first()
    categories = Category.query.filter(Category.name=='root').first()
    contacts = Contacts.query.all()

    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        topic = request.form['topic']
        asyncio.run(somefunc(name, phone, topic))
        send_email(name, phone, topic)
        client = Clients(name=name, phone=phone, site=topic)
        try:
            db.session.add(client)
            db.session.commit()
            return render_template('search.html', categories=categories, ind=ind, contacts=contacts, now=now, happy='Данные успешно отправленны')
        except:
            return 'Произошла ошибка'
    else:
        keyword = request.args.get('search')

        keyword = keyword.capitalize() # type: ignore 
        keywordlower = keyword.lower() # type: ignore 

        category = Category.query.msearch(keyword, fields=['name'], limit=10)
        product = Product.query.msearch(keyword, fields=['name'], limit=10)

        productlower = Product.query.msearch(keywordlower, fields=['name'], limit=10)
        categorylower = Category.query.msearch(keywordlower, fields=['name'], limit=10)

        return render_template('search.html', category=category, categorylower=categorylower, product=product, productlower=productlower,  ind=ind, categories=categories, now=now, contacts=contacts, keyword=keyword)

@app.route('/politica')
def politica():
    ind = Social.query.first()
    categories = Category.query.filter(Category.name=='root').first()
    return render_template('politica.html', categories=categories, ind=ind, now=now)







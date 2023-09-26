from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user
import os
from werkzeug.security import check_password_hash, generate_password_hash
from transliterate import slugify

from app import app, db, allowed_file
from app.models_cases import Contacts, ContactsTitle, Partners, Phone, Cases, CasesTitle, Images_cases, Keys_cases, Images_key_cases, Aboutus, Foundation, Equipment, Employees, Awards, Clients
from app.models_main import Category, Product
from app.new_image import NewCaseImage, NewCaseKey
import uuid


# Функции проверки кириллиц
def hascyr(s):
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(s.lower()) != set()

#  Новый кейс

@app.route('/admin/new_cases', methods = ['POST', 'GET'])
@login_required
def new_cases():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        title2 = request.form['title2']
        description = request.form['description']
        if hascyr(title)==True:
            url = slugify(title)
        else:
            url = title

        case = Cases(title=title, url=url, intro=intro, title2=title2, description=description)


        # Функция загрузки image

        file = request.files['file']
        alt = request.form['alt']
        img = NewCaseImage(file, alt, url) 
        img = img.rec_2()

        case.image.append(img) # Подключиаем к таблице Product


        # Функция Keys

        title1 = request.form['title1']
        text1 = request.form['text1']
        keys = Keys_cases(title=title1, text=text1)


        # Функция загрузки image key

        file1 = request.files['file1']
        alt1 = request.form['alt1']
        img1 = NewCaseKey(file1, alt1, url)
        img_1 = img1.rec_2()

        file2 = request.files['file2']
        alt2 = request.form['alt2']
        img2 = NewCaseKey(file2, alt2, url)
        img_2 = img2.rec_2()

        file3 = request.files['file3']
        alt3 = request.form['alt3']
        img3 = NewCaseKey(file3, alt3, url)
        img_3 = img3.rec_2()

        
        keys.images.extend([img_1, img_2, img_3])
        case.keys.append(keys)


         #    Функция услуги
        uslugi = request.form.getlist("uslugi")
        if uslugi != []:
            for usl in uslugi:
                usl2 = Product.query.filter_by(id=usl).first()
                case.uslugi.append(usl2)

        try:
            db.session.add(case)
            db.session.commit()  
            # return redirect('/admin/new_cases')
            return redirect(url_for('update_case', id=case.id))
        except:
            return 'Произошла ошибка'
    else:
        cases = Cases.query.all()
        categories = Category.query.filter(Category.name=='root').first()
        
        case_t = CasesTitle.query.filter_by(id=1).first()
        return render_template('new_cases.html', categories=categories, cases=cases, case_t=case_t)

# Case_title

@app.route('/admin/case_title', methods = ['POST', 'GET'])
@login_required
def case_title():
    case = CasesTitle.query.filter_by(id=1).first() 
    if request.method == "POST":
        case.title = request.form['title']
        case.description = request.form['description']
        try:
            db.session.add_all([case])
            db.session.commit()
            return redirect(url_for('new_cases'))
        except:
            return 'Произошла ошибка'
    else:
        return 'ок'

# Редактировать кейс
@app.route('/admin/s/update_case/<int:id>', methods = ['POST', 'GET'])
@login_required
def update_case(id):
    case = Cases.query.filter_by(id=id).first()
    categories = Category.query.filter(Category.name=='root').first()
    if request.method == 'POST':
        pass
    else:
        return render_template('update_case.html', case=case, categories=categories)

@app.route('/delete/case/<int:id>')
@login_required
def case_delete(id):
    case = Cases.query.filter_by(id=id).first()
    try:
        if case.image != []:
            for image in case.image:
                path = app.config['UPLOAD_FOLDER'] + 'cases/'
                if os.path.isfile(path + image.filename) == True:
                    os.remove(path + image.filename)

        if case.keys != []:
            for key in case.keys:
                for image in key.images:
                    path = app.config['UPLOAD_FOLDER'] + 'ca_keys/'
                    if os.path.isfile(path + image.filename) == True:
                        os.remove(path + image.filename)

        db.session.delete(case)
        db.session.commit()
        return redirect('/admin/new_cases')
    except:
        return "При удалении произошла ошибка"

# Контакты title 

@app.route('/admin/contact_title', methods = ['POST', 'GET'])
@login_required
def contact_title():
    contact = ContactsTitle.query.filter_by(id=1).first() 
    if request.method == "POST":
        contact.title = request.form['title']
        contact.description = request.form['description']
        try:
            db.session.add_all([contact])
            db.session.commit()
            return redirect(url_for('new_contact'))
        except:
            return 'Произошла ошибка'
    else:
        return 'ок'
# Контакты

@app.route('/admin/new_contact', methods = ['POST', 'GET'])
@login_required
def new_contact():
    if request.method == 'POST':
        address = request.form['address']
        name = request.form['name']
        email = request.form['email']
        script = request.form['script']
        weekdays = request.form['weekdays']
        saturday = request.form['saturday']
        sunday = request.form['sunday']
        contact = Contacts(address=address, name=name, email=email, script=script, weekdays=weekdays, saturday=saturday, sunday=sunday)
        
        # функция сбор телефона

        phones = request.form.getlist('phone')
        for phone in phones:
            phonex = Phone(phone=phone)
            contact.phones.append(phonex)

        try:
            db.session.add_all([contact])
            db.session.commit()
            return redirect('/admin/new_contact')
        except: 
            return 'Произошла ошибка'
    else:
        contact_t = ContactsTitle.query.filter_by(id=1).first()
        contacts = Contacts.query.all()
        return render_template('new_contacts.html', contacts=contacts, contact_t=contact_t)

        
# Редактировать контакты

@app.route('/admin/update_contact/<int:id>', methods = ['POST', 'GET'])
@login_required
def update_contact(id):
    contact = Contacts.query.filter_by(id=id).first()
    if request.method == 'POST':
        contact.address = request.form['address']
        contact.name = request.form['name']
        contact.email = request.form['email']
        contact.script = request.form['script']
        contact.weekdays = request.form['weekdays']
        contact.saturday = request.form['saturday']
        contact.sunday = request.form['sunday']
        try:
            db.session.add(contact)
            db.session.commit()
            return render_template('update_contact.html', contact=contact)
        except:
            return 'Произошла ошибка'
    else:
        return render_template('update_contact.html', contact=contact)


# Добавить телефон

@app.route('/admin/new_phone/<int:id>', methods = ['POST', 'GET'])
@login_required
def new_phone(id):
    contact = Contacts.query.filter_by(id=id).first()
    phones = request.form.getlist('phone')
    for phone in phones:
        phonex = Phone(phone=phone)
        contact.phones.append(phonex)

    try:
        db.session.add_all([contact])
        db.session.commit()
        return redirect(url_for('update_contact', id=id))
    except: 
        return 'Произошла ошибка'


# Удалить телефон

@app.route('/delete/phone/<int:id>')
@login_required
def phone_delete(id):
    phone = Phone.query.filter_by(id=id).first()
    try:
        db.session.delete(phone)
        print(phone.contact.id)
        db.session.commit()
        return redirect(url_for('update_contact', id=phone.contact.id))
    except:
        return "При удалении произошла ошибка"

# Редактировать телефоны

@app.route('/admin/update_phone/<int:id>', methods = ['POST', 'GET'])
@login_required
def update_phone(id):
    contact = Contacts.query.filter_by(id=id).first()

    phone = request.form.getlist('phone')

    uniq_and_fifa = dict(zip(contact.phones, phone))

    for key,value in uniq_and_fifa.items():
        print(key.phone)
        print(value)
        croc = Phone.query.filter_by(phone=key.phone).first()
        croc.phone = value

    try:
        db.session.commit()
        return redirect(url_for('update_contact', id=id))
    except:
        return "Произошла ошибка"


# Удалить контакт

@app.route('/delete/contact/<int:id>')
@login_required
def contact_delete(id):
    contact = Contacts.query.filter_by(id=id).first()
    try:
        db.session.delete(contact)
        db.session.commit()
        return redirect('/admin/new_contact')
    except:
        return "При удалении произошла ошибка"







# Заполнить данные "О нас"

@app.route('/admin/update_aboutus', methods=['POST', 'GET'])
@login_required
def update_aboutus():
    ab = Aboutus.query.filter_by(id=1).first()
    if request.method == "POST":
 
        if ab != None:
            ab.branches = request.form['branches']
            ab.num_employees = request.form['num_employees']
            ab.title = request.form['title']
            ab.description = request.form['description']

            try:
                db.session.add(ab)
                db.session.commit()
                return redirect('/admin/update_aboutus')
            except:
                return 'Произошла ошибка1'

        else:
            branches = request.form['branches']
            num_employees = request.form['num_employees']
            aboutus = Aboutus(branches=branches, num_employees=num_employees)

            try:
                db.session.add(aboutus)
                db.session.commit()
                return redirect('/admin/update_aboutus')
            except:
                return 'Произошла ошибка2'

    else:
        return render_template('update_aboutus.html', ab=ab)

# Загрузить image Foundation

@app.route('/image_upload', methods=['POST', 'GET'])
@login_required
def image_upload():
    ab = Aboutus.query.filter_by(id=1).first()
    name = request.form['foundation']
    file = request.files['file']

    file_name = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    foundation2 = Foundation(name=name, filename=file_name)

    ab.foundation.append(foundation2)

    try:
        db.session.add(ab)
        db.session.commit()
        return redirect('/admin/update_aboutus')
    except:
        return 'Произошла ошибка2'

# Удалить Image Foundation

@app.route('/del_image_foundation/<int:id>')
@login_required
def del_image_foundation(id):
    foundation = Foundation.query.filter_by(id=id).first()
    try:
        db.session.delete(foundation)
        db.session.commit()
        return redirect('/admin/update_aboutus')
    except:
        return "При удалении произошла ошибка"

# Добвать оборудование equipments

@app.route('/equipments', methods=['POST', 'GET'])
@login_required
def equipments():
    ab = Aboutus.query.filter_by(id=1).first()
    equipments = request.form['equipments']
    ddf = Equipment(equip=equipments)
    ab.equipment.append(ddf)
    try:
        db.session.add(ab)
        db.session.commit()
        return redirect('/admin/update_aboutus')
    except:
        return 'Произошла ошибка'

# Удалить Оборудование (equipment)

@app.route('/equipment_delete/<int:id>')
@login_required
def equipment_delete(id):
    equipmnet = Equipment.query.filter_by(id=id).first()
    try:
        db.session.delete(equipmnet)
        db.session.commit()
        return redirect('/admin/update_aboutus')
    except:
        return "При удалении произошла ошибка"


# Загрузить image Сотрудники (Employees)

@app.route('/image_upload_employees', methods=['POST', 'GET'])
@login_required
def image_upload_employees():
    ab = Aboutus.query.filter_by(id=1).first()
    name = request.form['employees']
    file = request.files['file']

    file_name = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    employees2 = Employees(name=name, filename=file_name)

    ab.employees.append(employees2)

    try:
        db.session.add(ab)
        db.session.commit()
        return redirect('/admin/update_aboutus')
    except:
        return 'Произошла ошибка2'

# Удалить Сотрудника (Employess)

@app.route('/del_image_employees/<int:id>')
@login_required
def del_image_employees(id):
    employees = Employees.query.filter_by(id=id).first()
    try:
        db.session.delete(employees)
        db.session.commit()
        return redirect('/admin/update_aboutus')
    except:
        return "При удалении произошла ошибка"


# Загрузить image Награды (Awards)

@app.route('/image_upload_award', methods=['POST', 'GET'])
@login_required
def image_upload_awards():
    ab = Aboutus.query.filter_by(id=1).first()
    file = request.files['file']

    file_name = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    awards2 = Awards(filename=file_name)

    ab.awards.append(awards2)

    try:
        db.session.add(ab)
        db.session.commit()
        return redirect('/admin/update_aboutus')
    except:
        return 'Произошла ошибка2'

# Удалить Награды (Awards)

@app.route('/del_image_award/<int:id>')
@login_required
def del_image_awards(id):
    awards = Awards.query.filter_by(id=id).first()
    try:
        db.session.delete(awards)
        db.session.commit()
        return redirect('/admin/update_aboutus')
    except:
        return "При удалении произошла ошибка"


# Загрузить партнёров (partners)

@app.route('/image_upload_partners', methods=['POST', 'GET'])
@login_required
def image_upload_partners():
    ab = Aboutus.query.filter_by(id=1).first()
    file = request.files['file']

    extension = file.filename.split(".")[1].lower()
    file_name = uuid.uuid4().hex+'.'+extension
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    partners2 = Partners(filename=file_name)

    ab.partners.append(partners2)

    try:
        db.session.add(ab)
        db.session.commit()
        return redirect('/admin/update_aboutus')
    except:
        return 'Произошла ошибка2'


# Удалить партнёров (partners)

@app.route('/del_image_parners/<int:id>')
@login_required
def del_image_partners(id):
    partners = Partners.query.filter_by(id=id).first()
    
    path = app.config['UPLOAD_FOLDER']+'/'
    if os.path.isfile(path + partners.filename) == True:
        os.remove(path + partners.filename)
        
    try:
        db.session.delete(partners)
        db.session.commit()
        return redirect('/admin/update_aboutus')
    except:
        return "При удалении произошла ошибка"


# Клиенты

@app.route('/client')
@login_required
def client():
    clients = Clients.query.order_by(Clients.date.asc()).all()
    return render_template('client.html', clients=clients)


# Удалить Клиента 

@app.route('/client_del/<int:id>')
@login_required
def client_del(id):
    client = Clients.query.filter_by(id=id).first()
    try:
        db.session.delete(client)
        db.session.commit()
        return redirect('/client')
    except:
        return "При удалении произошла ошибка"




# Редактировать кейс (+ заголовок, +intro, +title2, description)

@app.route('/st/case_reride/<int:id>', methods=['POST', 'GET'])
@login_required
def case_reride(id):
    case = Cases.query.filter_by(id=id).first()
    case.title = request.form['title']
    if hascyr(case.title)==True:
        case.url = slugify(case.title)
    else:
        case.url = case.title
    case.intro = request.form['intro']
    case.title2 = request.form['title2']
    case.description = request.form['description']

    try:
        db.session.add(case)
        db.session.commit()
        return redirect(url_for('update_case', id=case.id))
    except:
        return 'Произошла ошибка'


# Загрузить Image Case

@app.route('/img/case_image_upload/<int:id>', methods=['POST', 'GET'])
@login_required
def case_image_upload(id):
    case = Cases.query.filter_by(id=id).first()

    # Функция загрузки image
    file = request.files["file"]
    alt = request.form["alt"]
    img = NewCaseImage(file, alt, case.url) 
    img = img.rec_2()
    
    case.image.append(img) # Подключиаем к таблице Case

    try:
        db.session.add(case)
        db.session.commit()
        return redirect(url_for('update_case', id=case.id))
    except:
        return 'Произошла ошибка'


# Удалить Image Case

@app.route('/r/del_image_case/<int:id>')
@login_required
def del_image_case(id):
    case_image = Images_cases.query.filter_by(id=id).first()

    print(case_image.case_id)

    count = Cases.query.filter_by(id=case_image.case_id).first()
    try:
        coun = 0
        for co in count.image:
            coun += 1

        if coun > 1:
            path = app.config['UPLOAD_FOLDER'] + 'cases/'
            if os.path.isfile(path + case_image.filename) == True:
                os.remove(path + case_image.filename)
            db.session.delete(case_image)
            print(case_image.case.id)
            db.session.commit()
        else:
            return "Вы удаляете последнюю картинку, нужно чтобы хоть одна картинка оставалась"

        
        return redirect(url_for('update_case', id=case_image.case.id))
    except:
        return "При удалении произошла ошибка"


# Добавить Услуги (Дополнительные товары)
@app.route('/k/new_uslugi/<int:id>', methods=['POST', 'GET'])
@login_required
def new_uslugi(id):
    case = Cases.query.filter_by(id=id).first()

     #    Функция услуги
    uslugi = request.form.getlist("uslugi")
    if uslugi != []:
        for usl in uslugi:
            usl2 = Product.query.filter_by(id=usl).first()
            case.uslugi.append(usl2)
    try:
        db.session.add(case)
        db.session.commit()  
        # return redirect('/admin/new_cases')
        return redirect(url_for('update_case', id=case.id))
    except:
        return 'Произошла ошибка'


# Удалить Услуги (Дополнительные товары)
@app.route('/del_uslugi/<int:id><int:uslugi>')
@login_required
def del_uslugi(id, uslugi):
    case = Cases.query.filter_by(id=id).first()
    # uslugi = Case.query.filter_by(id=suggestion).first()
    for i in case.uslugi:
        if i.id == uslugi: 
            case.uslugi.remove(i)
            try:
                db.session.add(case)
                db.session.commit()
                return redirect(url_for('update_case', id=case.id))
            except:
                return "При удалении произошла ошибка"


# Редактировать Key
@app.route('/x/update_key_cases/<int:id>', methods=['POST', 'GET'])
@login_required
def update_key_cases(id):
    key = Keys_cases.query.filter_by(id=id).first()
    key.title = request.form['title']
    key.text = request.form['text']
    try:
        db.session.commit()
        return redirect(url_for('update_case', id=key.case.id))
    except:
        return 'Произошла ошибка'


# Удалить Key + картинки

@app.route('/f/del/key_cases/<int:id>', methods=['POST', 'GET'])
@login_required
def del_key_cases(id):
    key = Keys_cases.query.filter_by(id=id).first()
    pr = key.case.id
    try:
        path = app.config['UPLOAD_FOLDER'] + 'ca_keys/'
        for img in key.images:
            if os.path.isfile(path + img.filename) == True:
                os.remove(path + img.filename)

        db.session.delete(key)
        db.session.commit()
        print(key)
        return redirect(url_for('update_case', id=pr))
    except:
        return 'Произошла ошибка'







# Новый key_cases

@app.route('/new_key_cases/<int:id>', methods=['POST', 'GET'])
@login_required
def new_key_cases(id):
    case = Cases.query.filter_by(id=id).first()

    title1 = request.form['title1']
    text1 = request.form['text1']


    file1 = request.files['file1']
    alt1 = request.form['alt1']
    img1 = NewCaseKey(file1, alt1, case.url)
    img_1 = img1.rec_2()


    file2 = request.files['file2']
    alt2 = request.form['alt2']
    img2 = NewCaseKey(file2, alt2, case.url)
    img_2 = img2.rec_2()


    file3 = request.files['file3']
    alt3 = request.form['alt3']
    img3 = NewCaseKey(file3, alt3, case.url)
    img_3 = img3.rec_2()


    keys = Keys_cases(title=title1, text=text1)  
    keys.images.extend([img_1, img_2, img_3])
    case.keys.append(keys)

    try:
        db.session.add_all([case])
        db.session.commit()
        return redirect(url_for('update_case', id=case.id))
    except:
        return 'Произошла ошибка'

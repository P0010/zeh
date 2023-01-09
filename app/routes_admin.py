from flask import render_template, request, url_for, redirect, flash, session
from flask_login import login_user, login_required, logout_user
import os
from werkzeug.security import check_password_hash, generate_password_hash
from transliterate import slugify

from app import app, db, allowed_file
from app.models_main import Category, Product, Images, Keys, Images_key, Price, Suggestion, Social, Index_product, User
from app.new_image import NewProduct, NewKey, NewCategory

# Функции проверки кириллиц (удалить?)
def hascyr(s):
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(s.lower()) != set()

@app.route('/admin/new_product', methods=['POST','GET'])
@login_required
def new_product():
    if request.method == 'POST':
        name = request.form['name']
        if hascyr(name)==True:
            url = slugify(name)
        else:
            url = name
        category_id = request.form['category_id']
        intro = request.form['intro']
        text = request.form['text']
        title = request.form['title']
        description = request.form['description']
        product = Product(name=name, url=url, category_id=category_id, intro=intro, text=text, title=title, description=description)


        #     Функция загрузки image

        file = request.files['file']
        alt = request.form['alt']
        img = NewProduct(file, alt, url) 
        img = img.rec_2()

        product.items.append(img) # Подключиаем к таблице Product


        # Функция Keys

        title1 = request.form['title1']
        text1 = request.form['text1']
        keys = Keys(title=title1, text=text1)


        # Функция загрузки image key

        file1 = request.files['file1']
        alt1 = request.form['alt1']
        img1 = NewKey(file1, alt1, url)
        img_1 = img1.rec_2()


        file2 = request.files['file2']
        alt2 = request.form['alt2']
        img2 = NewKey(file2, alt2, url)
        img_2 = img2.rec_2()


        file3 = request.files['file3']
        alt3 = request.form['alt3']
        img3 = NewKey(file3, alt3, url)
        img_3 = img3.rec_2()


        keys.images.extend([img_1, img_2, img_3])
        product.keys.append(keys)
        


        #    Функция Price
        name_price = request.form.getlist("name_price")
        price = request.form.getlist("price")
        if name_price != ['']:
            uniq_and_fifa = dict(zip(name_price, price))
            
            for key,value in uniq_and_fifa.items():
                pr2 = Price(name_price=key, price=value)
                product.price.append(pr2)


        #    Функция Suggestion (дополнение)
        suggeso = request.form.getlist("suggestion")
        if suggeso != []:
            for sug in suggeso:
                sug2 = Suggestion(product_id=sug)
                product.suggestion.append(sug2)

        try:
            db.session.add(product)

            db.session.commit()
            
            # return redirect('/admin/new_product')
            return redirect(url_for('update_product', id=product.id))
        except:
            return 'Произошла ошибка'
    else:
        categories = Category.query.filter(Category.name=='root').first()
        return render_template('new_product.html', categories=categories)

# Редактироват Product 

@app.route('/admin/update_product/<int:id>', methods=['POST', 'GET'])
@login_required
def update_product(id):
    if request.method == "POST":
        pass
    else:
        product = Product.query.filter_by(id=id).first()
        categories = Category.query.filter(Category.name=='root').first()
        return render_template('update_product.html', product=product, categories=categories)


# Удалить Image Product 

@app.route('/del_image_product/<int:id>')
@login_required
def del_image_product(id):
    product_image = Images.query.filter_by(id=id).first()
    count = Product.query.filter_by(id=product_image.item.id).first()
    try:
        coun = 0
        for co in count.items:
            coun += 1

        if coun > 1:
            path = app.config['UPLOAD_FOLDER'] + 'new_product/'
            if os.path.isfile(path + product_image.filename) == True:
                os.remove(path + product_image.filename)
            db.session.delete(product_image)
            print(product_image.item.id)
            db.session.commit()
        else:
            return "Вы удаляете последнюю картинку, нужно чтобы хоть одна картинка оставалась"

        
        return redirect(url_for('update_product', id=product_image.item.id))
    except:
        return "При удалении произошла ошибка"


# Редактировать продукт (+ заголовок, +intro)

@app.route('/sd/product_reride/<int:id>', methods=['POST', 'GET'])
@login_required
def product_reride(id):
    product = Product.query.filter_by(id=id).first()
    product.name = request.form['name']
    if hascyr(product.name)==True:
        product.url = slugify(product.name)
    else:
        product.url = product.name

    product.intro = request.form['intro']
    product.title = request.form['title']
    product.description = request.form['description']

    try:
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('update_product', id=product.id))
    except:
        return 'Произошла ошибка'


# Загрузить Image Product
@app.route('/img/product_image_upload/<int:id>', methods=['POST', 'GET'])
@login_required
def product_image_upload(id):

    product = Product.query.filter_by(id=id).first()

    # Функция загрузки image
    file = request.files["file"]
    alt = request.form["alt"]
    img = NewProduct(file, alt, product.url) 
    img = img.rec_2()

    product.items.append(img) # Подключиаем к таблице Product

    try:
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('update_product', id=product.id))
    except:
        return 'Произошла ошибка'


# Удалить прайс

@app.route('/del_price/<int:id>')
@login_required
def del_price(id):
    price = Price.query.filter_by(id=id).first()
    try:
        db.session.delete(price)
        print(price.product.id)
        db.session.commit()
        return redirect(url_for('update_product', id=price.product.id))
    except:
        return "При удалении произошла ошибка"


# Добавить прайс

@app.route('/new_price/<int:id>', methods=['POST', 'GET'])
@login_required
def new_price(id):
    product = Product.query.filter_by(id=id).first()
    name_price = request.form.getlist("name_price")
    price = request.form.getlist("price")
    uniq_and_fifa = dict(zip(name_price, price))

    for key,value in uniq_and_fifa.items():
            pr2 = Price(name_price=key, price=value)
            product.price.append(pr2)

    try:
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('update_product', id=product.id))
    except:
        return 'Произошла ошибка'


# Добавить текст

@app.route('/new_text/<int:id>', methods=['POST', 'GET'])
@login_required
def new_text(id):
    product = Product.query.filter_by(id=id).first()
    product.text = request.form['text']
    try:
        db.session.commit()
        return redirect(url_for('update_product', id=product.id))
    except:
        return 'Произошла ошибка'


# Добавить Suggestion (Дополнительные товары)

@app.route('/new_suggestion/<int:id>', methods=['POST', 'GET'])
@login_required
def new_suggestion(id):
    product = Product.query.filter_by(id=id).first()
    suggeso = request.form.getlist("suggestion")
    if suggeso != []:
        for sug in suggeso:
            sug2 = Suggestion(product_id=sug)
            product.suggestion.append(sug2)
    try:
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('update_product', id=product.id))
    except:
        return 'Произошла ошибка'


# Удалить Suggestion (Дополнительные товары)
@app.route('/del_suggestion/<int:id>/<int:suggestion>')
@login_required
def del_suggestion(id, suggestion):
    product = Product.query.filter_by(id=id).first()
    suggestion2 = Suggestion.query.filter_by(id=suggestion).first()
    for i in product.suggestion:
        if i.id == suggestion: 
            product.suggestion.remove(i)
            try:
                db.session.add(product)
                db.session.delete(suggestion2)
                db.session.commit()
                return redirect(url_for('update_product', id=product.id))
            except:
                return "При удалении произошла ошибка"


# Редактировать Key
@app.route('/update_end_text/<int:id>', methods=['POST', 'GET'])
@login_required
def update_end_text(id):
    key = Keys.query.filter_by(id=id).first()
    key.title = request.form['title']
    key.text = request.form['text']
    try:
        db.session.commit()
        return redirect(url_for('update_product', id=key.product.id))
    except:
        return 'Произошла ошибка'


# Новый key

@app.route('/new_cases/<int:id>', methods=['POST', 'GET'])
@login_required
def new_key(id):
    product = Product.query.filter_by(id=id).first()

    title1 = request.form['title1']
    text1 = request.form['text1']


    # Функция загрузки image key

    file1 = request.files['file1']
    alt1 = request.form['alt1']
    img1 = NewKey(file1, alt1, product.url)
    img_1 = img1.rec_2()


    file2 = request.files['file2']
    alt2 = request.form['alt2']
    img2 = NewKey(file2, alt2, product.url)
    img_2 = img2.rec_2()


    file3 = request.files['file3']
    alt3 = request.form['alt3']
    img3 = NewKey(file3, alt3, product.url)
    img_3 = img3.rec_2()

    keys = Keys(title=title1, text=text1)
    keys.images.extend([img_1, img_2, img_3])
    product.keys.append(keys)

    try:
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('update_product', id=product.id))
    except:
        return 'Произошла ошибка'



# Удалить Key + картинки

@app.route('/d/del/key/<int:id>', methods=['POST', 'GET'])
@login_required
def del_key(id):
    key = Keys.query.filter_by(id=id).first()
    pr = key.product.id
    try:
        path = app.config['UPLOAD_FOLDER'] + 'keys/'
        for img in key.images:
            if os.path.isfile(path + img.filename) == True:
                os.remove(path + img.filename)

        db.session.delete(key)
        db.session.commit()
        print(key)
        return redirect(url_for('update_product', id=pr))
    except:
        return 'Произошла ошибка'
    


# Редактироват Category

@app.route('/admin/update_category/<int:id>', methods=['POST', 'GET'])
@login_required
def update_category(id):
    category = Category.query.filter_by(id=id).first()
    categories = Category.query.filter(Category.name=='root').first()
    if request.method == 'POST':
        category.name = request.form['name']
        if hascyr(category.name)==True:
            category.url = slugify(category.name)
        else:
            category.url = category.name

        file = request.files['file']
        filename = file.filename

        category.image[0].alt = request.form['alt']
        alt = request.form['alt']
        category.text = request.form['text']

        category.title = request.form['title']
        category.description = request.form['description']

        if filename != '':
            path = app.config['UPLOAD_FOLDER'] + 'catalog/'
            img_del = Images.query.filter_by(id=category.image[0].id).first()
            if os.path.isfile(path + img_del.filename) == True:
                os.remove(path + img_del.filename)


            img = NewCategory(file, alt, category.url)
            img = img.rec_2()

            category.image.append(img)


        try:
            db.session.add(category)
            if filename != '':
                db.session.delete(img_del)
            db.session.commit()
            return render_template('update_category.html', category=category, categories=categories)
        except:
            return 'Произошла ошибка'

    else:
        return render_template('update_category.html', category=category, categories=categories)




@app.route('/admin/new_category', methods = ['POST', 'GET'])
@login_required
def category():
    if request.method == 'POST':
        name = request.form['name']
        if hascyr(name)==True:
            url = slugify(name)
        else:
            url = name
        
        text = request.form['text']
        parent = request.form['category_id']
        title = request.form['title']
        description = request.form['description']
        category = Category(name=name, url=url, text=text, title=title, description=description) #child
        category.parent_id = parent


        #  Функция загрузки image

        file = request.files['file']
        alt = request.form['alt']
        img = NewCategory(file, alt, url)
        img = img.rec_2()

        category.image.append(img)
        

        try:
            db.session.add(category)
            db.session.commit()  
            return redirect('/admin/new_category')
        except:
            return 'Произошла ошибка'
    else:
        ind = Social.query.first()
        categories = Category.query.filter(Category.name=='root').first()
        return render_template('category.html', categories=categories, ind=ind)


@app.route('/admin/update', methods=['POST', 'GET'])
@login_required
def update():
    if request.method == 'POST':
        categories = Category.query.filter(Category.name=='root').first()
    else:
        categories = Category.query.filter(Category.name=='root').first()
        return render_template('update.html', categories=categories)



@app.route('/admin/move_product', methods = ['POST', 'GET'])
@login_required
def product_category():
    if request.method == 'POST':
        category_id = request.form['category_id']
        product_id = request.form['product_id']
        new = Product.query.filter_by(id=product_id).first()
        new.category_id = category_id
        try:
            db.session.commit()
            return redirect('/admin/move_product')
        except:
            return 'Произошла ошибка при исправлении статьи'
    else:
        categories = Category.query.filter(Category.name=='root').first()
        return render_template('product_category.html', categories=categories)


@app.route('/admin/move_category', methods = ['POST', 'GET'])
@login_required
def category_red():
    if request.method == 'POST':
        parent = request.form['parent']
        child = request.form['child']
        new = Category.query.filter_by(name=child).first()
        new.parent_id = parent
        try:
            db.session.commit()
            return redirect('/admin/move_category')
        except:
            return 'Произошла ошибка при исправлении статьи'
    else:
        ind = Social.query.first()
        categories = Category.query.filter(Category.name=='root').first()
        return render_template('category_red.html', categories=categories, ind=ind)


@app.route('/admin/update_index', methods=['POST', 'GET'])
@login_required
def admin_index():
    ind = Social.query.first()
    categories = Category.query.filter(Category.name=='root').first()

    if ind:
        ind_pr = Index_product.query.all()
        if request.method == 'POST':
            ind.telegram = request.form['telegram']
            ind.whatsap = request.form['whatsapp']
            ind.phone1 = request.form['phone1']
            ind.phone2 = request.form['phone2']
            ind.phone3 = request.form['phone3']
            ind.phone4 = request.form['phone4']
            ind.phone5 = request.form['phone5']
            ind.phone6 = request.form['phone6']
            ind.email = request.form['email']
            ind.title = request.form['title']
            ind.description = request.form['description']

             # Добавлени товара на главную
            index_prod = request.form.getlist("index_prod")
            
            if index_prod != []:
                for re in index_prod:
                    product = Product.query.filter_by(id=re).first()
                    prod = Index_product(product_id=re)
                    product.index_prod.append(prod)

            # Удаление продукта из главной 
            del_ind = request.form.getlist("del")

            if del_ind != []:
                for d in del_ind:
                    delit = Index_product.query.get_or_404(d)
                    db.session.delete(delit)

            try:
                # if 'prod' in globals():
                #     db.session.add(prod) - смысла в этом нет
                db.session.commit()
                return redirect('/admin/update_index')
            except:
                return 'Произошла ошибка'
        else:
            return render_template('admin_index.html', ind=ind, categories=categories, ind_pr=ind_pr)


    else:
        if request.method == 'POST':
            telegram = request.form['telegram']
            whatsapp = request.form['whatsapp']
            phone1 = request.form['phone1']
            phone2 = request.form['phone2']
            phone3 = request.form['phone3']
            phone4 = request.form['phone4']
            phone5 = request.form['phone5']
            phone6 = request.form['phone6']
            email = request.form['email']

         
              # Добавлени товара на главную
            index_prod = request.form.getlist("index_prod")
            
            if index_prod != []:
                for re in index_prod:
                    product = Product.query.filter_by(id=re).first()
                    prod = Index_product(product_id=re)
                    product.index_prod.append(prod)
             

            ind = Social(telegram=telegram, whatsap=whatsapp, phone1=phone1, phone2=phone2, phone3=phone3, phone4=phone4, phone5=phone5, phone6=phone6, email=email)

            try:
                db.session.add(ind)
                # if 'prod' in globals():
                #     db.session.add(prod)
                db.session.commit()
                return redirect('/admin/update_index')
            except:
                return 'Произошла ошибка'
        else:
            return render_template('admin_index.html', ind=ind, categories=categories)


# Удалить продукт

@app.route('/delete/<int:id>')
@login_required
def post_delete(id):
    product = Product.query.filter_by(id=id).first()


    try:
        if product.items != []:  # Удаление картинки в файловой системе
            for image in product.items:
                path = app.config['UPLOAD_FOLDER'] + 'new_product/'
                print(path + image.filename)
                if os.path.isfile(path + image.filename) == True:
                    os.remove(path + image.filename)

        if product.keys != []: # Удаление картинок в Key 
            for key in product.keys:
                path = app.config['UPLOAD_FOLDER'] + 'keys/'
                for img in key.images:
                    if os.path.isfile(path + img.filename) == True:
                        os.remove(path + img.filename)


        db.session.delete(product)
        db.session.commit()
        return redirect('/admin/update')
    except:
        return "При удалении произошла ошибка"


# Удаляем категории с продуктами и с фотографиями

@app.route('/delete/category/<int:category_id>')
@login_required
def category_delete(category_id):
    category = Category.query.filter_by(id=category_id).first()
    if category.children == [] and category.items == []:

        for image in category.image:
            path = app.config['UPLOAD_FOLDER'] + 'catalog/'
            if os.path.isfile(path + image.filename) == True:
                        os.remove(path + image.filename)

        try:
            db.session.delete(category)
            db.session.commit()
            return redirect('/admin/update')
        except:
            return "При удалении категории произошла ошибка"

    elif category.children == [] and category.items != []:

        # Удаление фото категории
        for image in category.image:
            path = app.config['UPLOAD_FOLDER'] + 'catalog/'
            if os.path.isfile(path + image.filename) == True:
                        os.remove(path + image.filename)

        # Удаление фото продукта
        for product in category.items:
            for img in product.items:
                path = app.config['UPLOAD_FOLDER'] + 'new_product/'
                if os.path.isfile(path + img.filename) == True:
                        os.remove(path + img.filename)
            
            if product.keys != []: # Удаление картинок в Key 
                for key in product.keys:
                    path = app.config['UPLOAD_FOLDER'] + 'keys/'
                    for img in key.images:
                        if os.path.isfile(path + img.filename) == True:
                            os.remove(path + img.filename)
        
        try:
            db.session.delete(category)
            db.session.commit()
            return redirect('/admin/update')
        except:
            return "При удалении продутов произошла ошибка"
    else:
        return "В категории есть подкатегории, вначале удалите их"



# Регистрация клиента

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password =request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            print(next_page)
            if next_page != None:
                return redirect(next_page)
            else:
                return redirect(url_for('new_product'))
        else:
            flash('Логин или пароль заполнен неправильно')
    else: 
        flash('Ошибка авторизации')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста, заполните все поля')
        elif password != password2:
            flash('Разные пароли')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')















# Ошибка 404

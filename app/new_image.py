from transliterate import slugify
from app import app
from PIL import Image
import PIL
import os
from app.models_main import Images_key, Images
from app.models_cases import Images_cases, Images_key_cases

# Функции проверки кириллиц
def hascyr(s):
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(s.lower()) != set()


# Класс создания картинки

class NewImage():
    def __init__(self, file, alt, url):
        self.file = file
        self.alt = alt
        self.url = url

    def upload_img(self):

        # Транслитерация alt если это нужно 

        if hascyr(self.alt)==True:
            self.alt_transliter = slugify(self.alt)
        else:
            self.alt_transliter = self.alt
        

        # Проверяем существование последнего id

        if self.l_id: 
            self.count = str(int(self.l_id.id) + 1)
        else:
            self.count = 1


        # Сохраняем файл

        im = Image.open(self.file).convert("RGB")  # Конвертируем в .rgb
        self.filename = self.alt_transliter + '_' + self.url + '_' + str(self.count) + '.webp'
        self.path = app.config['UPLOAD_FOLDER'] + self.folder
        im.save(os.path.join(self.path, self.filename), "webp")  # Сохраняем в .webp

 
    


# Картинка в продукте

class NewProduct(NewImage):
    def __init__(self, file, alt, url):
        super().__init__(file, alt, url)

    def rec_2(self):
        self.l_id = Images.query.order_by(Images.id.desc()).first()  # Узнаем последний id
        self.folder = 'new_product/'

        super().upload_img()

        self.image = Images(filename=self.filename, alt=self.alt)  # Сохраняем картинку в классе
        return self.image



# Картинки в продукте Key

class NewKey(NewImage):
    def __init__(self, file, alt, url):
        super().__init__(file, alt, url)
   
    def rec_2(self):
        self.l_id = Images_key.query.order_by(Images_key.id.desc()).first()  # Узнаем последний id
        self.folder = 'keys/'

        super().upload_img()

        self.image = Images_key(filename=self.filename, alt=self.alt)  # Сохраняем картинку в классе
        return self.image




# Картинка в Cases

class NewCaseImage(NewImage):
    def __init__(self, file, alt, url):
        super().__init__(file, alt, url)

    def rec_2(self):
        self.l_id = Images_cases.query.order_by(Images_cases.id.desc()).first()  # Узнаем последний id
        self.folder = 'cases/'

        super().upload_img()

        self.image = Images_cases(filename=self.filename, alt=self.alt)  # Сохраняем картинку в классе
        return self.image


# Картинки в Case Key

class NewCaseKey(NewImage):
    def __init__(self, file, alt, url):
        super().__init__(file, alt, url)
   
    def rec_2(self):
        self.l_id = Images_key_cases.query.order_by(Images_key_cases.id.desc()).first()  # Узнаем последний id
        self.folder = 'ca_keys/'

        super().upload_img()

        self.image = Images_key_cases(filename=self.filename, alt=self.alt)  # Сохраняем картинку в классе
        return self.image




# Картинка в Категории

class NewCategory(NewImage):
    def __init__(self, file, alt, url):
        super().__init__(file, alt, url)

    def rec_2(self):
        self.l_id = Images.query.order_by(Images.id.desc()).first()  # Узнаем последний id
        self.folder = 'catalog/'

        super().upload_img()

        self.image = Images(filename=self.filename, alt=self.alt)  # Сохраняем картинку в классе
        return self.image
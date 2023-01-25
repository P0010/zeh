
// Добавление/удаление input в админке (создание таблиц)

var coutn_price = 0;

function AInput_price() {
  var profile1 = document.getElementById('profile1');
  var div = document.createElement('div');
  div.id = 'inputadm' + ++coutn_price;
  div.classList = 'input_red';
  div.innerHTML = '<input type="text" name="name_price" class="admin_n" maxlength="50" placeholder="Введите название(до 50 символов)" required><input type="number" name="price" class="admin_n" maxlength="20" placeholder="Введите цену" required>';
  profile1.appendChild(div);
}

function DInput_price() {
  var div = document.getElementById('inputadm' + coutn_price);
  div.remove();
  --coutn_price;
}


// Добавление/удаление input в админке (создание телефона)

var x = 0;

function addInput_phone() {
  var profile = document.getElementById('profile');
  var div = document.createElement('div');
  div.id = 'input' + ++x;
  div.classList = 'inputadm';
  div.innerHTML = '<textarea name="phone" maxlength="400" placeholder="Введите номер телефон, пример +7(999)999 99 99" require></textarea>';
  profile.appendChild(div);
}

function delInput_phone() {
  var div = document.getElementById('input' + x);
  div.remove();
  --x;
}

//    Pop up --??

let header__burger2 = document.querySelectorAll('.open_pop_up,#pop_up_close');
let header_menu2 = document.querySelector('.pop_up');
let back2 = document.querySelector('body');

header__burger2.forEach(function (item) {
   item.onclick = function () {
      item.classList.toggle('active');
      header_menu2.classList.toggle('active');
      back2.classList.toggle('lock');
   }
});

//    Pop up - catalog

let header__burger_catalog = document.querySelectorAll('.open_pop_up_catalog,#catalog_close');
let header_menu_catalog = document.querySelector('.pop_up_catalog');
let back_catalog = document.querySelector('body');

header__burger_catalog.forEach(function (item) {
   item.onclick = function () {
      item.classList.toggle('active');
      header_menu_catalog.classList.toggle('active');
      back_catalog.classList.toggle('lock');
   }
});

//    Pop up - mobile menu

let header__burger_mobilmenu = document.querySelectorAll('.open_pop_up_mobilmenu,#mobilmenu_close');
let header_mobilmenu = document.querySelector('.pop_up_mobilmenu');
let back_mobilmenu = document.querySelector('body');

header__burger_mobilmenu.forEach(function (item) {
   item.onclick = function () {
      item.classList.toggle('active');
      header_mobilmenu.classList.toggle('active');
      back_mobilmenu.classList.toggle('lock');
   }
});

//    Pop up - otvet form

let otvet_popup_active = document.querySelectorAll('.open_otvet,#otvet_close');
let otvet_block = document.querySelector('.pop_up_otvet');
let back_otvet = document.querySelector('body');

otvet_popup_active.forEach(function (item) {
   item.onclick = function () {
      item.classList.toggle('active');
      otvet_block.classList.toggle('active');
      back_otvet.classList.toggle('lock');
   }
});

// pop up по таймеру 30 секундв
// функция появления
function greet () {
  document.getElementsByClassName('pop_up1')[0].style.display = "flex";
  // устанавливаем localstorage
  localStorage.setItem('test', 1);
}

width = screen.width; // ширина окна
console.log(width); // вывод в консоль

// если localstorage не равно 1, включаем функцию greet через 4 секунды
if (localStorage.getItem('test') != 1 & width<400) setTimeout (greet, 25000) ;

// при клике мы выключаем pop up
function rabbit () {
  document.getElementsByClassName('pop_up1')[0].style.display = "none";
}
    
// удаляем нажимая на id=del
del.onclick = function() {
  delete localStorage.test;
}



// Слайдер продукта (картинки)

/* Индекс слайда по умолчанию */
var slideIndex = 1;
showSlides(slideIndex);

/* Функция увеличивает индекс на 1, показывает следующй слайд*/
function plusSlide() {
    showSlides(slideIndex += 1);
}

/* Функция уменьшяет индекс на 1, показывает предыдущий слайд*/
function minusSlide() {
    showSlides(slideIndex -= 1);  
}

/* Устанавливает текущий слайд */
function currentSlide(n) {
    showSlides(slideIndex = n);
}

/* Основная функция слайдера */
function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("item_s");
    var dots = document.getElementsByClassName("slider-dots_item");
    if (n > slides.length) {
      slideIndex = 1
    }
    if (n < 1) {
        slideIndex = slides.length
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}





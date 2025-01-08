const categoryLinks = document.querySelectorAll('.category-link');  // Все стрелки
const subcategories = document.querySelectorAll('.subcategories');  // Все подкатегории

categoryLinks.forEach((categoryLink, index) => {
    categoryLink.addEventListener('click', () => {
        subcategories[index].classList.toggle('active');  // Открытие/закрытие подкатегорий
    });
});





// JavaScript для смены основного изображения при клике на миниатюру

const thumbnails = document.querySelectorAll('.thumbnail');
const mainImage = document.getElementById('main-image');

thumbnails.forEach(thumbnail => {
    thumbnail.addEventListener('click', () => {
        mainImage.src = thumbnail.dataset.image;
    });
});
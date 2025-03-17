// main.js

document.getElementById('image-upload').onchange = function() {
    var file = this.files[0];
    var reader = new FileReader();

    reader.onload = function(e) {
        var imageElement = document.getElementById('uploaded-image');
        imageElement.src = e.target.result;
        imageElement.style.maxWidth = '400px';  // 가로 크기를 400px로 제한
        imageElement.style.height = 'auto';  // 세로 크기는 비율에 맞게 자동으로 조절
        imageElement.style.display = 'block';
        document.getElementById('images-container').style.display = 'flex';
        document.getElementById('input-and-submit-container').style.display = 'flex';
        document.getElementById('saved-image').style.display = 'none';
    }
    reader.readAsDataURL(file);
};


document.getElementById('submit-btn_').onclick = function() {

    var imageFileInput = document.getElementById('image-upload');
    var formData = new FormData();
    formData.append('image', imageFileInput.files[0]);


    fetch('/process_image_ocr', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(images => {
        var savedImageElement = document.getElementById('uploaded-image');
        var objectURL = URL.createObjectURL(images);
        savedImageElement.src = objectURL;
        savedImageElement.style.maxWidth = 'none';  // 가로 크기를 400px로 제한
        savedImageElement.style.height = 'auto';  // 세로 크기는 비율에 맞게 자동으로 조절=
        savedImageElement.style.display = 'block';
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        alert('An error occurred: ' + error.message);
    });
};

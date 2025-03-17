// main.js

document.getElementById('image-upload').onchange = function() {
    var file = this.files[0];
    var reader = new FileReader();

    // 결과 이미지 제거
    var savedImageElement = document.getElementById('saved-image');
    if (savedImageElement) {
        savedImageElement.style.display = 'none';
    }

    // before-input, after-input 값 초기화
    document.getElementById('before-input').value = '';
    document.getElementById('after-input').value = '';

    reader.onload = function(e) {
        var imageElement = document.getElementById('uploaded-image');
        imageElement.src = e.target.result;
        imageElement.style.maxWidth = '400px';  // 가로 크기를 400px로 제한
        imageElement.style.height = 'auto';  // 세로 크기는 비율에 맞게 자동으로 조절
        imageElement.style.display = 'block';
        document.getElementById('images-container').style.display = 'flex';
        document.getElementById('input-container').style.display = 'block';
        //document.getElementById('sliders-container').style.display = 'block';

        // Show the toggle button
        document.getElementById('toggle-btn').style.display = 'flex';
        document.getElementById('submit-btn').style.display = 'flex';
    }
    reader.readAsDataURL(file);
};

document.getElementById('submit-btn').onclick = function() {
    var imageFileInput = document.getElementById('image-upload');
    var beforeInputValue = document.getElementById('before-input').value;
    var afterInputValue = document.getElementById('after-input').value;

    var formData = new FormData();
    formData.append('image', imageFileInput.files[0]);
    formData.append('before', beforeInputValue);
    formData.append('after', afterInputValue);

    if (isNaN(beforeInputValue) || isNaN(afterInputValue) || beforeInputValue === '' || afterInputValue === '') {
        alert('Before and After must be valid numbers.');
        return;
    }
    if (Number(beforeInputValue) <= Number(afterInputValue)) {
        alert('After must be less than Before.');
        return;
    }

    fetch('/process_image', {
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
        var savedImageElement = document.getElementById('saved-image');
        var objectURL = URL.createObjectURL(images);
        savedImageElement.src = objectURL;
        savedImageElement.style.maxWidth = '400px';  // 가로 크기를 400px로 제한
        savedImageElement.style.height = 'auto';  // 세로 크기는 비율에 맞게 자동으로 조절=
        savedImageElement.style.display = 'block';
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        alert('An error occurred: ' + error.message);
    });
};

var sliders = document.getElementsByClassName('slider');
for (var i = 0; i < sliders.length; i++) {
    sliders[i].oninput = function() {
        var label = this.dataset.label;
        document.getElementById(label + '-value').innerText = this.value;
    }
}

document.getElementById('toggle-btn').onclick = function() {
    var slidersContainer = document.getElementById('sliders-container');
    var toggleBtn = document.getElementById('toggle-btn');

    if (slidersContainer.style.display === 'none') {
        slidersContainer.style.display = 'block';
        toggleBtn.textContent = '▼ Hide Sliders';
    } else {
        slidersContainer.style.display = 'none';
        toggleBtn.textContent = '▶ Show Sliders';
    }
};

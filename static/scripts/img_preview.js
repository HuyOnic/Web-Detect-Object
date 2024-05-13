document.getElementById('file').addEventListener('change', function(event) {
    var fileInput = event.target;
    var imagePreview = document.getElementById('imagePreview');
  
    // Check if any file is selected
    if (fileInput.files.length > 0) {
      var file = fileInput.files[0];
      var reader = new FileReader();
  
      reader.onload = function(e) {
        var imageUrl = e.target.result;
        var img = document.createElement('img');
        img.src = imageUrl;
        img.classList.add('img')
        imagePreview.innerHTML = '';
        imagePreview.appendChild(img);
      }
  
      reader.readAsDataURL(file);
    }
  });
  
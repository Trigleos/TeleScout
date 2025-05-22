function previewImage(img) {
  var enlargedImg = document.createElement("img");
  enlargedImg.src = img.src;
  var newWindow = window.open("");
  newWindow.document.write(enlargedImg.outerHTML);
}


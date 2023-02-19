function thumbUp() {
  console.log("bouton thumb up cliqué");
  var thumbDownButton = document.getElementById("thumb-down-button");
  var thumbUpButton = document.getElementById("thumb-up-button");
  thumbDownButton.classList.remove("active");
  thumbUpButton.classList.add("active");
}

function thumbDown(){
  console.log("bouton thumb down cliqué")
  var thumbDownButton = document.getElementById("thumb-down-button");
  var thumbUpButton = document.getElementById("thumb-up-button");
  thumbUpButton.classList.remove("active");
  thumbDownButton.classList.add("active");
}
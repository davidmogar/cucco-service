document.addEventListener('DOMContentLoaded', function(event) {
  document.getElementById('hamburger').addEventListener('click', function(event) {
    document.getElementsByTagName('nav')[0].classList.toggle('expanded');
  }, false);

  window.addEventListener('click', function(e){
    if (!document.getElementsByTagName('header')[0].contains(e.target)) {
      document.getElementsByTagName('nav')[0].classList.remove('expanded');
    }
  });

  var goUpButton = document.getElementById('go-up');
  var goUpButtonVisible = false;

  goUpButton.addEventListener('click', function(event) {
    window.scrollTo(0, 0);
  }, false);

  window.addEventListener('scroll', function(e) {
    if (!goUpButtonVisible && window.scrollY > 1000) {
      goUpButtonVisible = true;
      goUpButton.classList.add('visible');
    } else if (goUpButtonVisible && window.scrollY < 800) {
      goUpButtonVisible = false;
      goUpButton.classList.remove('visible');
    }
  });
});

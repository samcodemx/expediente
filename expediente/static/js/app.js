document.addEventListener('DOMContentLoaded', function () {
  /* ========================================
    Abrir y cerrar el menu de sesion
  ========================================= */
  let showToggle = document.getElementById('showToggle');
  let subMenu = document.getElementById('subMenu');
  showToggle.addEventListener('click', function () {
    subMenu.classList.toggle('open-menu');
  });


  
});

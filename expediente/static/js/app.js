document.addEventListener('DOMContentLoaded', function () {

  /* ========================================
  Autoresize para los TextArea
========================================= */
  const textAreas = document.querySelectorAll('textarea');

  textAreas.forEach(function (textarea) {
    textarea.addEventListener('input', function () {
      textarea.style.height = 'auto'; // Restaurar la altura a auto para ajustar correctamente el contenido
      textarea.style.height = `${textarea.scrollHeight}px`; // Establecer la altura en función del contenido
    });
  });

  /* ========================================
  Cambiar color del enlace dependiendo la url
  ========================================= */
    // Obtenemos la URL actual
    let currentURL = window.location.pathname;

    // Verificamos si la URL coincide con cada enlace y actualizamos las clases correspondientes
    if (currentURL === '/') {
      document.getElementById('files').classList.add('text-main');
      document.getElementById('files').classList.remove('text-gray-400');
      document.getElementById('files').classList.add('font-semibold');
    } else if (currentURL === '/create-file') {
      document.getElementById('create-file').classList.add('text-main');
      document.getElementById('create-file').classList.remove('text-gray-400');
      document.getElementById('create-file').classList.add('font-semibold');
    } else if (currentURL === '/help') {
      document.getElementById('help').classList.add('text-main');
      document.getElementById('help').classList.remove('text-gray-400');
      document.getElementById('help').classList.add('font-semibold');
    }

});

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
  Cambiar los formularios
========================================= */
  // Obtenemos todos los botones y formularios
  const botones = document.querySelectorAll('#botonera button');
  const formularios = document.querySelectorAll('.formulario');

  // Función para ocultar todos los formularios
  function ocultarFormularios() {
    formularios.forEach(formulario => {
      formulario.style.display = 'none';
    });
  }

  // Función para mostrar el formulario seleccionado
  function mostrarFormulario(id) {
    const formulario = document.getElementById(id);
    formulario.style.display = 'block';
  }

  // Añadimos los event listeners a los botones
  botones.forEach(boton => {
    boton.addEventListener('click', function() {
      const id = this.id.replace('btn_', 'form_'); // Obtenemos el ID del formulario correspondiente
      ocultarFormularios(); // Ocultamos todos los formularios
      mostrarFormulario(id); // Mostramos el formulario seleccionado
    });
  });


  /* ========================================
  Cambiar el color de la botonera de formularios
  al dar click
  ========================================= */
  let buttons = document.querySelectorAll('#botonera button');
  console.log('Buttons');

  function toggleClasesBoton(boton) {
    buttons.forEach(b => {
      b.classList.remove('bg-background', 'font-bold');
      b.classList.add('bg-white');
    });
    boton.classList.remove('bg-white');
    boton.classList.add('bg-background', 'font-bold');
  }

  buttons.forEach(boton => {
    boton.addEventListener('click', function() {
      toggleClasesBoton(this);
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

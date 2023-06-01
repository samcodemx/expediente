document.addEventListener('DOMContentLoaded', function () {
  console.log('JS...');
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

});

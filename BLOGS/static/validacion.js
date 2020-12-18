function validar(){
    var p1 = document.getElementById("ActualizarPassword").value;
    var p2 = document.getElementById("confirActualizarPassword").value;

    var espacios = false;
var cont = 0;

while (!espacios && (cont < p1.length)) {
  if (p1.charAt(cont) == " ")
    espacios = true;
  cont++;
}
   
if (espacios) {
  alert ("La contraseña no puede contener espacios en blanco");
  return false;
}

if (p1.length == 0 || p2.length == 0) {
    alert("Los campos de la contraseña no pueden quedar vacios");
    return false;
}

  if (p1 != p2) {
    alert("Las contraseñas deben de coincidir");
    return false;
  } else {
    alert("Todo esta correcto");
    return true; 
  }

}


function crearUsuario(){
  document.getElementById("fomularioUsuario").action="/login";
}

function crearBlog(){
  document.getElementById("fomularioBlog").action="/blog";
}
function crearBlog2(){
  document.getElementById("formulario_comentario").action="{{ url_for('crearBlog',post_id=r['id_b']) }}";
} 


var i=3;
function validar_formulario(){    
var p1 = document.getElementById("usuario").value;
var p2 = document.getElementById("password").value;

    if(p1=="test" && p2=="test" && i>0){
        alert("Ingreso Exitoso");   
    }else if(i==0){
        var  boton = document.getElementsbyName("usuario");
        var  boton = document.getElementsbyName("password");
        boton.disabled = true;
    }else{
        alert("Le quedan "+(i)+" intentos");
        i--;
    }
   
}


    
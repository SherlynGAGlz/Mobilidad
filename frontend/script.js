/**est es parte del front, es de Fany */
const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

/**este codigo es para lo del back tambien, la parte que dio LU */
/*async function enviarDatos() {
    const datos = { fuente: "web", datos: { sensor: 25.5 } };
    await fetch("http://127.0.0.1:8000/recibe_datos/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    });
}*/
//este es el codigo mio de prueba para el back tambien
async function enviarDatos() {
    const datos = {
        origen: "web",
        datos: { sensor: 25.5 }
    };

    //peticion post a la pedorra api
    try {
        const respuesta = await fetch("http://127.0.0.1:8000/recibe_datos/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(datos),
        });

        // Verificamos si la respuesta fue exitosa
        if (respuesta.ok) {
            const jsonRespuesta = await respuesta.json();
            console.log("Datos guardados:", jsonRespuesta);
        } else {
            console.log("Error al guardar los datos:", respuesta.statusText);
        }
    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
}

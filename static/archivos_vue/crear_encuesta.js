const vm = new Vue({
    el:'main',
    data:{
        perfiles:[],
        token: $("#csrf").val(),
        pregunta:{
            pregunta:'',
            recomendacion:'',
            respuestas:{
                Uno:'',
                Dos: '',
                Tres: '',
                Cuatro: '',
                Cinco: '',
            }
        },
        //Copiar a modificar
        pregunta_editar:{
            id:'',
            pregunta:{}
        },
        encuesta:{
            perfil:'',
            preguntas:[],
        },
        //migrar a modificiar_encuesta.js
        encuesta_editar:{},
        encuestas:[],
        //---//
    },
    created(){
        this.cargar_perfiles();
        if (localStorage.getItem('encuesta')) {
            let aux = localStorage.getItem('encuesta');
            this.encuesta = JSON.parse(aux);
        }
        //migrar a modificar_encuesta.js
        if (window.location.pathname === "/administrador/encuesta/modificar"){
            this.cargar_encuestas();
        }
    },
    methods:{
        //migrar a modificar_encuesta.js
        eliminar_pregunta_encuesta(id){
            var self = this;
            numero = id + 1;
            swal({
                title: '¿Estás seguro?',
                text: "Estás a punto de eliminar la pregunta " + numero + " de la encuesta.",
                type: 'question',
                showCancelButton: true,
                confirmButtonColor: 'red',
                cancelButtonColor: 'gray',
                confirmButtonText: 'Si, borrar pregunta!',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.value) {
                swal({
                    title: 'Eliminada!',
                    text: 'La pregunta ha sido eliminada, no olvides confirmar los cambios hechos antes de salir del sistema.',
                    type: 'error'
                }).then((result) =>{
                    self.encuesta_editar.preguntas.splice(id,1);
                    localStorage.setItem('encuesta', JSON.stringify(self.encuesta_editar))
            })
            }
        })
        },
        agregar_pregunta_nueva(){
            var self = this
            if (self.pregunta.pregunta.length == 0 || self.pregunta.recomendacion.length == 0 || self.pregunta.respuestas.Uno.length == 0 || self.pregunta.respuestas.Dos.length == 0 || self.pregunta.respuestas.Tres.length == 0 || self.pregunta.respuestas.Cuatro.length == 0 || self.pregunta.respuestas.Cinco.length == 0){
                swal(
                    'Ups...',
                    'Todos los campos de la nueva pregunta son obligatorios.',
                    'error'
                )
            }
            else {
                var aux = JSON.parse(JSON.stringify(self.pregunta));
                self.encuesta_editar.preguntas.push(aux);
                self.pregunta = {
                    pregunta: '',
                    respuestas: {
                        Uno: '',
                        Dos: '',
                        Tres: '',
                        Cuatro: '',
                        Cinco: '',
                    }
                }
                localStorage.setItem('encuesta', JSON.stringify(self.encuesta_editar))
                swal(
                    'Bien!',
                    'Has agregado una nueva pregunta a la encuesta, no olvides confirmar los cambios hechos antes de salir del sistema.',
                    'success'
                )
            }
        },
        desactivar_encuesta(){
            var self = this;
            swal({
                title: '¿Estás seguro?',
                text: "Esta acción desactivará la encuesta en el sistema, si estás seguro da click en Confirmar",
                type: 'question',
                showCancelButton: true,
                confirmButtonColor: 'rgb(19,61,57)',
                cancelButtonColor: 'gray',
                confirmButtonText: 'Confirmar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.value) {
                axios({
                    method: 'post',
                    url: '/administrador/encuesta/desactivar',
                    datatype: 'json',
                    data: {
                        id: self.encuesta_editar.id,
                    },
                    headers: { "X-CSRFToken": self.token }
                }).then(function (respuesta) {
                    if (respuesta.data == "ok"){
                        swal({
                            title: 'Bien!',
                            text: 'Has desactivado la encuesta.',
                            type: 'error'
                        }).then((result) => {
                            location.reload();
                    })
                    }
                    else{
                        swal(
                            'Ups...',
                            'Algo ha salido mal & la acción no se llevó a cabo.',
                            'error'
                        )
                    }
                })
            }
        })
        },
        modificar_encuesta(){
            var self = this;
            let aux = JSON.parse(JSON.stringify(self.encuesta_editar));
            if (!self.encuesta_editar.perfil) {
                swal({
                    type: 'error',
                    title: 'Ups...',
                    text: 'No has escogido el perfil vocacional de esta encuesta, selecciónalo y vuelve a intentarlo.',
                })
            }
            else {
                swal({
                    title: '¿Estás seguro?',
                    text: "Esta acción modificará la encuesta en el sistema, si estás seguro que el proceso ha terminado da click en Confirmar",
                    type: 'question',
                    showCancelButton: true,
                    confirmButtonColor: 'rgb(19,61,57)',
                    cancelButtonColor: 'gray',
                    confirmButtonText: 'Confirmar',
                    cancelButtonText: 'Cancelar'
                }).then((result) => {
                    if (result.value) {
                    axios({
                        method: 'post',
                        url: '/administrador/encuesta/modificar',
                        datatype: 'json',
                        data: {
                            encuesta: aux,
                        },
                        headers: { "X-CSRFToken": self.token }
                    }).then(function (respuesta) {
                        swal({
                            title: 'Bien!',
                            text: 'Has guardado la encuesta.',
                            type: 'success'
                        }).then((result) => {
                            localStorage.removeItem('encuesta');
                            location.reload();
                    })
                    })
                }
            })
            }

        },
        asignar_pregunta_e(id) {
            var self = this;
            aux = self.encuesta_editar.preguntas[id];
            self.pregunta_editar.id = id;
            self.pregunta_editar.pregunta = aux;
        },
        asignar_encuesta(id) {
            var self = this;
            aux = self.encuestas[id];
            self.encuesta_editar = aux;
            let div = document.getElementById("div-encuesta-modificar");
            div.setAttribute("style", "display: block");
        },
        cargar_encuestas(){
            var self = this;
            axios({
                method: "POST",
                url: "/administrador/encuesta/cargar/todos",
                headers: { "X-CSRFToken": this.token }
            }).then((respuesta) => {
                respuesta.data.forEach(element => {
                self.encuestas.push(element);
        });
        })
        },

        //---//
        guardar_encuesta(){
            var self = this;
            let aux = JSON.parse(JSON.stringify(self.encuesta));
            if (!self.encuesta.perfil){
                swal({
                    type: 'error',
                    title: 'Ups...',
                    text: 'No has escogido el perfil vocacional de esta encuesta, selecciónalo y vuelve a intentarlo.',
                })
            }
            else{
                swal({
                    title: '¿Estás seguro?',
                    text: "Esta acción guardará la encuesta en el sistema, si estás seguro que el proceso ha terminado da click en Confirmar",
                    type: 'question',
                    showCancelButton: true,
                    confirmButtonColor: 'rgb(19,61,57)',
                    cancelButtonColor: 'gray',
                    confirmButtonText: 'Confirmar',
                    cancelButtonText: 'Cancelar'
                }).then((result) => {
                    if (result.value) {
                    axios({
                        method: 'post',
                        url: '/administrador/encuesta/guardar',
                        datatype: 'json',
                        data: {
                            encuesta: aux,
                        },
                        headers: { "X-CSRFToken": self.token }
                    }).then(function (respuesta) {
                        if (respuesta.data == "ok"){
                            swal({
                                title: 'Bien!',
                                text: 'Has guardado la encuesta.',
                                type: 'success'
                            }).then((result) => {
                                localStorage.clear();
                            location.reload();
                        })
                        }
                        else{
                            swal(
                                'Ups...',
                                respuesta.data,
                                'error'
                            )
                        }
                    })
                }
            })
            }
        },
        eliminar_pregunta(id){
            var self = this;
            swal({
                title: '¿Estás seguro?',
                text: "Esta acción no podrá ser revertida.",
                type: 'question',
                showCancelButton: true,
                confirmButtonColor: 'red',
                cancelButtonColor: 'gray',
                confirmButtonText: 'Si, borrar pregunta!',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.value) {
                swal({
                    title: 'Eliminada!',
                    text: 'La pregunta ha sido eliminada.',
                    type: 'error'
                }).then((result) =>{
                    self.encuesta.preguntas.splice(id,1);
                localStorage.setItem('encuesta', JSON.stringify(self.encuesta))
                location.reload();
            })
            }
        })
        },
        editar_pregunta() {
            var self = this;
            let aux = JSON.parse(JSON.stringify(self.pregunta_editar.pregunta));
            self.encuesta.preguntas[self.pregunta_editar.id] = aux;
            localStorage.setItem('encuesta', JSON.stringify(self.encuesta));
            location.reload();
        },
        cargar_perfiles(){
            var self = this;
            axios({
                method: "POST",
                url: "/administrador/perfil/cargar/todos",
                headers: { "X-CSRFToken": this.token }
            }).then((respuesta)=>{
                respuesta.data.forEach(element => {
                self.perfiles.push(element);
        });
        })
        },
        agregar_pregunta(){
            var self = this
            var aux = JSON.parse(JSON.stringify(self.pregunta));
            self.encuesta.preguntas.push(aux);
            self.pregunta = {
                pregunta: '',
                respuestas: {
                    Uno: '',
                    Dos: '',
                    Tres: '',
                    Cuatro: '',
                    Cinco: '',
                }
            }
            localStorage.setItem('encuesta', JSON.stringify(self.encuesta))
        },
        limpiar_campos(){
            swal({
                title: '¿Estás seguro?',
                text: "Esta acción no podrá ser revertida.",
                type: 'question',
                showCancelButton: true,
                confirmButtonColor: 'red',
                cancelButtonColor: 'green',
                confirmButtonText: 'Si, limpiar campos',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.value) {
                swal({
                    title: 'Borrado!',
                    text: 'Se han limpiado todos los campos.',
                    type: 'success'
                }).then((result)=>{
                    localStorage.clear();
                location.reload();
            })
            }
        })
        },
        asignar_pregunta(id){
            var self = this;
            aux = self.encuesta.preguntas[id];
            self.pregunta_editar.id = id;
            self.pregunta_editar.pregunta = aux;
        },

    },
});

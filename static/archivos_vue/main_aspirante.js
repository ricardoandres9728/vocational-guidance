const vm = new Vue({
    el: 'main',
    data: {
        token: $("#csrf").val(),
        aspirante: {
            nombres: '',
            apellidos: '',
            correo: '',
            password: {
                anterior: '',
                nueva: '',
            },
            newsletter: ''
        },
        encuestas: [],
        encuesta: null,
        id_encuesta: 0,
        id_pregunta: 0,
        respuesta_id: 0,
        rta: {
            rta: '',
            pta: '',
        },
        respuestas: [],
        recomendaciones: [],
        mensaje: ""
    },
    created() {
        this.cargar_aspirante();
        this.cargar_encuestas();
    },
    methods: {
        prev() {
            this.respuestas.pop();
            this.id_pregunta--;
            this.respuesta_id = null;
        },
        next() {
            if (this.respuesta_id) {
                this.respuestas.push(this.respuesta_id);
                this.id_pregunta++;
                this.respuesta_id = null;
            } else {
                swal({
                    title: "Oops...",
                    type: "error",
                    text: "Debes seleccionar una opcion"
                })
            }

        },
        finalizar_encuesta() {
            if (this.respuesta_id) {
                swal({
                    title: '¿Estás seguro?',
                    text: "Esta acción guardará tus respuestas en el sistema.",
                    type: 'question',
                    showCancelButton: true,
                    confirmButtonColor: 'rgb(19,61,57)',
                    cancelButtonColor: 'gray',
                    confirmButtonText: 'Confirmar',
                    cancelButtonText: 'Cancelar',
                    allowOutsideClick: false,
                }).then((result) => {
                    if (result.value) {
                        this.respuestas.push(this.respuesta_id);
                        this.respuesta_id = null;
                        axios({
                            method: "POST",
                            url: "/aspirante/encuesta/guardar",
                            headers: { "X-CSRFToken": this.token },
                            data: {
                                respuestas: this.respuestas,
                                encuesta: this.encuesta.id
                            }
                        }).then((respuesta) => {
                            swal({
                                title: 'Bien!',
                                text: 'Encuesta resuelta exitosamente',
                                type: 'success'
                            }).then((result) => {
                                this.encuesta = null
                                localStorage.clear();
                            })
                            this.recomendaciones = respuesta.data.recomendaciones;
                            console.log(this.recomendaciones)
                            if (respuesta.data.respuesta) {
                                this.mensaje = "Felicitaciones, cumples con el perfil"
                            } else {
                                this.mensaje = 'Lo sentimos, no cumples con el perfil'
                            }
                        })
                    }
                });
            } else {
                swal({
                    title: "Oops...",
                    type: "error",
                    text: "Debes seleccionar una opcion"
                })
            }
        },
        mostrar_encuesta() {
            function compare(a, b) {
                const idA = a.id;
                const idB = b.id;
                let comparison = 0;
                if (idA > idB) {
                    comparison = 1;
                } else if (idA < idB) {
                    comparison = -1;
                }
                return comparison;
            }
            this.encuesta = this.encuestas[this.id_encuesta];
            this.encuesta.preguntas = this.encuesta.preguntas.sort(compare);
        },
        cargar_encuestas() {
            var self = this;
            axios({
                method: "POST",
                url: "/administrador/encuesta/cargar/todos",
                headers: { "X-CSRFToken": this.token }
            }).then((respuesta) => {
                self.encuestas = respuesta.data;
            })
        },
        newsletter() {
            var self = this;
            axios({
                method: 'post',
                url: '/aspirante/newsletter',
                headers: { "X-CSRFToken": self.token }
            })
        },
        cambiar_password() {
            var self = this
            swal({
                title: '¿Estás seguro?',
                text: "Esta acción cambiará tu contraseña en el sistema.",
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
                        url: '/aspirante/cambiar/password',
                        datatype: 'json',
                        data: {
                            password: self.aspirante.password,
                        },
                        headers: { "X-CSRFToken": self.token }
                    }).then(function(respuesta) {
                        if (respuesta.data == "ok") {
                            swal({
                                title: 'Bien!',
                                text: 'Has cambiado el aspirante.',
                                type: 'success'
                            }).then((result) => {
                                localStorage.clear();
                                location.reload();
                            })
                        } else {
                            swal(
                                'Ups...',
                                'No se hicieron cambios.',
                                'error'
                            )
                        }
                    })
                }
            })
        },
        modificar_aspirante() {
            var self = this
            var aux = self.aspirante;
            swal({
                title: '¿Estás seguro?',
                text: "Esta acción cambiará tu información en el sistema.",
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
                        url: '/aspirante/modificar',
                        datatype: 'json',
                        data: {
                            aspirante: aux,
                        },
                        headers: { "X-CSRFToken": self.token }
                    }).then(function(respuesta) {
                        if (respuesta.data == "ok") {
                            swal({
                                title: 'Bien!',
                                text: 'Has cambiado el aspirante.',
                                type: 'success'
                            }).then((result) => {
                                localStorage.clear();
                                location.reload();
                            })
                        } else {
                            swal(
                                'Ups...',
                                'No se hicieron cambios.',
                                'error'
                            )
                        }
                    })
                }
            })
        },
        cargar_aspirante() {
            var self = this;
            axios({
                method: "POST",
                url: "/aspirante/cargar",
                headers: { "X-CSRFToken": self.token }
            }).then((respuesta) => {
                self.aspirante = respuesta.data;
            })
        }

    }
})
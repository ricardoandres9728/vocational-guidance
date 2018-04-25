const vm = new Vue({
    el: 'main',
    data: {
        token: $("#csrf").val(),
        aspirante: {
            nombre: '',
            documento: '',
            correo: '',
            password: ''
        },
        aspirantes: [],
    },
    created() {
        this.cargar_aspirante();
    },
    methods: {
        desactivar_aspirante(id) {
            var self = this
            var aux = self.aspirantes[id]
            swal({
                title: '¿Estás seguro?',
                text: "Esta acción desactivará el aspirante en el sistema, si estás seguro que el proceso ha terminado da click en Confirmar",
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
                        url: '/administrador/aspirante/desactivar',
                        datatype: 'json',
                        data: {
                            aspirante: aux,
                        },
                        headers: {
                            "X-CSRFToken": self.token
                        }
                    }).then(function (respuesta) {
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
                text: "Esta acción cambiará el aspirante en el sistema, si estás seguro que el proceso ha terminado da click en Confirmar",
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
                        url: '/administrador/aspirante/modificar',
                        datatype: 'json',
                        data: {
                            aspirante: aux,
                        },
                        headers: { "X-CSRFToken": self.token }
                    }).then(function (respuesta) {
                        if (respuesta.data == "ok") {
                            swal({
                                title: 'Bien!',
                                text: 'Has cambiado el aspirante.',
                                type: 'success'
                            }).then((result) => {
                                localStorage.clear();
                                location.reload();
                            })
                        }
                        else {
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
        asignar_aspirante(id) {
            var self = this;
            aux = self.aspirantes[id];
            self.aspirante = aux;
            var div = document.getElementById("div-editar-aspirante");
            div.setAttribute("style", "display: block");
        },
        cargar_aspirante() {
            var self = this;
            axios({
                method: "POST",
                url: "/administrador/aspirante/cargar/todos",
                headers: { "X-CSRFToken": self.token }
            }).then((respuesta) => {
                respuesta.data.forEach((element) => {
                    self.aspirantes.push(element);
                })
            })
        },
    }
})
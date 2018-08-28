const vm = new Vue({
    el: 'main',
    data: {
        token: $("#csrf").val(),
        colegio: {
            nombre: '',
            documento: '',
            correo: '',
            password: {
                anterior: '',
                nueva: '',
            },
        },
        aspirantes:[]
    },
    created() {
        this.cargar_colegio();
        this.cargar_aspirantes();
    },
    methods: {
        cargar_aspirantes() {
            var self = this;
            axios({
                method: "POST",
                url: "/colegio/cargar/aspirantes",
                headers: { "X-CSRFToken": self.token }
            }).then((respuesta) => {
                respuesta.data.forEach((element) => {
                    self.aspirantes.push(element);
                })
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
                        url: '/colegio/cambiar/password',
                        datatype: 'json',
                        data: {
                            password: self.colegio.password,
                        },
                        headers: { "X-CSRFToken": self.token }
                    }).then(function (respuesta) {
                        if (respuesta.data == "ok") {
                            swal({
                                title: 'Bien!',
                                text: 'Has cambiado el colegio.',
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
        modificar_colegio() {
            var self = this
            var aux = self.colegio;
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
                        url: '/colegio/modificar',
                        datatype: 'json',
                        data: {
                            colegio: aux,
                        },
                        headers: { "X-CSRFToken": self.token }
                    }).then(function (respuesta) {
                        if (respuesta.data == "ok") {
                            swal({
                                title: 'Bien!',
                                text: 'Has cambiado el colegio.',
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
        cargar_colegio() {
            var self = this;
            axios({
                method: "POST",
                url: "/colegio/cargar",
                headers: { "X-CSRFToken": self.token }
            }).then((respuesta) => {
                self.colegio = respuesta.data;
            })
        },
    }
})
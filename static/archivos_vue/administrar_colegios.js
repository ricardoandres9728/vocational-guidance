const vm = new Vue({
    el: 'main',
    data: {
        token: $("#csrf").val(),
        colegio:{
            nombre:'',
            correo:'',
            password:''
        },
        colegios:[],
    },
    created(){
        this.cargar_colegios();
    },
    methods:{
        desactivar_colegio(id) {
            var self = this
            var aux = self.colegios[id]
            swal({
                title: '¿Estás seguro?',
                text: "Esta acción desactivará el colegio en el sistema, si estás seguro que el proceso ha terminado da click en Confirmar",
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
                        url: '/administrador/colegio/desactivar',
                        datatype: 'json',
                        data: {
                            colegio: aux,
                        },
                        headers: {
                            "X-CSRFToken": self.token
                        }
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
        modificar_colegio() {
            var self = this
            var aux = self.colegio;
            swal({
                title: '¿Estás seguro?',
                text: "Esta acción cambiará el colegio en el sistema, si estás seguro que el proceso ha terminado da click en Confirmar",
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
                        url: '/administrador/colegio/modificar',
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
        asignar_colegio(id){
            var self = this;
            aux = self.colegios[id];
            self.colegio = aux;
            var div = document.getElementById("div-editar-colegio");
            div.setAttribute("style", "display: block");
        },
        cargar_colegios(){
            var self = this;
            axios({
                method: "POST",
                url: "/administrador/colegio/cargar/todos",
                headers: { "X-CSRFToken": self.token }
            }).then((respuesta) => {
                respuesta.data.forEach((element) => {
                    self.colegios.push(element);
                })
            })
        },
        registrar_colegio(){
            var self = this;
            let password = document.getElementById("password");
            let confirmar = document.getElementById("confirmar");
            if (confirmar.value != password.value){
                confirmar.setAttribute("class", "form-control parsley-error");
                password.setAttribute("class", "form-control parsley-error");
                swal(
                    'Ups...',
                    'Las contraseñas deben ser iguales.',
                    'error'
                )
            }
            else{
                let aux = self.colegio;
                axios({
                    method: 'post',
                    url: '/administrador/colegio/registrar',
                    datatype: 'json',
                    data: {
                        colegio: aux,
                    },
                    headers: { "X-CSRFToken": self.token }
                }).then(function (respuesta) {
                    if (respuesta.data == "ok") {
                        swal({
                            title: 'Bien!',
                            text: 'Has registrado el colegio.',
                            type: 'success'
                        }).then((result) => {
                            location.reload();
                        })
                    }
                    else {
                        let nombre = document.getElementById("nombre");
                        nombre.setAttribute("class", "form-control parsley-error");
                        swal(
                            'Ups...',
                            respuesta.data,
                            'error'
                        )
                    }
                })
            }
        },
    }
})

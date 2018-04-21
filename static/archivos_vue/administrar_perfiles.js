const vm = new Vue({
    el: 'main',
    data: {
        token: $("#csrf").val(),
        perfiles:[],
        perfil:{
            id:'',
            nombre:'',
            live:''
        }
    },
    created(){
        this.cargar_perfiles();
    },
    methods:{
        desactivar_perfil(id){
            var self = this
            var aux = self.perfiles[id]
            swal({
                title: '¿Estás seguro?',
                text: "Esta acción desactivará el perfil en el sistema, si estás seguro da click en Confirmar",
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
                        url: '/administrador/perfil/desactivar',
                        datatype: 'json',
                        data: {
                            perfil: aux,
                        },
                        headers: { "X-CSRFToken": self.token }
                    }).then(function (respuesta) {
                        if (respuesta.data == "ok") {
                            swal({
                                title: 'Bien!',
                                text: 'Has cambiado el perfil.',
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
        modificar_perfil(){
            var self = this
            var aux = self.perfil
            swal({
                title: '¿Estás seguro?',
                text: "Esta acción guardará el perfil en el sistema, si estás seguro que el proceso ha terminado da click en Confirmar",
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
                        url: '/administrador/perfil/modificar',
                        datatype: 'json',
                        data: {
                            perfil: aux,
                        },
                        headers: { "X-CSRFToken": self.token }
                    }).then(function (respuesta) {
                        if (respuesta.data == "ok") {
                            swal({
                                title: 'Bien!',
                                text: 'Has cambiado el perfil.',
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
        cargar_perfiles() {
            var self = this;
            axios({
                method: "POST",
                url: "/administrador/perfil/cargar/todos",
                headers: { "X-CSRFToken": self.token }
            }).then((respuesta) => {
                respuesta.data.forEach((element) => {
                    self.perfiles.push(element);
                })
            })
        },
        asignar_perfil(id){
            var self = this;
            aux = self.perfiles[id];
            self.perfil = aux
            var div = document.getElementById("div-editar-perfil");
            div.setAttribute("style", "display: block");
        }
    },
});
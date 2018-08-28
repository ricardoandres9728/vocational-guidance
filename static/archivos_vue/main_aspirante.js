const vm = new Vue({
    el: 'main',
    data: {
        token: $("#csrf").val(),
        aspirante: {
            nombres: '',
            apellidos: '',
            documento: '',
            correo: '',
            password:{
                anterior:'',
                nueva:'',
            },
            newsletter:''
        },
        encuestas:[],
        encuesta:{
            id: 0,
            preguntas:{},
            perfil:'',
        },
        id_pregunta:0,
        pregunta:{},
        rta:{
            rta:'',
            pta:'',
        },
    },
    created() {
        this.cargar_aspirante();
        this.cargar_encuestas();
    },
    methods: {
        next(){
            var self = this;
            if(self.id_pregunta+1<self.encuesta.preguntas.length){
            self.id_pregunta++;
            self.mostrar_encuesta();
            }
        },
        mostrar_encuesta(){
            var self = this;
            aux = self.encuesta.preguntas[self.id_pregunta];
            self.pregunta = aux;
        },
        asignar_encuesta() {
            var self = this;
            aux = self.encuestas[self.encuesta.id];
            self.encuesta = aux;
            console.log(self.encuesta.id);
        },
        cargar_encuestas() {
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
        newsletter(){
            var self = this;
            axios({
                method: 'post',
                url: '/aspirante/newsletter',
                headers: { "X-CSRFToken": self.token }
            })
        },
        cambiar_password(){
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
        cargar_aspirante() {
            var self = this;
            axios({
                method: "POST",
                url: "/aspirante/cargar",
                headers: { "X-CSRFToken": self.token }
            }).then((respuesta) => {
                self.aspirante = respuesta.data;
            })
        },
    }
})
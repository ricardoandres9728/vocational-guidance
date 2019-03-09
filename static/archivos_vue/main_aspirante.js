const vm = new Vue({
    el: 'main',
    data: {
        token: $("#csrf").val(),
        aspirante: {
            nombres: '',
            apellidos: '',
            correo: '',
            password:{
                anterior:'',
                nueva:'',
            },
            newsletter:''
        },
        encuestas:[],
        encuesta: null,
        id_encuesta: 0,
        id_pregunta:0,
        pregunta:{},
        rta:{
            rta:'',
            pta:'',
        },
        respuesta_pregunta:{
            id_pregunta:"",
            respuesta: "1"
        },
        respuestas_encuesta:{
            id_encuesta:0,
            respuestas:[]
        }
    },
    created() {
        this.cargar_aspirante();
        this.cargar_encuestas();
    },
    methods: {
        next(){
            this.respuesta_pregunta.id_pregunta = this.id_pregunta;
            this.respuestas_encuesta.respuestas.push(JSON.parse(JSON.stringify(this.respuesta_pregunta)));
            this.id_pregunta ++;
        },
        finalizar_encuesta(){
            this.respuesta_pregunta.id_pregunta = this.id_pregunta;
            this.respuestas_encuesta.respuestas.push(JSON.parse(JSON.stringify(this.respuesta_pregunta)));
        },
        mostrar_encuesta(){
            this.encuesta = this.encuestas[this.id_encuesta];
            this.respuestas_encuesta.id_encuesta = this.encuesta.id;
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

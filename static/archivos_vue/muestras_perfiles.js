const vm1 = new Vue({
    el: "#main",
    data() {
        return {
            encuestas: [],
            token: $("#csrf").val(),
            selectedEncuesta: null,
            preguntas: [],
            perfiles: [],
            muestras: [],
            newMuestra: {
                respuestas: {},
                perfil_id: null
            }
        }
    },
    methods: {
        loadData() {
            axios({
                url: "/administrador/encuesta/cargar/todos",
                method: "POST",
                headers: { "X-CSRFToken": this.token }
            }).then((respuesta) => {
                this.encuestas = respuesta.data;
                this.preguntas = respuesta.data.preguntas;
            })
        },
        cargarMuestras(selectedEncuesta) {
            axios({
                method: "POST",
                url: "/administrador/encuesta/cargar/muestras",
                data: { encuesta: selectedEncuesta },
                headers: { "X-CSRFToken": this.token }
            }).then(respuesta => {
                this.muestras = respuesta.data
            })

        },
        encuestaCambiada(event) {
            this.selectedEncuesta = this.encuestas[event.target.value]
            this.cargarMuestras(this.selectedEncuesta.id)
        },
        agregarMuestra() {
            this.newMuestra.encuesta_id = this.selectedEncuesta.id;
            axios({
                method: "POST",
                url: "/administrador/encuesta/crear/muestras",
                data: this.newMuestra,
                headers: { "X-CSRFToken": this.token }
            }).then(respuesta => {
                this.cargarMuestras(this.selectedEncuesta.id)
                this.newMuestra = {
                    respuestas: {},
                    perfil_id: null
                }
            })
        },
        eliminarMuestra(id) {
            axios({
                method: "POST",
                url: "/administrador/encuesta/eliminar/muestras",
                data: { encuesta: id },
                headers: { "X-CSRFToken": this.token }
            }).then(respuesta => {
                this.cargarMuestras(this.selectedEncuesta.id)
            })
        },
        entrenarMuestra() {
            axios({
                method: "POST",
                url: "/administrador/encuesta/entrenar/muestras",
                data: { encuesta: this.selectedEncuesta.id },
                headers: { "X-CSRFToken": this.token }
            }).then(respuesta => {
                this.cargarMuestras(this.selectedEncuesta.id)
            })
        }
    },
    mounted() {
        axios({
            method: "POST",
            url: "/administrador/perfil/cargar/todos",
            headers: { "X-CSRFToken": this.token }
        }).then(respuesta => {
            this.perfiles = respuesta.data
        })
        this.loadData();
    }
})
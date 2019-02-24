const vm = new Vue({
    el: 'main',
    data: {
        token: $("#csrf").val(),
        colegios: 0,
        correo: '',
        aspirantes: 0,
        encuestas: 0,
        perfiles: 0,
        feedback:[],
        password:{
            anterior:'',
            nueva:''
        }
    },
    created() {
        this.cargar_principal();
    },
    methods: {

        cargar_principal(){
            var self = this;
            axios({
                method: "POST",
                url: "/administrador/principal/cargar",
                headers: { "X-CSRFToken": self.token }
            }).then((respuesta) => {
                self.aspirantes = respuesta.data.aspirantes;
                self.encuestas = respuesta.data.encuestas;
                self.colegios = respuesta.data.colegios;
                self.perfiles = respuesta.data.perfiles;
                self.feedback = respuesta.data.feedback;
                self.correo = respuesta.data.correo;
        })
        },
    }
})

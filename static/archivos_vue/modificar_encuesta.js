const vm = new Vue({
    el: 'main',
    data: {
        token: $("#csrf").val(),
        pregunta_editar: {
            id: '',
            pregunta: {}
        },
        encuesta: {
            perfil: '',
            preguntas: [],
        },
    },
})
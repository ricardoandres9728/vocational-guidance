const vm1 = new Vue({
    el: "#main",
    data() {
        return {
            encuestas: []
        }
    },
    methods: {
        loadData() {
            Axios({
                url: "/"
            })
        }
    },
    mounted() {
        this.loadData();
    }
})
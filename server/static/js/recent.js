let fresh = new Vue({
    delimiters:['[[', ']]'],
    el: '#right-content',
    data: {
        items:[['Loading', '']]
    },
    methods:{
        refresh:function (m) {
            this.items = m
        }
    }
});

let socket = io('fycx.mynetgear.com:28000');
socket.on('update', function (message) {
    fresh.refresh(message);
});

let like = new Vue({
    delimiters:['[[', ']]'],
    el: '#like',
    data: {
        isLike: false,
        hey:'aaa'
    },
    methods:{
        upvote:function () {
            socket.emit('message', {data:123})
        }
    }
});

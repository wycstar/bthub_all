let fresh = new Vue({
    delimiters:['[[', ']]'],
    el: '#right-content',
    data: {
        items:[['Loading', '']]
    },
    methods:{
        refresh:function (m) {
            this.items = m;
        }
    },
    computed:{
        hItems:function () {
            return this.items.map(function (i) {
                a = [];
                a.push(i[0]);
                moment.locale('zh-cn');
                a.push(moment(i[1], "X").fromNow());
                return a
            })
        }
    }
});

let socket = io('https://www.bthub.me');
socket.on('update', function (message) {
    fresh.refresh(message);
    console.log(message)
});

let l = new Vue({
    delimiters:['[[', ']]'],
    el: "#bonus",
    components:{
        likeit:{
            delimiters:['[[', ']]'],
            props: ['count', 'infohash'],
            data:function () {
                return {isLiked:false,
                        vCount:this.count,
                        unlikeClass: "fa-heart-o",
                        likeClass: "fa-heart"}
            },
            template:`
            <div class="like-button fl wide-animate" id="like">
                <span class="heart-zone">
                    <a v-on:click="upvote()"><i class="fa" v-bind:class="[isLiked ? likeClass : unlikeClass]" aria-hidden="true"></i>喜欢 |</a>
                </span>
                <span class="num-zone">[[ vCount ]]</span>
            </div>
            `,
            methods:{
                upvote:function () {
                    switch(this.check(this.infohash)){
                        case 0:
                            document.cookie = this.infohash + '=1;';
                            this.isLiked = true;
                            this.vCount += 1;
                            socket.emit('like', this.infohash);
                            break;
                        case 1:
                            document.cookie = this.infohash + '=1;';
                            this.isLiked = true;
                            this.vCount += 1;
                            socket.emit('like', this.infohash);
                            break;
                        case 2:
                            document.cookie = this.infohash + '=0;';
                            this.isLiked = false;
                            this.vCount -= 1;
                            socket.emit('unlike', this.infohash);
                            break;
                    }
                },
                check:function (m) {
                    if(document.cookie.length > 0){
                        let start = document.cookie.indexOf(m+'=');
                        if(start === -1){
                            return 0;
                        }
                        else{
                            start = start + m.length + 1;
                            return parseInt(document.cookie.substr(start, 1)) + 1
                        }
                    }else{
                        return 0;
                    }
                }
            },
            mounted:function () {
                this.isLiked = (this.check(this.infohash) === 2);
            }
        }
    }
});

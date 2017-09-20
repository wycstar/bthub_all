$("#code").qrcode({
    render: "table",
    width: 200,
    height: 200,
    text: window.location.href
});
let wo = $("#wx-overlay");
let ws = $("#wx-share");
function openWXShareWindow() {
    wo.css("z-index", 10000);
    ws.css("z-index", 10001);
    wo.fadeTo(500, 0.5);
    ws.fadeTo(500, 1.0);
}
function az() {
    wo.css("z-index", 0);
    ws.css("z-index", 0);
}
function closeWXShareWindow() {
    wo.fadeTo(500, 0);
    ws.fadeTo(500, 0);
    setTimeout("az()", 500);
}
function openWBShareWindow() {
    let s = 'http://v.t.sina.com.cn/share/share.php?title=我发现一个很好的关于《' + document.title.slice(0, -15) + '》的资源!&url=' + window.location.href + '&content=utf-8&sourceUrl=' + window.location.href;
    window.open(s, 'newwindow', 'height=400,width=400,top=100,left=100');
}
// function like() {
//     socket.emit('message', {data:123})
// }

$("#code").qrcode({
    render: "table",
    width: 200,
    height: 200,
    text: window.location.href
});
let wo = $("#wx-overlay");
let ws = $("#wx-share");
let dw = $("#donate");
function openWXShareWindow() {
    wo.fadeIn();
    ws.fadeIn();
}
function closeWXShareWindow() {
    wo.fadeOut();
    ws.fadeOut();
}
function openWBShareWindow() {
    let s = 'http://v.t.sina.com.cn/share/share.php?title=我在BTHUB发现一个很好的关于《' + document.title.slice(0, -15) + '》的资源!&url=' + window.location.href + '&content=utf-8&sourceUrl=' + window.location.href;
    window.open(s, 'newwindow', 'height=400,width=400,top=100,left=100');
}
function openDonateWindow() {
    wo.fadeIn();
    dw.fadeIn();
}
function closeDonateWindow() {
    wo.fadeOut();
    dw.fadeOut();
}
dal = ["2", "5", "10", "20", "50", "100", "200", "500", "自定"];
dali = 0;
dat = "wx";
function donateRoll(d) {
    d === 0 ? dali++ : dali--;
    if(dali < 0){
        dali = 8;}
    else if (dali > 8){
        dali = 0;}
    $("#dfs").text(dal[dali]);
    setDonateQr();
}
function donateMethod(obj) {
    if(obj.value === "wx-pay"){
        dat = "wx";
    }
    else if(obj.value === "ali-pay"){
        dat = "ali";
    }
    setDonateQr();
}
function setDonateQr() {
    let dfq = $(".df-qrcode");
    let prefix = window.location.protocol + "//" + window.location.host + "/static/img/pay/";
    dfq.fadeOut(100);
    $("#donate-qrcode").attr("src", prefix + dat + "-" + (dali === 8 ? "ud" : dal[dali]) + ".png");
    dfq.fadeIn(100);
}

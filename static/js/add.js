<script src="https://cdn.jsdelivr.net/npm/js-cookie@beta/dist/js.cookie.min.js"></script>
function addToCar(item){
    //item為品項名稱，型態為字串
if(Cookies.get("carItem") == undefined){
            //若目前沒有 carItem 這個 key 的 Cookie ，直接新增一個，並只對購物車頁面設定 Cookie
    Cookies.set("carItem", item, { path: '/shopcar' })
}
else{
            //有的話就用逗號將品項做分隔再加入至 carItem 中
    currentItem = Cookies.get("carItem");
    currentItem = currentItem+","+item; 
    Cookies.set("carItem", currentItem, { path: '/shopcar' });
}
alert("已加至購物車");
}
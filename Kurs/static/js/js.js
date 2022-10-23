var i = 0;
update();
function update(){
    console.log(i)
    i++;
    setTimeout(update, 1000);
}

function get_random_tile(){
        return(tiles[Math.floor(Math.random() * tiles.length)]);
}

var slots = $("td"),
    slot  = undefined
    i     = 0,
    tiles = ["water","grass", "sand", "rocks", "mountains","dirt", "forest", "snow", "ice"];
    
for(i = 0; i < slots.length; i++){
    $(slots[i]).addClass(get_random_tile());
}

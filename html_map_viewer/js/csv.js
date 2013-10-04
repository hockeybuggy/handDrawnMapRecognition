
var i,
    j,
    csvUrl,
    csvStr,
    rows,
    row,
    table = [];

csvUrl = "csv/" +  RegExp("file=(.+)").exec(window.location.search)[1];
$.get(csvUrl, function(data){
    csvStr = $.trim(data);
    rows = csvStr.split("\n");
    for(i = 0; i < rows.length; i += 1){
        row = rows[i].split(",");
        if(i == 0){
            create_table(row.length, rows.length); // Assume the map is rectangular
        }
        table.push(row);
    }
    //console.log(table);
    draw_table(table);
});

function create_table(width, height){
    var i,
        j,
        table = ["<table>"];

    for(i = 0; i < height; i += 1){
        table.push("<tr>");
        for(j = 0; j < width; j += 1){
            table.push("<td id='" + i + "-" + j + "'>-</td>");
        }
        table.push("</tr>");
    }
    table.push("</table>");

    $("#csv-container").html(table.join("")); // Put table into container
}

function draw_table(){
    var i, j;
    for(i=0; i < table.length; i+=1){
        for(j=0; j < table[i].length; j+=1){
            $("#"+i+"-"+j).text(table[i][j]); // Insert into cell
        }
    }
}

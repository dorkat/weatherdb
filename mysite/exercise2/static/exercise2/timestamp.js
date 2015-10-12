/**
 * Created by dor on 9/1/15.
 */


$(document).ready(function(){
    $("#update_button").click(function(){
        var country = document.getElementById("country").options[document.getElementById("country").selectedIndex].text;
        var city = document.getElementById("city").options[document.getElementById("city").selectedIndex].text;
        var url = "http://192.168.200.128:8000/exercise2/temp/?country=" + country + "&city=" + city;
        var request = new XMLHttpRequest;
        request.onreadystatechange = function () {
            var DONE = this.DONE || 4;
            if (this.readyState === DONE) {
                console.log("update temperature and humidity request for " + city + " ready");
                var temp_and_hum = request.responseText;
                temp_and_hum = temp_and_hum.split(',');
                temp_and_hum[0] = temp_and_hum[0].substring(2, temp_and_hum[0].length - 1);
                temp_and_hum[1] = temp_and_hum[1].substring(3, temp_and_hum[1].length - 2);
                var table = document.getElementById("temp_table");
                for (var i = 0, row; row = table.rows[i]; i++){
                 if (row.cells[0].innerHTML == country && row.cells[1].innerHTML == city) {
                     row.cells[2].innerHTML = temp_and_hum[0];
                     row.cells[3].innerHTML = temp_and_hum[1];
                     console.log("updated " + city);
                 }
                }
            }
        };
        request.open("GET", url, true);
        request.send(null);
    });
});

$(document).ready(function(){
    $("#time_button").click(function(){
        t = document.innerHTML=Date();
        $("#date").text(t);
    });
});

function ToTable(city_id) {
    var url = "http://192.168.200.128:8000/exercise2/info/?id=" + city_id;
    var request = new XMLHttpRequest;
    request.onreadystatechange = function () {
        var DONE = this.DONE || 4;
        if (this.readyState === DONE) {
            var info = request.responseText;
            info = info.substring(1, info.length - 1);
            info = info.split(',');
            info[0] = info[0].substring(2, info[0].length - 1);
            info[1] = info[1].substring(3, info[1].length - 1);
            info[2] = info[2].substring(2, info[2].length - 1);
            info[3] = info[3].substring(3, info[3].length - 1);
            var table = document.getElementById("temp_table");
            var row = table.insertRow(-1);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            var btn = document.createElement("button");
            btn.title = "delete " + info[1];
            btn.setAttribute("class", "btn btn-danger glyphicon glyphicon-remove btn-xs");
            cell1.innerHTML = info[0];
            cell2.innerHTML = info[1];
            cell3.innerHTML = info[2];
            cell4.innerHTML = info[3];
            cell5.appendChild(btn);
            console.log(info[1] + " updated to table")
        }
    };
    request.open("GET", url, true);
    request.send(null);
}

$(document).ready(function(){
    $("#temp_table").on('click', 'button',function(){
        var i = this.parentNode.parentNode.rowIndex;
        var country = document.getElementById("temp_table").rows[i].cells[0].innerHTML;
        var city = document.getElementById("temp_table").rows[i].cells[1].innerHTML;
        document.getElementById("temp_table").deleteRow(i);
        var url = "http://192.168.200.128:8000/exercise2/remove?name=" + city + "&country=" + country;
        var request = new XMLHttpRequest;
        request.onreadystatechange = function () {
            var DONE = this.DONE || 4;
            if (this.readyState === DONE) {
                console.log(city + " removed");
                alert(city + " removed");
            }
        };
        request.open("GET", url, true);
        request.send(null);
    });
});

$(document).ready(function(){
    var request = new XMLHttpRequest;
    request.onreadystatechange = function () {
        var DONE = this.DONE || 4;
        if (this.readyState === DONE) {
            var ct_arr = request.responseText;
            ct_arr = ct_arr.substring(1, ct_arr.length - 1);
            ct_arr = ct_arr.split(',');
            for (i = 0; i < ct_arr.length; i++)
                ToTable(ct_arr[i])
            console.log("city table information retrieved from db")
        }
    };
    request.open("GET", "http://192.168.200.128:8000/exercise2/retrieve/", true);
    request.send(null);
});

$(document).ready(function(){
    $("#add_city_button").click(function(){
        var country = document.getElementById("country").options[document.getElementById("country").selectedIndex].text;
        var city = document.getElementById("city").options[document.getElementById("city").selectedIndex].text;
        var add_city_check = true;
        var table = document.getElementById("temp_table");
        for (var i = 0, row; row = table.rows[i]; i++){
            if (row.cells[0].innerHTML == country && row.cells[1].innerHTML == city){
                add_city_check = false;
            }
        }
        if (add_city_check) {
            var url = "http://192.168.200.128:8000/exercise2/temp/?country=" + country + "&city=" + city;
            var request = new XMLHttpRequest;
            request.onreadystatechange = function () {
                var DONE = this.DONE || 4;
                if (this.readyState === DONE) {
                    console.log("add city request for " + city + " ready");
                    var temp_and_hum = request.responseText;
                    temp_and_hum = temp_and_hum.split(',');
                    temp_and_hum[0] = temp_and_hum[0].substring(2, temp_and_hum[0].length - 1);
                    temp_and_hum[1] = temp_and_hum[1].substring(3, temp_and_hum[1].length - 2);
                    var table = document.getElementById("temp_table");
                    var row = table.insertRow(-1);
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);
                    var cell3 = row.insertCell(2);
                    var cell4 = row.insertCell(3);
                    var cell5 = row.insertCell(4);
                    var btn = document.createElement("button");
                    btn.title = "delete " + city;
                    btn.setAttribute("class", "btn btn-danger glyphicon glyphicon-remove btn-xs");
                    cell1.innerHTML = country;
                    cell2.innerHTML = city;
                    cell3.innerHTML = temp_and_hum[0];
                    cell4.innerHTML = temp_and_hum[1];
                    cell5.appendChild(btn);
                    console.log("add city request for " + city + " done")
                }
            };
            request.open("GET", url, true);
            request.send(null);

            var save_url = "http://192.168.200.128:8000/exercise2/store/?country=" + country + "&name=" + city;
            var save_request = new XMLHttpRequest;
            save_request.open("GET", save_url, true);
            save_request.send(null);
            console.log(city + " was saved to the database")
        }
        else {
            console.log(city + " is already in the table");
            alert(city + " is already in the table")
        }
    });
});

$(document).ready(function() {
    var request = new XMLHttpRequest;
    request.onreadystatechange = function () {
    var DONE = this.DONE || 4;
    if (this.readyState === DONE){
    console.log("country list request ready");
    var country_list = request.responseText;
    country_list = country_list.substring(0, country_list.length -1);
    country_list = country_list.split(',');
    var country = document.myform.country;
    for (i = 0; i < country_list.length; i++) {
        country_list[i] = country_list[i].substring(3, country_list[i].length-1);
        country.options[country.options.length] = new Option(country_list[i], country_list[i], false, false)
    }
    console.log("country list request done")
}
    };
    request.open("GET", "http://192.168.200.128:8000/exercise2/country_list/", true);
    request.send(null);
});

$(document).ready(function() {
    document.getElementById("country").onchange = function () {
        document.myform.city.options.length = 0;
            if (document.getElementById("country").value == "") {city.options[city.options.length] = new Option("", "", false, false)
            }
            else {
                var x = document.getElementById("country").value;
                var request = new XMLHttpRequest;
                request.onreadystatechange = function () {
                    var DONE = this.DONE || 4;
                    if (this.readyState === DONE) {
                        console.log("city list request for " + x + " ready");
                        var city_list = request.responseText;
                        city_list = city_list.substring(0, city_list.length - 1);
                        city_list = city_list.split(',');
                        for (i = 0; i < city_list.length; i++) {
                            city_list[i] = city_list[i].substring(3, city_list[i].length - 1);
                            city.options[city.options.length] = new Option(city_list[i], city_list[i], false, false)
                        }
                        console.log("city list request for " + x + " done")
                    }
                };
                var url = "http://192.168.200.128:8000/exercise2/city_list/?name=" + x;
                request.open("GET", url, true);
                request.send(null);
            }
    };
});

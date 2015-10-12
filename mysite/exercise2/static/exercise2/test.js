/**
 * Created by dor on 9/6/15.
 */



$(document).ready(function() {
    var request = new XMLHttpRequest;
    request.onreadystatechange = function () {
    var DONE = this.DONE || 4;
    if (this.readyState === DONE){
    console.log("country list request ready");
    var country_list = request.responseText;
    country_list = country_list.substring(0, country_list.length -1);
    country_list = country_list.split(',');
    var options = "";
    for (i = 0; i < country_list.length; i++) {
        country_list[i] = country_list[i].substring(3, country_list[i].length-1);
        options += '<option value="'+country_list[i]+'" />';
    }
    document.getElementById('country').innerHTML = options;
    console.log("country list request done")
}
    };
    request.open("GET", "http://192.168.200.128:8000/exercise2/country_list/", true);
    request.send(null);
});

$(document).ready(function() {
    document.getElementById("country_input").onchange = function () {
            if (document.getElementById("country").value == "") {city.options[city.options.length] = new Option("", "", false, false)
            }
            else {
                var x = document.getElementById("country_input").value;
                console.log(x);
                var request = new XMLHttpRequest;
                request.onreadystatechange = function () {
                    var DONE = this.DONE || 4;
                    if (this.readyState === DONE) {
                        console.log("city list request for " + x + " ready");
                        var city_list = request.responseText;
                        city_list = city_list.substring(0, city_list.length - 1);
                        city_list = city_list.split(',');
                        var options = "";
                        for (i = 0; i < city_list.length; i++) {
                            city_list[i] = city_list[i].substring(3, city_list[i].length - 1);
                            options += '<option value="'+city_list[i]+'" />';
                        }
                        document.getElementById('city').innerHTML = options;
                        console.log("city list request for " + x + " done")
                    }
                };
                var url = "http://192.168.200.128:8000/exercise2/city_list/?name=" + x;
                request.open("GET", url, true);
                request.send(null);
            }
    };
});


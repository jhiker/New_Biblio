var data = {
    {
        maplist
    }
}
$(document).ready(function () {
        var latitude = parseFloat("51.515252");
        var longitude = parseFloat("-0.189852");

        var latlngPos = new google.maps.LatLng(latitude, longitude);

        // Set up options for the Google map
        var myOptions = {
            zoom: 5,
            center: latlngPos,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        // Define the map
        map = new google.maps.Map(document.getElementById("map"), myOptions);
        data.forEach(function (p) {
                var pinColor = "FE7569";
                var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
                    new google.maps.Size((Math.round(5 + 20 * p.pinvar)), Math.round((5 + 30 * p.pinvar))),
                    new google.maps.Point(0, 0),
                    new google.maps.Point(10, 34));
                var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
                    new google.maps.Size(Math.round(5 * 40 * p.pinvar)), Math.round(5 + p.pinvar * 37)),
                    new google.maps.Point(0, 0),
                    new google.maps.Point(12, 35));
            var point = new google.maps.LatLng(p.lat, p.lng);
            var marker = new google.maps.Marker({
                position: point,
                map: map,
                url: p.url,
                title: p.name,
                icon: pinImage,
                shadow: pinShadow

            }); google.maps.event.addListener(marker, 'click', function () {
                window.location.href = marker.url;

                var html = "<div class='infowin'><strong>" + p.name + "</strong><hr>";
                html = html + pointData.description
                bindInfoWindow(marker, map, infoWindow, html);
            }); google.maps.event.addListener(marker, 'mouseover', function () {
                infoWindow.setContent(html);
                infoWindow.open(map, marker);
            }); google.maps.event.addListener(marker, 'mouseout', function () {
                infoWindow.close();
            })
        });
            
            
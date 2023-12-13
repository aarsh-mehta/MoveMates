   function createPassengerTripTable(trips, title, elementID) {

        if (trips.length === 0) {
            return null;
        } else {
            let table = "<table class='table table-hover'>";
            table += '<br>';
            table += `<h3>${title}</h3>`;
            table += "<th><i class='far fa-calendar fa-2x'></i></th>";
            table += "<th><i class='far fa-clock fa-2x'></i></th>";
            table += "<th><i class='fas fa-map-marker-alt fa-2x'></i></th>";
            table += "<th><i class='fas fa-map-marked-alt fa-2x'></i></th>";
            table += "<th><i class='fas fa-car fa-2x'></i></th>";

            


function clickhere(){
    var availability = String(document.querySelector('input[name="availablity"]:checked').value);
    var furnishing = String(document.querySelector('input[name="FD"]:checked').value);
    var transaction = String(document.querySelector('input[name="trans"]:checked').value);
    var bathroom =  parseInt(document.getElementById('bath').value);

    var bhk = parseInt(document.getElementById('bedroom').value);
    var total_sqft = parseFloat(document.getElementById('area').value);
    var location = document.getElementById('uilocation');
    var estimated = document.getElementById('estimated');
    console.log("Estimate Price Button Clicked");
    
    var url = 'https://bhopal-ka-khabri.herokuapp.com/predict_home_price';
    $.post(url,{
        avail: availability,
        furnish: furnishing,
        trans : transaction,
        bath : bathroom,
        bedroom: bhk,
        sqft:total_sqft,
        loc: location.value,
    },function(data,status){
        console.log("let's calculate.")
        console.log(data.estimated_price);
        estimated.innerHTML= "<h1>You can buy this kind of house at approximately <br><u>"+ data.estimated_price.toString()+" Lakh Rupees</u></h1>";
        console.log(status)
    })

}
function onPageLoad(){
    console.log("document loaded");
    var url = "https://bhopal-ka-khabri.herokuapp.com/get_location_name";
    $.get(url,function(data,status){
        console.log("got a response for get_location_names request");
        if(data){
            var locations = data.locations;
            var uilocation = document.getElementById('uilocation');
            $('#uilocation').empty();
            for(var i in locations){
                var opt = new Option(locations[i]);
                $('#uilocation').append(opt)
            }
        }
    });
}

window.onload = onPageLoad;


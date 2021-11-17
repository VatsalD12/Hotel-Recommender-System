const btn=document.getElementById("btn1");

const input_city=document.getElementById("city");
const input_address=document.getElementById("address");
const input_necessity=document.getElementById("necessity");
const input_guests=document.getElementById("guests");

const mapDiv=document.getElementById("mapDiv");
const map=document.getElementById("map");
const tbody=document.getElementById('tbody');
const tableDiv=document.getElementById("tableDiv");
const loading=document.getElementById("loading");
let mymap;
// Display Places
const displayPlaces=(places)=>{
    tableDiv.style.display="block"
    tbody.innerHTML="";
    places.forEach(ele=>{
        const tr=document.createElement("tr")
        tr.innerHTML=`
        <td>${ele.hotel}</td>
        <td>${ele.cityName}</td>
        <td>${ele.hotelAddress}</td>
        <td>${ele.dist.toFixed(2)}</td>
        <td>${ele.roomType}</td>
        <td>${ele.rate==0?100:ele.rate}</td>
        <td>${ele.rating}/5</td>
        <td><a href=${ele.hotel_url}>Book from here</a></td>
        
        `
        tbody.appendChild(tr)
    })
}


// Plot Map
const plotMap=(places)=>{
    
    mapDiv.style.display="block"
    // Access Token
    let accessToken="pk.eyJ1IjoiamF5cGFqamkiLCJhIjoiY2thNnpuaW85MDR6OTJwbXpiajhtaXdhZiJ9.uW0aB84Ow8lWrqmiaPORMw"
    // Maps
    if(mymap!==undefined){
        mymap.remove()
    }
    mymap = L.map('map').setView(places[0].coordinates, 15);
    // Tile
    L.tileLayer(`https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${accessToken}`, {
        attribution: `Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>`,
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: accessToken
}).addTo(mymap);

places.forEach(ele=>{
    let marker=L.marker(ele.coordinates).addTo(mymap)
    marker.on('mouseover', function(e) { 
        tooltipPopup = L.popup({ offset: L.point(0, -50)});
                tooltipPopup.setContent(`<b>${ele.hotel}<br><span class="text-center">$${ele.rate}<b></span>`);
                tooltipPopup.setLatLng(e.target.getLatLng());
                tooltipPopup.openOn(mymap);
        });
    
        marker.on('mouseout', function(e) { 
            mymap.closePopup(tooltipPopup);
        });
    })

    // Sorting places on basis of day of visit
    places.sort((a,b)=>b.rating - a.rating)

    // End loading 
    loading.style.display="none"
    // Call to display the itinary table
    displayPlaces(places)
}


const formatData=(data)=>{
    
    let hotels=[];
    console.log(data);
    const {address,city,hotelname,latitude,longitude,maxoccupancy,onsiterate,roomtype_x,distance,starrating,url} = data 
    for(var i=0;i<city.length;i++){
        
        hotels.push({
            cityName:city[i],
            coordinates:[latitude[i],longitude[i]],
            hotel:hotelname[i],
            dist:distance[i],
            maxCap:maxoccupancy[i],
            roomType:roomtype_x[i],
            hotelAddress:address[i],
            rate:onsiterate[i],
            rating:starrating[i],
            hotel_url:url[i],
        })
    }
    
    plotMap(hotels)

}

const getResponse=async(data)=>{
    const formData = new FormData();
    formData.append('city',data.city);
    formData.append("add",data.address)
    formData.append('nec',data.necessity);
    formData.append("g",data.guests)

    const url="http://localhost:5000";
    const config={
        method:"POST",
        body:formData
    }
    try{
        const response = await fetch(url,config)
        const data=await response.json()
        console.log(data)
        formatData(data)
    }
    catch(err){
        loading.style.display="none";
        alert("Sorry could not process your request...")
        console.log(err)
    }
}

const TakeInput=(e)=>{
    e.preventDefault()

    // Clear the already rendered data
    map.innerHTML=""
    mapDiv.style.display="none"
    tbody.innerHTML=""
    tableDiv.style.display="none"
    // Show Loading
    loading.style.display="block";
    
    if(input_city.value!=="" && input_address.value!=="" && input_guests.value!=="" && input_necessity.value!==""){
        getResponse({city:input_city.value,address:input_address.value,necessity:input_necessity.value,guests:input_guests.value})
    }
    else{
        loading.style.display="none"
        alert("Plese Provide all details...")
    }
}

btn.addEventListener("click",TakeInput)
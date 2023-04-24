const productTemplate = (obj) => {
    const root = document.createElement("div");
    const elem = [];
    for (let index = 0; index < 10; index++) {
        elem[index] = document.createElement("div");
    }
    root.className = "card mb-3";
    elem[0].className = "card-body";
    elem[1].className = "d-flex justify-content-between";
    elem[2].className = "d-flex flex-row align-items-center";
    elem[3].className = "";
    elem[4].className = "ms-3";
    elem[5].className = "d-flex flex-row align-items-center";
    elem[6].style.width = "50px";
    elem[7].style.width = "80px";
    elem[7].innerHTML = "<h5 class=\"mb-0\">Rs. "+obj["total_price"]+"</h5>";
    elem[6].innerHTML = "<h5 class=\"fw-normal mb-0\">"+obj["product_quantity"]+"</h5>";
    elem[5].appendChild(elem[6]);elem[5].appendChild(elem[7]);
    elem[4].innerHTML = "<h5>"+obj["product_name"]+"</h5><p class=\"small mb-0\">Rs. "+obj["product_price"]+"</p>";
    elem[3].innerHTML = "<img src=\"{{url_for('static', filename='logo.jpeg')}}\" class=\"img-fluid rounded-3\" alt=\"Shopping item\" style=\"width: 65px;\">";
    elem[2].appendChild(elem[3]); elem[2].appendChild(elem[4]);
    elem[1].appendChild(elem[2]); elem[1].appendChild(elem[5]); elem[0].appendChild(elem[1]);
    root.appendChild(elem[0]);
    return root;
}

fetch("/cartdata1")
  .then((response) => response.json())
  .then((data) => {console.log(data);
return data;}).then((data) => {
    const root = document.getElementById("prod_root");
    data.forEach(element => {
        root.appendChild(productTemplate(element));
    });
});

fetch("/cartdata2")
  .then((response) => response.json())
  .then((data) => {console.log(data);
return data;}).then((data) => {
    const root = document.getElementsByClassName("subtotal");
    for (let index = 0; index < root.length; index++) {
        const element = root[index];
        element.innerText = "Rs. " + data[0]["grand_total"];
        
    }
});


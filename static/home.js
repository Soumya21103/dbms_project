
const categoryRedirect = (data) => {
    let a = data.getAttribute('cat_id');
    console.log("yoli",a);
    let dat = JSON.stringify({'c_id' : a +''});
    console.log(JSON.parse(dat));
    // console.log(dat);
    fetch("/productdata", {
  method: "POST", // or 'PUT'
  headers: {
    "Content-Type": "application/json",
  },
  body: dat,
  
})
//   .then((response) => response.json())
//   .then((data) => {
//     console.log("Success:", data);
//   })
//   .catch((error) => {
//     console.error("Error:", error);
//   });
window.location = "/productdata?&c_id="+a;  
}

const categoryTemplate = (cat_name,cat_id) => {
    const root = document.createElement('div');
    root.className = "col-lg-4 col-md-6 mb-4";
    root.setAttribute('cat_id',cat_id);
    root.setAttribute('cat_name',cat_name);
    // root.onclick = () => {categoryRedirect(root)};
    const in1 = [];
    for (let index = 0; index < 2; index++) {
        in1.push(document.createElement('div'));
    }
    
    in1[0].className = "card hover-lift hover-shadow-xl shadow-sm border-0";
    in1[1].className = "card-body p-4";
    const h5 = document.createElement('h5');
    h5.innerText = cat_name;
    in1[1].appendChild(h5);
    in1[0].appendChild(in1[1]);
    root.appendChild(in1[0]);
    const a = document.createElement('a');
    a.href = "productdata/"+cat_id;
    a.className = "stretched-link";
    in1[0].appendChild(a);
    return root;
}

fetch("/catdata")
  .then((response) => response.json())
  .then((data) => {console.log(data);
return data;}).then((data) => {
    const root = document.getElementById("cat-container");
    data.forEach(element => {
        root.appendChild(categoryTemplate(element["name"],element["id"]));
    });
});

function IdSelector(id) {
  return document.getElementById(id);
}
console.log("main js connected");
const navSearch = IdSelector("navBarSearchForm");

navSearch.addEventListener("keyup", () => {
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/site-search", true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.onload = function () {
    let data = JSON.parse(this.responseText).data_d;
    let datab = "";
    if (data.length != 0) {
      for (let i = 0; i < data.length; i++) {
        datab += `<li><a class="dropdown-item" title="Book Plan" href="/bookplan/${data[i].id}"><span class="text-success">${data[i].pname}</span> By <span class="text-success">${data[i].buname}</span> Type <span class="text-success">${data[i].mealtype}</span></a></li>`;
        if (data.length - i != 1) {
          datab += '<li><hr class="dropdown-divider" /></li>';
          console.log(`last`);
        }
      }
      IdSelector("search_res").innerHTML = datab;
    } else {
      IdSelector(
        "search_res"
      ).innerHTML = `<li class="text-danger text-center py-1">Data Not Found</li>`;
    }
  };
  xhr.send("data=" + navSearch.value);
});


document.querySelectorAll(".payment_info_show").forEach(function (e) {
  e.addEventListener("click", function () {
    let pay_id = this.getAttribute("data-id");
    let xhr2 = new XMLHttpRequest();
    xhr2.open("POST", "/payment-details-admin", true);
    xhr2.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr2.onload = function () {
      let data = JSON.parse(this.responseText).data[0];
      IdSelector("pd_oi").innerHTML = data.order_id;
      IdSelector("pd_rpid").innerHTML = data.razorpay_payment_id;
      IdSelector("pd_oa").innerHTML = data.amount;
      if (data.paid == true) {
        IdSelector("pd_ps").innerHTML = "Paid";
      } else {
        IdSelector("pd_ps").innerHTML = "UnPaid";
      }
    };
    xhr2.send("oid=" + pay_id);
  });
});

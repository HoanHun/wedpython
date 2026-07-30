var updatebtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updatebtns.length; i++) {
  updatebtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId:", productId, "action:", action);
    console.log("user: ", user);
    // xem nguoi dung co dang nhap hay khong, ko thi chuyeb sang trang dang nhap
    if (user === "AnonymousUser") {
      console.log("Cần đăng nhập");
    } else {
      updateUserOrder(productId, action);
    }
  });
}
function updateUserOrder(productId, action) {
  console.log("Đã thêm");
  var url = "/updateitem/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data:", data);
      location.reload();
    });
}

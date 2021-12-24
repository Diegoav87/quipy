function updateCart(productId, qty, productPrice, cartCount, totalProductEl, subtotalEl, csrftoken, url) {
    if (qty === "" || qty === "0") {
        Toastify({
            text: "Please enter a quantity",
            duration: 3000,
            close: true,
            style: {
                background: "linear-gradient(to right, #e80757, #e80909)",
            }
        }).showToast();
        return;
    }

    const data = new FormData();
    data.append("productId", productId);
    data.append("productQty", qty);
    data.append("csrfmiddlewaretoken", csrftoken);

    axios
        .post(url, data)
        .then(function (response) {
            console.log(response.data);
            cartCount.innerHTML = response.data.qty;
            subtotalEl.innerHTML = "$" + response.data.subtotal;
            totalProductEl.innerHTML = "$" + (productPrice * parseInt(qty)).toFixed(2);

            Toastify({
                text: "Item updated",
                duration: 3000,
                close: true,
                className: "alert alert-success",
                style: {
                    background: "linear-gradient(to right, #00b09b, #96c93d)",
                }
            }).showToast();
        })
        .catch(function (error) {
            console.log(error);
            Toastify({
                text: "Something went wrong",
                duration: 3000,
                close: true,
                style: {
                    background: "linear-gradient(to right, #e80757, #e80909)",
                }
            }).showToast();
        });
}
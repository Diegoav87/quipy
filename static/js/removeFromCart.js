function removeFromCart(deleteCartBtn, cartCount, subtotalEl, csrftoken, url) {
    const data = new FormData();
    data.append("productId", deleteCartBtn.value);
    data.append("csrfmiddlewaretoken", csrftoken);

    axios
        .post(url, data)
        .then(function (response) {
            console.log(response.data);
            cartCount.innerHTML = response.data.qty;
            subtotalEl.innerHTML = "$" + response.data.subtotal;

            const rowToRemove = document.querySelector("#row-" + deleteCartBtn.value);
            rowToRemove.parentElement.removeChild(rowToRemove);

            Toastify({
                text: "Item removed from cart",
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
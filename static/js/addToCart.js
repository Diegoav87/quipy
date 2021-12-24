function addToCart(addCartBtn, qty, cartCount, csrftoken, url) {

    if (qty === "") {
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
    data.append("productId", addCartBtn.value);
    data.append("productQty", qty);
    data.append("csrfmiddlewaretoken", csrftoken);

    axios
        .post(url, data)
        .then(function (response) {
            console.log(response.data);
            cartCount.innerHTML = response.data.qty;
            Toastify({
                text: "Item added to cart",
                duration: 3000,
                close: true,
                style: {
                    background: "linear-gradient(to right, #00b09b, #96c93d)",
                }
            }).showToast();
        })
        .catch(function (error) {
            console.log(error.response);

            if (error.response.status == 400) {
                Toastify({
                    text: error.response.data.error,
                    duration: 3000,
                    close: true,
                    style: {
                        background: "linear-gradient(to right, #e80757, #e80909)",
                    }
                }).showToast();
            } else {
                Toastify({
                    text: "Something went wrong",
                    duration: 3000,
                    close: true,
                    style: {
                        background: "linear-gradient(to right, #e80757, #e80909)",
                    }
                }).showToast();
            }
        });
}
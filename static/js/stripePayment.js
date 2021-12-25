const stripe = Stripe("pk_test_51KAcQsBxNNH6TRWIgiA5Uo80JMVcu0OjPPyhVZ7yXhPcdpVzDlEhbjtjvIYySTbwQkJeOR1VDmYddFAdmy8M7eMf00hPMNDIiW");

const submitBtn = document.getElementById("submit-payment");
const clientSecret = submitBtn.getAttribute("data-secret");

const elements = stripe.elements();
const style = {
    base: {
        background: "#F0F0E9",
        border: "0 none",
        marginBottom: "10px",
        padding: "10px",
        width: "100%",
        fontWeight: "300",
    }
};

const card = elements.create("card", { style: style })
card.mount("#card-element");

const form = document.getElementById('payment-form');

form.addEventListener('submit', function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const address = document.getElementById("address").value;
    const addressTwo = document.getElementById("address-two").value;
    const postCode = document.getElementById("post-code").value;

    const data = new FormData();
    data.append("order_key", clientSecret);
    data.append("csrfmiddlewaretoken", CSRF_TOKEN);

    axios
        .post(addOrderUrl, data)
        .then(res => {
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        address: {
                            line1: address,
                            line2: addressTwo
                        },
                        name: name
                    },
                }
            }).then(function (result) {
                if (result.error) {
                    console.log('payment error')
                    console.log(result.error.message);
                    Toastify({
                        text: result.error.message,
                        duration: 3000,
                        close: true,
                        style: {
                            background: "linear-gradient(to right, #e80757, #e80909)",
                        }
                    }).showToast();
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        console.log('payment processed');
                        Toastify({
                            text: "Payment processed",
                            duration: 3000,
                            close: true,
                            style: {
                                background: "linear-gradient(to right, #00b09b, #96c93d)",
                            }
                        }).showToast();
                        window.location.replace("http://127.0.0.1:8000/payment/order-placed/");
                    }
                }
            });
        })
        .catch(err => {
            Toastify({
                text: "Something went wrong",
                duration: 3000,
                close: true,
                style: {
                    background: "linear-gradient(to right, #e80757, #e80909)",
                }
            }).showToast();
        })


});
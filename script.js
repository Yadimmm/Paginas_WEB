let cart = [];

function addToCart(button) {
    const product = button.parentElement;
    const name = product.dataset.name;
    const price = parseFloat(product.dataset.price);
    const quantity = parseInt(product.querySelector('#cantidad').value);

    const productInCart = cart.find(item => item.name === name);

    if (productInCart) {
        productInCart.quantity += quantity;
    } else {
        cart.push({ name, price, quantity });
    }

    updateCart();
}

function updateCart() {
    const cartItemsContainer = document.getElementById('cart-items');
    const cartCount = document.getElementById('cart-count');
    cartItemsContainer.innerHTML = '';

    let totalPrice = 0;
    let totalItems = 0;

    cart.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.innerText = `${item.name} - $${item.price} x ${item.quantity}`;
        cartItemsContainer.appendChild(itemElement);

        totalPrice += item.price * item.quantity;
        totalItems += item.quantity;
    });

    document.getElementById('total-price').innerText = totalPrice.toFixed(2);
    cartCount.innerText = totalItems;
}

// Para hacer que el enlace se desplace suavemente a la sección del carrito
document.getElementById('cart-link').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('cart-section').scrollIntoView({ behavior: 'smooth' });
});
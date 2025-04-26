function removeItem(item){
    fetch(`/cart/remove_item/${encodeURIComponent(item)}`,{method:'POST'})
    .then(response=>{
        if(response.ok){
            document.getElementById(`item-${encodeURIComponent(item)}`).remove();
            document.getElementById("message").innerText = "The item removed";

        }else{
            alert("Item not found or couldn't be removed.");
        }
    });
}
function updateQuantity(item, delta) {
    fetch('/cart/update_quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `item=${encodeURIComponent(item)}&delta=${delta}`
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url; // אם השרת מחזיר רידיירקט
        }
    })
    .catch(error => {
        console.error('Error updating quantity:', error);
        alert('Failed to update quantity.');
    });
}

function removeItem(item) {
    fetch(`/cart/remove_item/${encodeURIComponent(item)}`, {
        method: 'POST'
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    })
    .catch(error => {
        console.error('Error removing item:', error);
        alert('Failed to remove item.');
    });
}

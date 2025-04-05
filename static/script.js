function removeItem(item){
    fetch(`/cart/remove_item/${encodeURIComponent(item)}`,{method:'DELETE'})
    .then(response=>{
        if(response.ok){
            document.getElementById(`item-${encodeURIComponent(item)}`).remove();
            document.getElementById("message").innerText = "The item removed";

        }else{
            alert("Item not found or couldn't be removed.");
        }
    });
}
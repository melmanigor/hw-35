function removeItem(item){
    fetch(`/remove_item/${encodeURIComponent(item)}`,{method:'DELETE'})
    .then(response=>{
        if(response.ok){
            document.getElementById(`item-${encodeURIComponent(item)}`).remove();

        }else{
            alert("Item not found or couldn't be removed.");
        }
    });
}
window.onload = function() {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        let t_href = event.target
        console.log(t_href.name)
        console.log(t_href.value)

        $.ajax(
            {
                url: "/baskets/edit" + t_href.name + "/" + t_href.value + "/",
                success: function (data){
                    $('.basket_list').html(data.result)
                },
//                errors: function()
            });
        event.preventDefault()
    })

        $('.card_add_basket').on('click', 'button[type="button"]', function () {
        let product_id = event.target.value
        let product_name = event.target.getAttribute('prod_name')

        $.ajax(
            {
                url: "/baskets/add/" + product_id + "/",
                success: function (data){
                    $('.card_add_basket').html(data.result)
                    alert(`Товар ${product_name} добавлен в корзину`)
                },
//                errors: function()
            });
        event.preventDefault()
    })
}
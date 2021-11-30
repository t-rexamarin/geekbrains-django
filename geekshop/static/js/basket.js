window.onload = function() {
    // редактирование кол-ва товара в профиле
    $('.basket_list').on('click', 'input[type="number"]', function () {
        let t_href = event.target
        console.log(t_href.name)
        console.log(t_href.value)

        $.ajax(
            {
                url: "/baskets/edit/" + t_href.name + "/" + t_href.value + "/",
                success: function (data){
                    $('.basket_list').html(data.result)
                },
//                errors: function()
            });
        event.preventDefault()
    })

    // добавление в корзину с просмотра всех товаров
    $('.card_add_basket').on('click', 'button[type="button"]', function () {
        let product_id = event.target.value
        let product_name = event.target.getAttribute('prod_name')
        console.log(product_id)

        $.ajax(
            {
                url: "/baskets/add/" + product_id + "/",
                success: function (data){
                    // чтобы не возвращал на список товаров
                    //$('.card_add_basket').html(data.result)
                    alert(`Товар ${product_name} добавлен в корзину`)
                },
//                errors: function()
            });
        event.preventDefault()
    })

    // добавление в корзинку с индивидуальной карточки товара
    $('.item_card').on('click', 'button[type="button"]', function () {
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

    // удаление кол-ва товара в профиле
    $('.basket_list').on('click', 'i.fa-trash', function () {
        let basket_id = event.target.getAttribute('basket_id')
        console.log(basket_id)

        $.ajax(
            {
                url: `/baskets/remove/${basket_id}`,
                success: function (data){
                    $('.basket_list').html(data.result)
                },
//                errors: function()
            });
        event.preventDefault()
    })
}
window.onload = function() {
    function createAlert(parentElement) {
        let alertBlock = document.createElement('div');

        alertBlock.setAttribute('id', 'success-alert');
        alertBlock.className = 'custom-alert alert-success';
        alertBlock.innerHTML = '<strong>Success!</strong> Product has been added to your cart';
        parentElement.insertAdjacentElement('beforeend', alertBlock);

        $("#success-alert").fadeTo(1000, 500).slideUp(500, function() {
            $("#success-alert").slideUp(500);
            $("#success-alert").remove();
        });
    }

    // редактирование кол-ва товара в профиле
    $('.basket_list').on('click', 'input[type="number"]', function () {
        let t_href = event.target;
        //console.log(t_href.name);
        //console.log(t_href.value);

        $.ajax(
            {
                //url: "/baskets/edit/" + t_href.name + "/" + t_href.value + "/",
                url: `/baskets/edit/${t_href.name}/${t_href.value}`,
                success: function (data){
                    $('.basket_list').html(data.result);
                },
                    //errors: function()
            });
        event.preventDefault();
    });

    // добавление в корзину с просмотра всех товаров
    $('.card_add_basket').on('click', 'button[type="button"]', function () {
        let product_id = event.target.value;
        let product_name = event.target.getAttribute('prod_name');
        let targetParent = event.target.parentElement;

        $.ajax(
            {
                //url: "/baskets/add/" + product_id + "/",
                url: `/baskets/add/${product_id}/`,
                success: function (data){
                    // чтобы не возвращал на список товаров
                    //$('.card_add_basket').html(data.result)
                    //alert(`Товар ${product_name} добавлен в корзину`)
                    createAlert(targetParent);
                },
                    //errors: function()
            });
        event.preventDefault()
    });

    // добавление в корзинку с индивидуальной карточки товара
    $('.item_card').on('click', 'button[type="button"]', function () {
        let product_id = event.target.value;
        let product_name = event.target.getAttribute('prod_name');
        let targetParent = event.target.parentElement;

        $.ajax(
            {
                //url: "/baskets/add/" + product_id + "/",
                url: `/baskets/add/${product_id}/`,
                success: function (data){
                    $('.card_add_basket').html(data.result)
                    createAlert(targetParent);
                    //alert(`Товар ${product_name} добавлен в корзину`)
                },
                    //errors: function();
            });
        event.preventDefault();
    });

    // удаление кол-ва товара в профиле
    $('.basket_list').on('click', 'i.fa-trash', function () {
        let basket_id = event.target.getAttribute('basket_id');
        //console.log(basket_id);

        $.ajax(
            {
                url: `/baskets/remove/${basket_id}`,
                success: function (data){
                    $('.basket_list').html(data.result);
                },
                    //errors: function();
            });
        event.preventDefault();
    });
}
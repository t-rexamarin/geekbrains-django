window.onload = function(){
    let quantity, price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let prices_arr = [];

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text()) || 0;

    for(let i = 0; i < total_forms; i++){
        quantity = parseInt($(`input[name=orderitems-${i}-quantity]`).val());
        price = parseFloat($(`.orderitems-${i}-price`).text());
        quantity_arr[i] = quantity;

        if(price){
            prices_arr[i] = price;
        }else{
            prices_arr[i] = 0;
        }
    }
//    console.info('QUANTITY', quantity_arr);
//    console.info('PRICE', prices_arr);

//  при клике на кол-ва товара
    $('.order_form').on('click', 'input[type=number]', function(){
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''))
        if(prices_arr[orderitem_num]){
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(prices_arr[orderitem_num], delta_quantity);
        }
    });

//  при клике на удалению товара
    $('.order_form').on('click', 'input[type=checkbox]', function(){
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''))
        if(target.checked){
            delta_quantity = -quantity_arr[orderitem_num];
        }else{
            delta_quantity = quantity_arr[orderitem_num];
        }

        orderSummaryUpdate(prices_arr[orderitem_num], delta_quantity);
    });


//  пересчет итоговой формы
    function orderSummaryUpdate(orderitem_price, delta_quantity){
        delta_cost = orderitem_price * delta_quantity;
//        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_cost = (parseFloat(order_total_cost) + delta_cost).toFixed(2);
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    })

//  при удалении позиции из заказа
    function deleteOrderItem(row){
        let target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(prices_arr[orderitem_num], delta_quantity);
    }

//  смена товара в выпадающем списке
    $('.order_form select').change(function () {
        let target = event.target;
        let targetId = parseInt(target.id.replace('id_orderitems-', '').replace('-product', ''));
        let parentRow = target.parentElement.parentElement;
        let targetQuantity = parseInt(parentRow.querySelector(`#id_orderitems-${targetId}-quantity`).value);
        let targetPrice = parseFloat(parentRow.querySelector(`.orderitems-${targetId}-price`).innerText.replace(' руб', ''));
        let orderitem_product_pk = target.options[target.selectedIndex].value;

        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));

        if (orderitem_product_pk) {
            $.ajax({
                url: `/orders/get_product_price/${orderitem_product_pk}`,
                success: function (data) {
                    if (data.price) {
//                        если получили новые данные, минусуем кол-во и цену старого товара
                        order_total_cost = (parseFloat(order_total_cost) - targetPrice * targetQuantity).toFixed(2);
                        order_total_quantity = order_total_quantity - targetQuantity;

                        prices_arr[orderitem_num] = parseFloat(data.price)
                        if (isNaN(quantity_arr[orderitem_num])) {
                            quantity_arr[orderitem_num] = 0;
                        }

                        let price_html = `<span class="orderitems-${orderitem_num}-price">${data.price}</span> руб`;
                        let current_tr = $('.order_form table').find('tr:eq('+(orderitem_num+1)+')');
                        current_tr.find('td:eq(2)').html(price_html);
//                        апдейтим итоговую инфу по заказу
                        orderSummaryUpdate(prices_arr[orderitem_num], quantity_arr[orderitem_num]);
                    }
                }
            });
        }
    });

    function createAlert(parentElement) {
        let alertBlock = document.createElement('div');

//      быстрый костыль. Если алертов несколько, то плохо работает
//        alertBlock.setAttribute('class', 'success-alert');
        alertBlock.className = 'custom-alert alert-success success-alert';
        alertBlock.innerHTML = '<strong>Success!</strong> Product has been added to your cart';
        parentElement.insertAdjacentElement('beforeend', alertBlock);

        $(".success-alert").fadeTo(1000, 500).slideUp(500, function() {
            $(".success-alert").slideUp(500);
            $(".success-alert").remove();
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
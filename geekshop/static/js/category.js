$('.categories').on('click', 'a', function () {
    let cat_id = event.target.getAttribute('category')
    console.log(cat_id)

    $.ajax(
        {
            url: `/products/${cat_id}`,
            success: function (data){
                $('.card_add_basket').html(data.result)
            },
//                errors: function()
        });
    event.preventDefault()
})
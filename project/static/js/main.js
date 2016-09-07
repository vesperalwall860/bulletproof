$(document).ready(function() {
    $('.shop-inner .tabs .tab-title li').click(function() {
        var $this = $(this);
        var index = $this.index();
        var tabBody = $('.shop-inner .tabs .tab-body li:eq(' + index + ')');
        console.log(index);
        $('.shop-inner .tabs .tab-title li').removeClass('active');
        $('.shop-inner .tabs .tab-body li').removeClass('active');
        $this.addClass('active');
        tabBody.addClass('active');
    });
    $('.shop-inner .input-outer .plus').click(function() {
        var $this = $(this);
        var input = $this.parent().parent().find('input');
        input.val(+input.val()+1);
    });
    $('.shop-inner .input-outer .minus').click(function() {
        var $this = $(this);
        var input = $this.parent().parent().find('input');
        if (+input.val() > 1) {
            input.val(+input.val()-1);
        }
    });
    $('.shop-inner .btn-add-to-cart, ul.products .btn-add-to-cart').click(function(e) {
        var $this = $(this);
        var productId = $this.attr('data-id');
        var qty = 1;

        e.preventDefault();

        if ($this.is('button')) {
            qty = $('input.qty').val();
        }

        $.get('/cart/add/' + productId, {'qty': qty}, function(data){
            if (data != 'None' && data != 'Empty') {
                $('#cart .inner').removeClass('empty');
                $('#cart ul').html(data);
                $('#cart > div > strong').text($('#cart ul li').length - 1);
                alert('Cart has been updated.');
            }
            if (data == 'Empty') {
                $('#cart .inner').addClass('empty');
                $('#cart ul').html('');
                $('#cart > div > strong').text('0');
                alert('Cart has been updated.');
            }
        });
    });
    $('#cart, table').on('click', '.delete', function() {
        var $this = $(this);
        var productId = $this.attr('data-id');

        $.get('/cart/delete/' + productId, function(data){
            if (data != 'None' && data != 'Empty') {
                $('#cart .inner').removeClass('empty');
                $('#cart ul').html(data);
                $('#cart > div > strong').text($('#cart ul li').length - 1);
                alert('Cart has been updated.');
                if (window.location.pathname.indexOf('checkout')!=-1) {
                    location.reload();
                }
            }
            if (data == 'Empty') {
                $('#cart .inner').addClass('empty');
                $('#cart ul').html('');
                $('#cart > div > strong').text('0');
                alert('Cart has been updated.');
                if (window.location.pathname.indexOf('checkout')!=-1) {
                    location.reload();
                }
            }
        });
    });
    $('.product-details span.product-reviews a').click(function(e) {
        e.preventDefault();
        $('.review-add-popup-bg').fadeIn();
        $('.review-add-popup').fadeIn();
    });
    $('.review-add-popup-bg').click(function(e) {
        $(this).fadeOut();
        $('.review-add-popup').fadeOut();
    });
    $('.review-add-popup form button').click(function(e) {
        e.preventDefault();
        var productId = $('.review-add-popup form input[name="product_id"]').val();
        var validate = true;
        // collect all the form's inputs data
        var context = {
            'author': $('.review-add-popup form input[name="author"]').val(),
            'author_email': $('.review-add-popup form input[name="author_email"]').val(),
            'text': $('.review-add-popup form textarea[name="text"]').val(),
            'rate': $('.review-add-popup form input[name="rate"]:checked').val()
        }
        // check if any of the fields are not filled, 
        // otherwise don't allow it to be sent
        for (var key in context) {
            if (context[key] === undefined){
                validate = false;
                continue;
            }
            if (context[key].length == 0) {
                validate = false;
            }
        }
        if (validate) {
            $.post('/review/add/' + productId, context, function(data) {
                console.log(data);
                // check if the product we want to add a review to exists
                if (data != 'None') {
                    alert('Your review has been sent.');
                    $('.shop-inner .tab-body li:nth-child(2)').html(data);
                    // close the popup window
                    $('.review-add-popup-bg').click();
                }
            });
        } else {
            alert('All the fields are required.');
        }
    });
    $('.slider-body').unslider();

});
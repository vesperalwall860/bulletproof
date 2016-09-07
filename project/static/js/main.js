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
    $('.slider-body').unslider();

});
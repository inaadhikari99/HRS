$(document).ready(function(){
$(document).on('click',".btn.add-wishlist",function(){
        var hid=$(this).attr('data-hotel');
        var vm=$(this);
         $.ajax({
             url:"/add_wishlist",
             data:{
                    hotel:hid
         },
         dataType:'json',
         success:function(res){
           if(res.bool==true){
           vm.addClass('btn btn-sm btn-danger disabled').remove('btn.add-wishlist');
           }
         }

         });
         //ajax end garne
    });
//end
});



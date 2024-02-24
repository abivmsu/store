$(document).ready(function () {
 
  $("#add-list").click(function (e) {
    e.preventDefault();
   
    console.log("asdasdfa");
    $.ajax({
      type: "POST",
      
      data: {
          product_id: $('#add-list').val(),
          product_type: $('#type').val(),
          quantity: $('#quantity').val(),
          csrfmiddlewaretoken: ' {{csrf_token}}',
          action: 'post'
      },

      success: function(json){
        console.log(json)
      },

      erorr: function(xhr, errmsg,err){

      }
  });
  });
});

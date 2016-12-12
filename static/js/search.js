/**
 * Created by Jaekwang on 12/11/2016.
 */
$(function(){

    $("button").click(function(){
    		console.log("button clicked")
       var data = $("form").serialize()
		console.log(data);
       $("#result").load("/search?"+data)
    });

    /*
    $.getJSON( "ajax/test.json", function( data ) {
      var items = [];
      $.each( data, function( key, val ) {
        items.push( "<li id='" + key + "'>" + val + "</li>" );
      });

      $( "<ul/>", {
        "class": "my-new-list",
        html: items.join( "" )
      }).appendTo( "body" );
    });
    */
    /*
	$('button').click(function(){
	    console.log("Button clicked");
	    console.log($('form').serialize());

	    $.ajax({
          url: '/',
          type: 'GET',
          data: $('form').serialize,
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
        });
	});*/
});


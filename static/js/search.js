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

});


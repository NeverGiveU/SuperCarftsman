$(function(){

    $("#submit").click(function(){
        var data = {
            'signal': 1
        };
        $.ajax({
            type: 'GET',
            url: "register",
            data: data,
            dataType: 'text',
            success: function(data) {
                console.log("Success!");
            },
            error: function(error) {
                console.log("Fail!");
            }
        });
    })

})


$(function(){

    $("#submit").on('click', function(){
        // recover
        $("#nickname").css("border","1px solid black");
        $("#account").css("border","1px solid black");
        $("#email").css("border","1px solid black");
        $("#password").css("border","1px solid black");
        $("#password2").css("border","1px solid black");
        document.getElementById("warning").style.display="none";

        var nickname = $('#nickname').val();
        var account = $('#account').val();
        var email = $('#email').val();
        var password = $('#password').val();
        var password2 = $('#password2').val();

        var flag = true;

        // alert if not full
        if(nickname.length == 0){
            $("#nickname").css("border","1px solid red");
            flag = false;
        }
        if(account.length == 0){
            $("#account").css("border","1px solid red");
            flag = false;
        }
        if(email.length == 0){
            $("#email").css("border","1px solid red");
            flag = false;
        }
        if(password.length == 0){
            $("#password").css("border","1px solid red");
            flag = false;
        }
        if(password2.length == 0){
            $("#password2").css("border","1px solid red");
            flag = false;
        }
        if(password != password2){
            console.log("jgxx");
            document.getElementById("warning").style.display="";
            //$("#warning").style.display=true;
            console.log("jgxx");
            flag = false;
        }
        if(flag == true){
            var data = {
                'nickname':nickname,
                'account':account,
                'email':email,
                'password':password,
                'password2':password2
            };
            $.ajax({
                type: 'GET',
                url: register,
                data: data,
                dataType: 'json',
                success: function(data) {
                    var res = data.res;
                    if(res == 1){
                        document.getElementById("gotohome").style.display="";
                    }else{ // -1
                        $("#account").css("border","1px solid red");
                        alert("Fail to register, the ACCOUNT has been used! Please try again!");
                    }
                },
                error: function() {
                    console.log("Fail!");
                }
            });
        }
    })

    $("#login").on('click', function(){
        var account = $("#account").val();
        var password =$("#password").val();
        var data = {
            'account':account,
            'password':password
        };
        $.ajax({
            type:'GET',
            url:'/SuperCraftsman/login',
            data:data,
            dataType:'json',
            success:function(data){
                if (data.state == 1){
                    // console.log(data.nickname);
                    document.getElementById("subscribe").style.display="none";
                    document.getElementById("self_info").innerHTML=data.nickname;
                    document.getElementById("self_info_board").style.display="";
                    document.getElementById("close").click()
                }else if(data.state == 2) {
                    alert("The account has been used, please try another one!");
                }
                else{ // -1
                    alert("Account/Password is wrong, please try again!");
                    // empty
                    $("#account").val("");
                    $("#password").val("");
                }
            },
            error:function(){
                console.log('Fail!');
            }
        })
    })
})


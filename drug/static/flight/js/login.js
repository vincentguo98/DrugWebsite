
$(document).on("click", "#login", function () {
    var username = $("#username").val();
    var password = $("#password").val();
    $.ajax({
        type:"post",
        url:"../login/",
        data:{
            'username':username,
            'password':password
        },
        success:function (data) {
            console.log(data);
            if (data == "1"){
                window.location.href = "/sports/group/register/"
                // window.location.href("../group-register.html/")
            }
            if(data == "2"){
                console.log("ggsmd")
                alert("密码错误，重新输入")
                location.href = '../pre_login/'
                // window.location.href = '../sports/pre_login/';
                // window.location.href("../pre_login/")

            }
        }
    });
});

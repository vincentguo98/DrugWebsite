$(document).ready(function () {
});

$(document).on("click", "#register", function () {
    var username = $("#username").val();
    var password = $("#password").val();
    var name = $("#name").val();
    var id_number = $("#id-number").val();
    
    $.ajax({
        type:"post",
        url:"solve/",
        data:{
            "username":username,
            "password":password,
            "name":name,
            "id_number":id_number
        },
        success:function (data) {
            if (data == "2"){
                swal({
                    title: "\n用户名已注册!",
                    text: "",
                    type: "error",
                    confirmButtonText: "OK"
                },
                function () {
                   // window.location.href = "../index";
                });
            }
            else
            {
                swal({
                    title: "\n注册成功!",
                    text: "",
                    type: "success",
                    confirmButtonText: "OK"
                },
                function () {
                   window.location.href = "../login";
                });
            }
        }
    });
});
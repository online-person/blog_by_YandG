function check_all() {
    var uname = $('#user_name').val();
    var unc = $('#unameinfo').css('color');
    // var uemail = $("#user_email").val();
    var $upobj = $("#user_pwd");
    var $ucpobj = $("#user_c_pwd");
    var upwd = $upobj.val();
    var ucpwd = $ucpobj.val();
    var ucpc = $("#ucpwdinfo").css('color');

    $upobj.val(md5(upwd));
    $ucpobj.val(md5(ucpwd));

    return (6<uname.length) && (uname.length<12) && (unc !='rgb(255, 0, 0)') && (upwd === ucpwd) &&(ucpwd !='rgb(255, 0, 0)');

}

$(function () {
    $('#user_name').change(function () {

        var value = $(this).val();
        console.log(value);
        $.getJSON('/blog/check/',{'u_name':value},function (data) {
            console.log(data);
            if(value.length>6 && value.length<12){
                if (data['status'] == '200'){
                $('#unameinfo').html('有效ID').css('color','green')
            }else {
                $('#unameinfo').html('无效id').css('color','red')
            }
            }else {
                $('#unameinfo').html('6到12位').css('color','red')
            }


        })
    });
    $('#user_c_pwd').change(function () {
            if($(this).val() === $('#user_pwd').val()){
                $("#ucpwdinfo").html('').css('color','green');
            }else {
                $("#ucpwdinfo").html('密码不一致').css('color','red');
            }
    })

});
/**
 * Created by zyh on 2016/5/21.
 */
//ajax_modify 提交修改"部位-费用-胶片"
$.ajax_modify=
    $.ajax({
         type: 'POST',
         url: '/tablespacs/bodypartDic/',
         data: {
             "posttype":"modify",
             "bodypart": $("#bodypart").val(),
             "fee": $("#fee").val(),
             "film_text": $("#film_text").val(),
         },    //post请求的条件
         //dataType: 'json',
         success: function (result) {
             dialog.dialog( "close" );
         },
         error: function () {
             alert("保存失败");
         }
    });
